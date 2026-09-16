# Quiz — Gestion de projet IA

Application de quiz conteneurisée pour la formation « Gestion de projet IA »
(support v1.0, 7 parties). 4 modules × 20 questions. Même socle que le quiz
« Conduite du changement » : comptes apprenants (username unique + mot de
passe), **une seule tentative par quiz**, classement par quiz, et correction
détaillée (score + bonnes réponses + explications) à la fin de chaque quiz.

## Modules

| Quiz | Contenu (parties du support) |
|---|---|
| m1 — Comprendre et cadrer un projet IA | Types de projets, échecs, CRISP-DM, rôles, AI Canvas, priorisation, build/buy, AI Act (parties 1–2) |
| m2 — Données et expérimentation (POC) | Data readiness, labellisation, gouvernance, POC, baseline, métriques ML et génératives (parties 3–4) |
| m3 — Industrialiser : MLOps et sécurité | POC → produit, CI/CD/CT, tests, menaces IA, monitoring et drift, outils (partie 5) |
| m4 — Piloter, déployer, exploiter | Jalons, backlog d'hypothèses, go/no-go, documentation, fournisseurs, FinOps, pilote (parties 6–7) |

## Fonctionnalités

- **Compte apprenant** : nom d'utilisateur unique + mot de passe (haché, jamais stocké en clair).
- **Une tentative par quiz et par utilisateur** : une fois soumis, le quiz n'est plus rejouable (il affiche la correction).
- **Classement par quiz** : tri par score puis par heure de passage (le plus rapide devant à score égal).
- **Correction** : à la fin, score sur 20 + pour chaque question la bonne réponse, votre réponse, et l'explication.
- **Qualité des questions** : 4 choix, 1 seul correct ; répartition équilibrée A/B/C/D (motif différent du quiz adoption) ; la bonne réponse n'est jamais la plus longue ; distracteurs plausibles du même registre que la bonne réponse (vérifié par `check_questions.py`).

## Espace administrateur

Identique au quiz adoption : tableau de bord (scores par module, statistiques,
réinitialisation d'une tentative, suppression d'un apprenant, export CSV).
Identifiants par défaut définis dans `docker-compose.yml` (`ADMIN_USER` /
`ADMIN_PASSWORD`) — **à changer avant mise en ligne**. Le mot de passe n'est
posé qu'à la première création du compte.

## Contenu

Les questions sont dans `questions.py` (banque `RAW`, une entrée par module).
Le vérificateur de contraintes :

```bash
python3 check_questions.py
```

## Déploiement sur un VPS OVH (port 9091)

Le service écoute en interne sur 9090 et est publié sur le **port 9091** de
l'hôte, pour cohabiter avec le quiz adoption (9090) sur le même VPS.

```bash
# 1. Copier le dossier sur le VPS
scp -r quiz-gestion-projet-ia/ ubuntu@VOTRE_VPS:/opt/quiz-gestion-projet-ia

# 2. Sur le VPS
cd /opt/quiz-gestion-projet-ia
docker compose up -d --build

# 3. Vérifier
docker compose ps
curl -s http://localhost:9091/healthz   # -> ok
```

Le quiz est alors accessible sur `http://VOTRE_VPS:9091`. Si `ufw` est actif :

```bash
sudo ufw allow 9091/tcp
```

### Persistance des données

Comptes et résultats sont stockés dans une base SQLite sur le volume Docker
`quiz-gp-data` (monté sur `/data`), distinct du volume du quiz adoption. Ils
survivent aux `docker compose restart` et `up -d --build`. Sauvegarde :

```bash
docker run --rm -v quiz-gestion-projet-ia_quiz-gp-data:/data -v "$PWD":/backup alpine \
  cp /data/quiz.db /backup/quiz-gp-backup-$(date +%F).db
```

### Mettre à jour les questions

Éditez `questions.py`, relancez `python3 check_questions.py`, puis :

```bash
docker compose up -d --build
```

> Attention : si vous modifiez l'ordre ou le nombre de questions d'un quiz **déjà
> passé** par des apprenants, leurs corrections enregistrées peuvent ne plus
> correspondre. Figez le contenu avant l'ouverture aux apprenants.

## Architecture

| Fichier | Rôle |
|---|---|
| `app.py` | API Flask (comptes, quiz, soumission, classement) + service du frontend |
| `questions.py` | Banque de questions + placement équilibré des bonnes réponses |
| `check_questions.py` | Vérifie les contraintes de conception des questions |
| `static/index.html` | Interface (page unique, sans dépendance externe) |
| `Dockerfile` | Image Python 3.12 + gunicorn (port interne 9090) |
| `docker-compose.yml` | Service `quiz` publié sur 9091 + volume `quiz-gp-data` |

Stack : Flask + SQLite (aucune base externe), servi par gunicorn (2 workers).
