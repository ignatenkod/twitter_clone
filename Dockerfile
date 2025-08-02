# Используем официальный образ Python
FROM python:3.10-slim-buster

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements /app/requirements

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements/production.txt && \
    pip install --no-cache-dir -r requirements/development.txt

# Копируем проект
COPY . /app

# Скрипт для запуска
COPY scripts/wait_for_db.py /app/scripts/

# Делаем скрипт исполняемым
RUN chmod +x /app/scripts/wait_for_db.py

# Порт, который будет слушать приложение
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.asgi:application"]
