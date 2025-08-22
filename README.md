# Чат-бот "Тест" 🤖

Чат-бот для Telegram, предназначенный для организации мероприятий, поиска участников и общения между пользователями.

## 🚀 Особенности

- **FastAPI** + **aiogram** для высокопроизводительного API и Telegram бота
- **SQLAlchemy** с поддержкой SQLite и PostgreSQL
- **Rasa** для интеллектуального общения и обработки естественного языка
- **Яндекс.Карты API** для отображения местоположений
- Админ панель для управления данными
- Собственное хранилище изображений
- Docker поддержка для простого развертывания

## 📋 Функционал

### Пользователи
- 👤 Регистрация и управление профилем
- 👥 Поиск друзей по интересам
- 💬 Общение между пользователями
- 🎉 Создание и участие в мероприятиях
- 🗺️ Просмотр местоположений на карте

### Администраторы
- 📊 Загрузка данных через Excel файлы
- 📈 Экспорт отчетов по пользователям и мероприятиям
- ⚙️ Управление системными данными

## 🛠️ Технический стек

- **Python 3.12**
- **FastAPI** - веб API
- **aiogram 3.x** - Telegram Bot API
- **SQLAlchemy** - ORM для работы с БД
- **Rasa** - обработка естественного языка
- **Alembic** - миграции базы данных
- **Docker** - контейнеризация
- **PostgreSQL/SQLite** - база данных
- **Redis** - кеширование

## 🏗️ Структура проекта

```
app/
├── api/                  # FastAPI приложение
│   ├── routes/          # API роуты
│   └── main.py         # Главный файл API
├── bot/                 # Telegram бот
│   ├── handlers/       # Обработчики сообщений
│   ├── keyboards/      # Клавиатуры
│   ├── middlewares/    # Middleware
│   └── states/         # FSM состояния
├── database/           # База данных
│   └── models/        # SQLAlchemy модели
├── rasa/              # Rasa конфигурация
│   ├── data/         # Обучающие данные
│   └── domain/       # Доменные файлы
└── static/           # Статические файлы
    ├── photos/       # Фотографии пользователей
    └── uploads/      # Загруженные файлы
```

## 🚀 Быстрый старт

### Используя Docker (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd test-bot
```

2. **Создайте файл .env:**
```bash
cp .env.example .env
```

3. **Настройте переменные окружения в .env:**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
API_SECRET_KEY=your_secret_key_here
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key_here
ADMIN_PHONES=+1234567890,+0987654321
```

4. **Запустите приложение:**
```bash
docker-compose up -d
```

### Локальная установка

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

2. **Настройте переменные окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл
```

3. **Запустите Rasa сервер (в отдельном терминале):**
```bash
cd app/rasa
rasa train
rasa run --enable-api --cors "*" --port 5005
```

4. **Запустите приложение:**
```bash
python main.py
```

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | Обязательно |
|-----------|----------|------------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | ✅ |
| `API_SECRET_KEY` | Секретный ключ для API | ✅ |
| `DATABASE_URL` | URL базы данных | ❌ |
| `YANDEX_MAPS_API_KEY` | Ключ API Яндекс.Карт | ❌ |
| `ADMIN_PHONES` | Телефоны администраторов | ❌ |
| `RASA_SERVER_URL` | URL Rasa сервера | ❌ |

### База данных

**SQLite (по умолчанию):**
```env
DATABASE_URL=sqlite+aiosqlite:///./test_bot.db
```

**PostgreSQL:**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/test_bot
```

## 📖 API Документация

После запуска приложения API документация доступна по адресу:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные эндпоинты:

- `POST /api/files/upload-photo` - Загрузка фотографий
- `GET /api/admin/export-users` - Экспорт пользователей
- `GET /api/admin/export-events` - Экспорт мероприятий
- `POST /api/admin/upload-data` - Загрузка данных
- `GET /api/maps/geocode` - Геокодирование адресов

## 🎯 Использование

### Регистрация пользователя
1. Найдите бота в Telegram
2. Отправьте команду `/start`
3. Следуйте инструкциям для регистрации
4. Заполните профиль (имя, возраст, регион, интересы)

### Администрирование
1. Убедитесь, что ваш номер телефона указан в `ADMIN_PHONES`
2. В боте выберите "⚙️ Админ панель"
3. Используйте доступные функции:
   - Загрузка данных (Excel файлы с регионами и интересами)
   - Экспорт отчетов

### Формат Excel файлов для загрузки

Файл должен содержать колонки:
- `regions` - список регионов
- `interests` - список интересов

Пример:
| regions | interests |
|---------|----------|
| Москва | Спорт |
| Санкт-Петербург | Музыка |
| Казань | Программирование |

## 🔧 Разработка

### Структура обработчиков
```python
# app/bot/handlers/example.py
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Пример")
async def example_handler(message: Message, user: User, session: AsyncSession):
    await message.answer("Ответ")
```

### Добавление новых моделей
```python
# app/database/models/example.py
from sqlalchemy import Column, Integer, String
from .base import Base

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
```

### Миграции базы данных
```bash
# Создание миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head
```

## 📝 Логирование

Логи приложения выводятся в консоль. Для production рекомендуется настроить логирование в файлы.

## 🛡️ Безопасность

- Используйте сильные пароли для базы данных
- Храните секретные ключи в переменных окружения
- Ограничьте доступ к админским функциям по номерам телефонов
- Регулярно обновляйте зависимости

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Отправьте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле LICENSE.

## 📞 Поддержка

Если у вас есть вопросы или предложения:
- Создайте Issue в GitHub
- Обратитесь к документации API
- Проверьте логи приложения

---

**Автор**: Создано с помощью AI Assistant  
**Версия**: 1.0.0  
**Обновлено**: 2024
