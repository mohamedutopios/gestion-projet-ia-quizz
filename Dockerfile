FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    QUIZ_DB=/data/quiz.db \
    PORT=9090

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py questions.py ./
COPY static ./static

# Repertoire de persistance de la base (monte en volume)
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 9090

# 2 workers x 4 threads = jusqu'a 8 requetes traitees en parallele.
# Les requetes du quiz sont courtes ; SQLite en WAL + busy_timeout gere les ecritures concurrentes.
CMD ["gunicorn", "--bind", "0.0.0.0:9090", "--workers", "2", "--threads", "4", "--timeout", "60", "app:app"]
