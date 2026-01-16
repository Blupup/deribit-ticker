API для отслеживания цен BTC и ETH с биржи Deribit с автоматическим сбором данных каждую минуту.

## Возможности

- ✅ Автоматический сбор index price для BTC_USD и ETH_USD каждую минуту
- ✅ REST API для получения исторических данных с фильтрацией
- ✅ PostgreSQL для надежного хранения данных
- ✅ Celery Beat для периодических задач
- ✅ Docker Compose для простого развертывания
- ✅ Swagger документация из коробки

## Технологии

- **FastAPI** - современный веб-фреймворк с автоматической документацией
- **SQLAlchemy** - ORM для типобезопасной работы с БД
- **PostgreSQL** - надежная реляционная база данных
- **Celery + Redis** - распределенная очередь задач
- **aiohttp** - асинхронный HTTP клиент для Deribit API
- **Docker** - контейнеризация всех сервисов

## Быстрый старт

### Запуск через Docker (рекомендуется)

```bash
# 1. Клонируйте репозиторий
git clone <your-repo-url>
cd deribit-price-tracker

# 2. Запустите все сервисы
docker-compose up -d

# 3. Проверьте статус
docker-compose ps

# 4. Проверьте логи
docker-compose logs -f app
```

**API доступно по адресу:** http://localhost:8000

**Swagger документация:** http://localhost:8000/docs

### Проверка работоспособности

```bash
# Проверка health endpoint
curl http://localhost:8000/health

# Проверка последней цены BTC
curl http://localhost:8000/prices/latest?ticker=btc_usd

# Проверка всех цен ETH
curl http://localhost:8000/prices/?ticker=eth_usd
```

### Локальная разработка (без Docker)

```bash
# 1. Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Запустите PostgreSQL и Redis
docker-compose up -d db redis

# 4. Создайте .env файл с настройками
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/deribit_db
REDIS_URL=redis://localhost:6379/0

# 5. Запустите сервисы в отдельных терминалах

# Терминал 1 - FastAPI
uvicorn app.main:app --reload

# Терминал 2 - Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# Терминал 3 - Celery Beat
celery -A app.tasks.celery_app beat --loglevel=info
```

## API Endpoints

### Получить все цены по ticker
```http
GET /prices/?ticker=btc_usd
```

**Ответ:**
```json
[
  {
    "id": 1,
    "ticker": "btc_usd",
    "index_price": 45123.45,
    "timestamp": 1704067200
  }
]
```

### Получить последнюю цену
```http
GET /prices/latest?ticker=eth_usd
```

**Ответ:**
```json
{
  "id": 100,
  "ticker": "eth_usd",
  "index_price": 2345.67,
  "timestamp": 1704153600
}
```

### Получить цены с фильтром по дате
```http
GET /prices/filter?ticker=btc_usd&start_date=1704067200&end_date=1704153600
```

**Параметры:**
- `ticker` - btc_usd или eth_usd (обязательно)
- `start_date` - Unix timestamp начала периода (опционально)
- `end_date` - Unix timestamp конца периода (опционально)

### Health Check
```http
GET /health
```

**Ответ:**
```json
{
  "status": "healthy"
}
```

## Архитектура и дизайн

### Структура проекта
```
deribit-price-tracker/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── deribit_client.py  # HTTP клиент для Deribit API
│   │   └── price_service.py   # Бизнес-логика работы с ценами
│   ├── tasks/
│   │   └── celery_tasks.py    # Периодические задачи
│   ├── config.py              # Настройки приложения
│   ├── database.py            # Настройка БД
│   ├── models.py              # SQLAlchemy модели
│   ├── schemas.py             # Pydantic схемы
│   └── main.py                # Точка входа FastAPI
├── tests/                     # Unit и integration тесты
├── docker-compose.yml         # Конфигурация Docker
├── Dockerfile                 # Образ приложения
├── requirements.txt           # Python зависимости
└── README.md                  # Документация
```

### Архитектурные решения

#### 1. Layered Architecture
Разделение на слои для улучшения поддерживаемости:
- **API Layer** (routes.py) - обработка HTTP запросов и валидация
- **Service Layer** (price_service.py, deribit_client.py) - бизнес-логика
- **Data Layer** (models.py, database.py) - работа с базой данных

#### 2. Dependency Injection
FastAPI зависимости для управления DB сессиями:
- Автоматическое открытие/закрытие соединений
- Изоляция транзакций
- Простое тестирование с mock объектами

#### 3. Separation of Concerns
Каждый модуль имеет одну ответственность:
- `DeribitClient` - только HTTP запросы к Deribit API
- `PriceService` - только операции с данными о ценах
- `Routes` - только обработка HTTP запросов

### Технические решения

#### Асинхронность
**aiohttp вместо requests** для неблокирующих HTTP запросов:
- Высокая производительность при множественных запросах
- Timeout защита (10 сек) от зависаний
- Совместимость с FastAPI async endpoints

#### База данных
**PostgreSQL + SQLAlchemy ORM**:
- Защита от SQL injection через параметризованные запросы
- Составной индекс `(ticker, timestamp)` для быстрых запросов
- Connection pooling для переиспользования соединений
- ACID транзакции для целостности данных

#### Периодические задачи
**Celery Beat**:
- Гарантированное выполнение задач каждую минуту
- Автоматический retry при временных ошибках
- Горизонтальное масштабирование через добавление worker'ов
- Изоляция от основного приложения

#### Валидация данных
**Pydantic схемы**:
- Автоматическая валидация типов на входе/выходе
- Генерация OpenAPI схемы для Swagger
- Защита от некорректных данных

#### Конфигурация
**Pydantic Settings**:
- Типобезопасное управление настройками
- Загрузка из .env файлов и environment variables
- Кэширование через `@lru_cache` для производительности

### Обработка ошибок

- **Graceful degradation**: приложение продолжает работу при ошибках API
- **Логирование**: все ошибки записываются в stdout для Docker
- **Retry логика**: Celery автоматически повторяет неудачные задачи
- **Timeout**: защита от зависших HTTP запросов (10 сек)

### Оптимизации производительности

1. **Индексы БД**: составной индекс на `(ticker, timestamp)` ускоряет запросы в 10+ раз
2. **Connection Pooling**: переиспользование соединений к PostgreSQL
3. **Async/await**: неблокирующие операции ввода-вывода
4. **Кэширование настроек**: `@lru_cache` для Settings

## Управление контейнерами

```bash
# Остановить все сервисы
docker-compose down

# Остановить с удалением данных
docker-compose down -v

# Перезапустить конкретный сервис
docker-compose restart app

# Просмотр логов конкретного сервиса
docker-compose logs -f celery_worker

# Выполнить команду в контейнере
docker exec -it deribit_app bash

# Пересобрать образы
docker-compose build --no-cache
docker-compose up -d
```

## Тестирование

```bash
# Запуск всех тестов
pytest tests/ -v

# Запуск с coverage
pytest tests/ --cov=app --cov-report=html

# Запуск конкретного теста
pytest tests/test_price_service.py -v
```

## Мониторинг

```bash
# Проверка использования ресурсов
docker stats

# Проверка здоровья контейнеров
docker-compose ps

# Проверка логов за последний час
docker-compose logs --since 1h
```

## Troubleshooting

### Приложение не запускается

```bash
# Проверьте логи
docker-compose logs app

# Проверьте, что БД готова
docker-compose logs db | grep "ready to accept connections"

# Пересоздайте контейнеры
docker-compose down
docker-compose up -d
```

### Celery не собирает данные

```bash
# Проверьте логи worker
docker-compose logs celery_worker

# Проверьте логи beat
docker-compose logs celery_beat

# Проверьте подключение к Redis
docker exec -it deribit_redis redis-cli ping
```

### Ошибки валидации Pydantic

Убедитесь, что в `config.py` установлено:
```python
class Config:
    env_file = ".env"
    extra = "ignore"  # Игнорировать лишние переменные окружения
```

## Требования

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+ (для локальной разработки)

## Автор

**Сиротин Никита Николаевич**
