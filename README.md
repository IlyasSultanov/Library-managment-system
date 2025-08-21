# Library Management System

Система управления библиотекой, построенная на FastAPI с использованием современной архитектуры и лучших практик разработки.

## 🏗️ Архитектура проекта

Проект следует принципам **Clean Architecture** и **Domain-Driven Design** с четким разделением слоев:

```
src/
├── api/                    # API слой (контроллеры)
│   └── v1/
│       └── api.py         # Основной роутер API v1
├── core/                   # Ядро приложения
│   └── config.py          # Конфигурация приложения
├── db/                     # Слой базы данных
│   ├── base.py            # Базовые импорты
│   ├── base_class.py      # Базовый класс модели
│   ├── database.py        # Настройки подключения к БД
│   └── __init__.py
├── endpoint/               # API endpoints
│   └── endpoint.py        # CRUD endpoints для книг
├── models/                 # Модели данных (SQLAlchemy)
│   └── model_book.py      # Модель книги
├── schemas/                # Pydantic схемы
│   └── book_schemas.py    # Схемы для валидации данных
├── service/                # Бизнес-логика
│   └── crud.py            # CRUD операции
├── jwt/                    # JWT токены
├── cearts/                 # Сертификаты
└── main.py                 # Точка входа приложения
```

### Слои архитектуры:

1. **API Layer** (`api/`, `endpoint/`) - обработка HTTP запросов
2. **Service Layer** (`service/`) - бизнес-логика и CRUD операции
3. **Data Layer** (`models/`, `db/`) - модели данных и работа с БД
4. **Schema Layer** (`schemas/`) - валидация и сериализация данных
5. **Core Layer** (`core/`) - конфигурация и общие утилиты

## 🚀 Технологический стек

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **Pydantic** - валидация данных и сериализация
- **PostgreSQL** - основная база данных
- **Docker & Docker Compose** - контейнеризация
- **Poetry** - управление зависимостями
- **JWT** - аутентификация и авторизация
- **Uvicorn** - ASGI сервер

## 📋 Требования

- Python 3.13+
- Docker & Docker Compose
- Poetry (для локальной разработки)

## 🛠️ Установка и запуск

### Вариант 1: С использованием Docker (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone <https://github.com/IlyasSultanov/Library-managment-system.git>
cd library_managment_system
```

2. **Создайте файл `.env` на основе примера:**
```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=library_db
POSTGRES_PORT=5432
URL=postgresql+asyncpg://postgres:password@db:5432/library_db

# Application
APP_PORT=8000
```

3. **Запустите приложение:**
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

### Вариант 2: Локальная разработка

1. **Установите Poetry:**
```bash
pip install poetry
```

2. **Установите зависимости:**
```bash
poetry install
```

3. **Активируйте виртуальное окружение:**
```bash
poetry shell
```

4. **Настройте базу данных PostgreSQL** и создайте файл `.env`

5. **Запустите приложение:**
```bash
python -m src.main
```

## 📚 API Endpoints

### Книги (Books)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/api/books/` | Создать новую книгу |
| `GET` | `/api/books/` | Получить список книг |
| `GET` | `/api/books/{book_id}` | Получить книгу по ID |
| `PATCH` | `/api/books/{book_id}` | Обновить книгу |
| `DELETE` | `/api/books/{book_id}` | Удалить книгу (soft delete) |

### Примеры запросов

#### Создание книги
```bash
curl -X POST "http://localhost:8000/api/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Война и мир",
    "description": "Роман-эпопея Льва Толстого"
  }'
```

#### Получение списка книг
```bash
curl "http://localhost:8000/api/books/?skip=0&limit=10&search=война"
```

#### Обновление книги
```bash
curl -X PATCH "http://localhost:8000/api/books/{book_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Война и мир (обновленное издание)"
  }'
```

## 🗄️ Модель данных

### Book (Книга)
```python
class Book(BaseModel):
    id: UUID (Primary Key)
    name: str (Название книги)
    description: str (Описание)
    created_at: datetime (Дата создания)
    updated_at: datetime (Дата обновления)
    deleted_at: datetime (Дата удаления, nullable)
```

## 🔧 Конфигурация

Основные настройки находятся в `src/core/config.py`:

- **База данных**: URL подключения к PostgreSQL
- **JWT**: Настройки аутентификации
- **CORS**: Настройки для кросс-доменных запросов

## 🧪 Разработка

### Структура для добавления новых сущностей

1. **Создайте модель** в `src/models/`
2. **Создайте схемы** в `src/schemas/`
3. **Добавьте CRUD операции** в `src/service/`
4. **Создайте endpoints** в `src/endpoint/`
5. **Подключите роутер** в `src/api/v1/api.py`

### Пример добавления новой сущности "Author":

```python
# src/models/model_author.py
class Author(BaseModel):
    __tablename__ = "authors"
    name: Mapped[str] = mapped_column(nullable=False)
    biography: Mapped[str] = mapped_column(nullable=True)

# src/schemas/author_schemas.py
class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    biography: Optional[str] = None

# src/service/crud_author.py
class CRUDAuthor:
    # CRUD операции...

# src/endpoint/author_endpoint.py
router = APIRouter(prefix="/authors", tags=["authors"])
# Endpoints...
```

## 🐳 Docker

### Сборка образа
```bash
docker build -t library-management-system .
```

### Запуск с Docker Compose
```bash
docker-compose up -d
```

### Просмотр логов
```bash
docker-compose logs -f app
```

## 📝 Документация API

После запуска приложения автоматически генерируется интерактивная документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Безопасность

- **Soft Delete**: Реализовано мягкое удаление записей
- **Валидация данных**: Используется Pydantic для валидации
- **CORS**: Настроен для работы с фронтендом
- **JWT**: Подготовлена инфраструктура для аутентификации

## 🚀 Производительность

- **Асинхронность**: Все операции с БД асинхронные
- **Connection Pooling**: Настроен пул соединений с БД
- **Пагинация**: Поддержка пагинации для больших списков
- **Поиск**: Реализован поиск по названию книги

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 👨‍💻 Автор

SultanovIlyas0@gmail.com

---

**Примечание**: Это базовая версия системы управления библиотекой. Для продакшена рекомендуется добавить аутентификацию, авторизацию, логирование и дополнительные функции управления библиотекой.
