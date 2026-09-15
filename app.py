# -*- coding: utf-8 -*-
"""
Backend du quiz de gestion de projet IA.
- Comptes : username unique + mot de passe (hache).
- Une seule tentative par (username, quiz).
- Classement par quiz.
- A la fin : score + bonnes reponses + explications.
Stack volontairement minimale : Flask + SQLite (stdlib). Aucune dependance externe hors Flask.
"""
import os, re, sqlite3, secrets, time
from flask import Flask, request, jsonify, g, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

from questions import QUIZZES, QUIZ_ORDER

DB_PATH = os.environ.get("QUIZ_DB", "/data/quiz.db")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
ADMIN_USER = os.environ.get("ADMIN_USER", "mohamed1780")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "MOHmoh1780@")

app = Flask(__name__, static_folder="static", static_url_path="")


# ---------- base de donnees ----------
def db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
        g.db = sqlite3.connect(DB_PATH, timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA busy_timeout=5000")  # attend jusqu'a 5s au lieu d'echouer sur ecritures concurrentes
    return g.db


@app.teardown_appcontext
def close_db(_):
    d = g.pop("db", None)
    if d:
        d.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users(
            username   TEXT PRIMARY KEY,
            pwhash     TEXT NOT NULL,
            token      TEXT UNIQUE,
            is_admin   INTEGER NOT NULL DEFAULT 0,
            created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS attempts(
            username   TEXT NOT NULL,
            quiz_id    TEXT NOT NULL,
            score      INTEGER NOT NULL,
            total      INTEGER NOT NULL,
            answers    TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            PRIMARY KEY(username, quiz_id)
        );
        """
    )
    # Migration : ajoute is_admin aux bases existantes
    try:
        conn.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    # Seed / promotion du compte admin. Idempotent et sans course entre workers :
    # INSERT OR IGNORE (le mot de passe n'est posé qu'à la première création),
    # puis on garantit le flag admin. Un second worker qui démarre en parallèle ne plante pas.
    if ADMIN_USER:
        conn.execute(
            "INSERT OR IGNORE INTO users(username, pwhash, token, is_admin, created_at) VALUES(?,?,?,1,?)",
            (ADMIN_USER, generate_password_hash(ADMIN_PASSWORD), None, int(time.time())),
        )
        conn.execute("UPDATE users SET is_admin=1 WHERE username=?", (ADMIN_USER,))
    conn.commit()
    conn.close()


# ---------- auth ----------
def current_row():
    auth = request.headers.get("Authorization", "")
    token = auth[7:].strip() if auth.startswith("Bearer ") else ""
    if not token:
        return None
    return db().execute("SELECT username, is_admin FROM users WHERE token=?", (token,)).fetchone()


def current_user():
    row = current_row()
    return row["username"] if row else None


def require_user():
    u = current_user()
    if not u:
        return None, (jsonify(error="Non authentifié"), 401)
    return u, None


def require_admin():
    row = current_row()
    if not row:
        return None, (jsonify(error="Non authentifié"), 401)
    if not row["is_admin"]:
        return None, (jsonify(error="Accès réservé à l'administrateur"), 403)
    return row["username"], None


# ---------- API : comptes ----------
@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not USERNAME_RE.match(username):
        return jsonify(error="Nom d'utilisateur invalide (3–30 caractères : lettres, chiffres, . _ -)"), 400
    if len(password) < 4:
        return jsonify(error="Mot de passe trop court (4 caractères minimum)"), 400
    token = secrets.token_urlsafe(24)
    try:
        db().execute(
            "INSERT INTO users(username, pwhash, token, created_at) VALUES(?,?,?,?)",
            (username, generate_password_hash(password), token, int(time.time())),
        )
        db().commit()
    except sqlite3.IntegrityError:
        return jsonify(error="Ce nom d'utilisateur est déjà pris"), 409
    return jsonify(username=username, token=token, is_admin=False)


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    row = db().execute("SELECT pwhash, is_admin FROM users WHERE username=?", (username,)).fetchone()
    if not row or not check_password_hash(row["pwhash"], password):
        return jsonify(error="Identifiants incorrects"), 401
    token = secrets.token_urlsafe(24)
    db().execute("UPDATE users SET token=? WHERE username=?", (token, username))
    db().commit()
    return jsonify(username=username, token=token, is_admin=bool(row["is_admin"]))


@app.get("/api/me")
def me():
    row = current_row()
    if not row:
        return jsonify(error="Non authentifié"), 401
    u = row["username"]
    done = {r["quiz_id"] for r in db().execute("SELECT quiz_id FROM attempts WHERE username=?", (u,))}
    return jsonify(username=u, done=sorted(done), is_admin=bool(row["is_admin"]))


# ---------- API : quiz ----------
@app.get("/api/quizzes")
def quizzes():
    u = current_user()
    done = set()
    if u:
        done = {r["quiz_id"] for r in db().execute("SELECT quiz_id FROM attempts WHERE username=?", (u,))}
    items = []
    for qid in QUIZ_ORDER:
        q = QUIZZES[qid]
        items.append({"id": qid, "title": q["title"], "count": len(q["questions"]), "done": qid in done})
    return jsonify(quizzes=items)


def _public_questions(qid):
    """Questions SANS la bonne reponse ni l'explication (ne pas divulguer avant soumission)."""
    return [{"q": it["q"], "options": it["options"]} for it in QUIZZES[qid]["questions"]]


@app.get("/api/quiz/<qid>")
def get_quiz(qid):
    if qid not in QUIZZES:
        return jsonify(error="Quiz introuvable"), 404
    u, err = require_user()
    if err:
        return err
    prev = db().execute("SELECT * FROM attempts WHERE username=? AND quiz_id=?", (u, qid)).fetchone()
    if prev:
        # deja fait : on renvoie directement la correction, pas le quiz jouable
        return jsonify(done=True, result=_build_result(qid, eval_answers(prev["answers"]), int(prev["score"])))
    return jsonify(
        done=False,
        quiz={"id": qid, "title": QUIZZES[qid]["title"], "questions": _public_questions(qid)},
    )


def eval_answers(s):
    try:
        return [int(x) for x in s.split(",")] if s else []
    except ValueError:
        return []


def _build_result(qid, answers, score):
    total = len(QUIZZES[qid]["questions"])
    corrections = []
    for i, it in enumerate(QUIZZES[qid]["questions"]):
        your = answers[i] if i < len(answers) else -1
        corrections.append(
            {
                "q": it["q"],
                "options": it["options"],
                "your": your,
                "correct": it["answer"],
                "explain": it["explain"],
            }
        )
    return {"quiz_id": qid, "title": QUIZZES[qid]["title"], "score": score, "total": total, "corrections": corrections}


@app.post("/api/quiz/<qid>/submit")
def submit(qid):
    if qid not in QUIZZES:
        return jsonify(error="Quiz introuvable"), 404
    u, err = require_user()
    if err:
        return err
    data = request.get_json(silent=True) or {}
    answers = data.get("answers")
    n = len(QUIZZES[qid]["questions"])
    if not isinstance(answers, list) or len(answers) != n:
        return jsonify(error=f"Réponses invalides : {n} réponses attendues"), 400
    norm = []
    for a in answers:
        norm.append(int(a) if isinstance(a, int) and 0 <= a <= 3 else -1)
    score = sum(1 for i, it in enumerate(QUIZZES[qid]["questions"]) if norm[i] == it["answer"])
    try:
        db().execute(
            "INSERT INTO attempts(username, quiz_id, score, total, answers, created_at) VALUES(?,?,?,?,?,?)",
            (u, qid, score, n, ",".join(str(x) for x in norm), int(time.time())),
        )
        db().commit()
    except sqlite3.IntegrityError:
        return jsonify(error="Vous avez déjà passé ce quiz"), 409
    return jsonify(result=_build_result(qid, norm, score))


@app.get("/api/quiz/<qid>/leaderboard")
def leaderboard(qid):
    if qid not in QUIZZES:
        return jsonify(error="Quiz introuvable"), 404
    rows = db().execute(
        "SELECT username, score, total, created_at FROM attempts WHERE quiz_id=? "
        "ORDER BY score DESC, created_at ASC LIMIT 200",
        (qid,),
    ).fetchall()
    board = [
        {"rank": i + 1, "username": r["username"], "score": r["score"], "total": r["total"], "at": r["created_at"]}
        for i, r in enumerate(rows)
    ]
    return jsonify(quiz_id=qid, title=QUIZZES[qid]["title"], leaderboard=board)


# ---------- API : administration ----------
@app.get("/api/admin/data")
def admin_data():
    _, err = require_admin()
    if err:
        return err
    urows = db().execute(
        "SELECT username, is_admin, created_at FROM users ORDER BY created_at ASC"
    ).fetchall()
    arows = db().execute("SELECT username, quiz_id, score, total, created_at FROM attempts").fetchall()
    by_user = {}
    for a in arows:
        by_user.setdefault(a["username"], {})[a["quiz_id"]] = {
            "score": a["score"], "total": a["total"], "at": a["created_at"]
        }
    users = []
    for u in urows:
        if u["is_admin"]:
            continue  # on ne liste pas les comptes admin comme apprenants
        res = by_user.get(u["username"], {})
        users.append(
            {
                "username": u["username"],
                "created_at": u["created_at"],
                "results": res,
                "done_count": len(res),
                "total_score": sum(r["score"] for r in res.values()),
            }
        )
    quizzes = []
    for qid in QUIZ_ORDER:
        scores = [by_user[u].get(qid, {}).get("score") for u in by_user if qid in by_user.get(u, {})]
        scores = [s for s in scores if s is not None]
        quizzes.append(
            {
                "id": qid,
                "title": QUIZZES[qid]["title"],
                "count": len(QUIZZES[qid]["questions"]),
                "attempts": len(scores),
                "avg": round(sum(scores) / len(scores), 1) if scores else None,
            }
        )
    return jsonify(
        totals={"users": len(users), "attempts": len(arows)},
        quizzes=quizzes,
        order=QUIZ_ORDER,
        users=users,
    )


@app.post("/api/admin/reset")
def admin_reset():
    _, err = require_admin()
    if err:
        return err
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    quiz_id = (data.get("quiz_id") or "").strip()
    if not username:
        return jsonify(error="username requis"), 400
    if quiz_id == "all":
        db().execute("DELETE FROM attempts WHERE username=?", (username,))
    elif quiz_id in QUIZZES:
        db().execute("DELETE FROM attempts WHERE username=? AND quiz_id=?", (username, quiz_id))
    else:
        return jsonify(error="quiz_id invalide"), 400
    db().commit()
    return jsonify(ok=True)


@app.post("/api/admin/delete_user")
def admin_delete_user():
    admin, err = require_admin()
    if err:
        return err
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify(error="username requis"), 400
    target = db().execute("SELECT is_admin FROM users WHERE username=?", (username,)).fetchone()
    if not target:
        return jsonify(error="Utilisateur introuvable"), 404
    if target["is_admin"]:
        return jsonify(error="Impossible de supprimer un compte administrateur"), 400
    db().execute("DELETE FROM attempts WHERE username=?", (username,))
    db().execute("DELETE FROM users WHERE username=?", (username,))
    db().commit()
    return jsonify(ok=True)


@app.get("/api/admin/export.csv")
def admin_export():
    _, err = require_admin()
    if err:
        return err
    rows = db().execute(
        "SELECT username, quiz_id, score, total, created_at FROM attempts ORDER BY username, quiz_id"
    ).fetchall()
    import io, csv, datetime
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["username", "module", "titre", "score", "total", "date"])
    for r in rows:
        dt = datetime.datetime.fromtimestamp(r["created_at"]).strftime("%Y-%m-%d %H:%M")
        w.writerow([r["username"], r["quiz_id"], QUIZZES[r["quiz_id"]]["title"], r["score"], r["total"], dt])
    return (
        buf.getvalue(),
        200,
        {"Content-Type": "text/csv; charset=utf-8", "Content-Disposition": "attachment; filename=resultats-quiz.csv"},
    )


# ---------- frontend ----------
@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/healthz")
def healthz():
    return "ok"


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "9090")))
