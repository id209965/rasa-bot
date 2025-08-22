# 🧠 Установка Rasa в отдельном окружении

Из-за конфликтов зависимостей между Rasa и современными версиями aiogram/FastAPI, рекомендуется запускать Rasa в отдельном виртуальном окружении.

## Вариант 1: Два отдельных окружения

### Шаг 1: Установите основной бот
```bash
# Основное окружение для бота
python3 -m venv venv-bot
source venv-bot/bin/activate
pip install -r requirements.txt  # Без Rasa
cp .env.example .env
# Настройте .env файл
python manage.py init-db
```

### Шаг 2: Установите Rasa отдельно
```bash
# Отдельное окружение для Rasa
python3 -m venv venv-rasa
source venv-rasa/bin/activate
pip install rasa==3.6.13 rasa-sdk==3.6.2

# Обучите модель
cd app/rasa
rasa train
```

### Шаг 3: Запустите оба сервиса
```bash
# Терминал 1: Rasa сервер
source venv-rasa/bin/activate
cd app/rasa
rasa run --enable-api --cors "*" --port 5005

# Терминал 2: Основной бот
source venv-bot/bin/activate
python main.py
```

## Вариант 2: Docker для Rasa

### docker-compose-rasa.yml
```yaml
version: '3.8'

services:
  bot:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app/static:/app/app/static
      - ./data:/app/data
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DATABASE_URL=sqlite+aiosqlite:///./data/test_bot.db
      - RASA_SERVER_URL=http://rasa:5005
    depends_on:
      - rasa

  rasa:
    image: rasa/rasa:3.6.13
    ports:
      - "5005:5005"
    volumes:
      - ./app/rasa:/app
    command: >
      bash -c "rasa train --domain domain.yml --data data/ --config config.yml &&
               rasa run --enable-api --cors '*'"
```

### Запуск с Docker
```bash
docker-compose -f docker-compose-rasa.yml up -d
```

## Вариант 3: Без Rasa (рекомендуется)

Просто используйте основной функционал без NLP:

```bash
pip install -r requirements.txt
python main.py
```

Все функции бота работают, кроме умных диалогов. Бот использует простые текстовые команды.

## Что работает без Rasa:

✅ Регистрация пользователей  
✅ Создание и редактирование профиля  
✅ Создание мероприятий  
✅ Поиск и добавление друзей  
✅ Участие в мероприятиях  
✅ Админ панель  
✅ Загрузка файлов  
✅ Яндекс.Карты интеграция  
✅ Экспорт отчетов  

❌ Умные диалоги и NLP обработка сообщений

## Заключение

Для большинства случаев использования **рекомендуется работать без Rasa**. Функционал бота практически полный, а установка и поддержка намного проще.

Rasa можно добавить позже как отдельный микросервис, если понадобятся продвинутые диалоговые функции.
