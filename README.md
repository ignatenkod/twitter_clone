# Mini Twitter на Django + WebSockets

## Описание проекта

Mini Twitter - это упрощенный аналог Twitter с основными функциями микроблогинга, реализованный на Django с использованием WebSockets для работы в реальном времени.

**Ключевые возможности**:
- Создание и публикация постов
- Система подписок на других пользователей
- Лента постов от пользователей из подписок
- Лайки и комментарии к постам
- Уведомления в реальном времени через WebSockets
- Фоновые задачи с использованием Celery

## Технологический стек

**Backend**:
- Python 3.10+
- Django 4.2
- Django Channels (WebSockets)
- Celery (фоновые задачи)
- PostgreSQL (основная БД)
- Redis (кеш и брокер сообщений)

**Frontend**:
- HTMX (динамический интерфейс без сложного JS)
- Bootstrap 5 (стилизация)
- Jinja2 (шаблонизация)

**Инфраструктура**:
- Docker (контейнеризация)
- Nginx (веб-сервер)
- Gunicorn (ASGI сервер)
- Daphne (WebSocket сервер)

## Установка и запуск

### Требования
- Docker и Docker Compose
- Python 3.10+ (для локальной разработки)

### Запуск с Docker
1. Скопируйте файл `.env.example` в `.env` и настройте переменные окружения:
   ```bash
   cp .env.example .env
   ```
2. Запустите сервисы:
   ```bash
   docker-compose up -d --build
   ```
3. Применение миграций:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
4. Сбор статических файлов:
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

### Локальная разработка (без Docker)
1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements/development.txt
   ```
3. Настройте базу данных PostgreSQL и Redis
4. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
5. Для WebSockets запустите:
   ```bash
   daphne config.asgi:application -p 8001
   ```
6. Для Celery запустите:
   ```bash
   celery -A config worker --loglevel=info
   ```

## Структура проекта

```
mini_twitter/
├── apps/               # Основные приложения
│   ├── core/           # Базовые компоненты
│   ├── posts/          # Посты, лайки, комментарии
│   ├── users/          # Пользователи и подписки
│   └── notifications/  # Система уведомлений
├── config/             # Настройки проекта
├── static/             # Статические файлы
├── templates/          # Шаблоны
└── tests/              # Тесты
```

## Основные API эндпоинты

- `GET /` - Лента постов
- `POST /posts/create/` - Создание поста
- `POST /posts/<pk>/like/` - Лайк поста
- `POST /users/<username>/subscribe/` - Подписка на пользователя
- `GET /notifications/` - Список уведомлений
- `WS /ws/notifications/` - WebSocket для уведомлений

## Лицензия

MIT License. Смотрите файл [LICENSE](LICENSE) для подробной информации.
