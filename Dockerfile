FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# SQLite-файл по умолчанию пишется в /app. Для сохранности данных
# смонтируй том на /app/data и укажи DB_URL=sqlite+aiosqlite:///data/database.db
CMD ["python", "main.py"]
