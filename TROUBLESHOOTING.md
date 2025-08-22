# 🔧 Устранение неполадок Test Bot

## ⚠️ Основные проблемы

### 1. Ошибка конфликта зависимостей Rasa

**Проблема:**
```
ERROR: Cannot install -r requirements.txt because these package versions have conflicting dependencies.
The conflict is caused by:
    rasa 3.6.13 depends on SQLAlchemy<1.5.0 and >=1.4.0
    sqlalchemy==2.0.23
```

**🔧 Решение:**
```bash
# Вариант 1: Установка без Rasa (рекомендуется)
pip install -r requirements-minimal.txt

# Вариант 2: Поэтапная установка с Rasa
pip install rasa==3.6.13
pip install -r requirements-minimal.txt

# Вариант 3: Использовать фиксированный скрипт
./install-fixed.sh
```

### 2. Python версия не подходит

**Проблема:**
```
ERROR: This package requires Python >=3.8
```

**🔧 Решение:**
```bash
# Проверить версию Python
python3 --version

# Если меньше 3.8, обновите Python
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.10

# macOS:
brew install python@3.10

# Или скачайте с https://python.org
```

### 3. Ошибки с базой данных

**Проблема:**
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table
```

**🔧 Решение:**
```bash
# Инициализировать базу данных
python manage.py init-db

# Если не помогает, удалить старую БД
rm -f *.db data/*.db
python manage.py init-db
```

### 4. Ошибка с Telegram токеном

**Проблема:**
```
TelegramUnauthorizedError: 401: Unauthorized
```

**🔧 Решение:**
```bash
# Проверить .env файл
cat .env | grep TELEGRAM_BOT_TOKEN

# Должно быть:
TELEGRAM_BOT_TOKEN=1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Получить новый токен от @BotFather в Telegram
```

### 5. Проблемы с виртуальным окружением

**Проблема:**
Пакеты устанавливаются глобально или конфликтуют

**🔧 Решение:**
```bash
# Пересоздать виртуальное окружение
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate.bat  # Windows

# Проверить, что окружение активно
which python
# Должно показывать путь к venv/bin/python
```

### 6. Порт 8000 уже занят

**Проблема:**
```
OSError: [Errno 48] Address already in use
```

**🔧 Решение:**
```bash
# Найти процесс, использующий порт 8000
lsof -i :8000

# Убить процесс
kill -9 <PID>

# Или изменить порт в .env
API_PORT=8001
```

### 7. Rasa сервер не запускается

**Проблема:** NLP функции не работают

**🔧 Решение:**
```bash
# Проверить, установлен Rasa
rasa --version

# Обучить модель
cd app/rasa
rasa train

# Запустить сервер
rasa run --enable-api --cors "*" --port 5005

# Или использовать без Rasa
# (бот будет работать, но без умных диалогов)
```

## 🔍 Диагностика

### Проверка системы
```bash
# Проверить Python и pip
python3 --version
pip --version

# Проверить установленные пакеты
pip list | grep -E "(fastapi|aiogram|sqlalchemy|rasa)"

# Проверить конфигурацию
cat .env
ls -la *.db
```

### Тестирование компонентов
```bash
# Тест API
curl http://localhost:8000/health

# Тест базы данных
python -c "from app.database.connection import init_database; import asyncio; asyncio.run(init_database())"

# Тест Rasa (если установлен)
curl http://localhost:5005/status
```

## 📞 Получить помощь

Если проблема не решается:

1. Проверьте логи приложения
2. Опишите проблему с полным текстом ошибки
3. Укажите вашу операционную систему и версию Python
4. Покажите вывод команд диагностики

## 🔄 Полная переустановка

Если ничего не помогает:

```bash
# Очистить всё
rm -rf venv
rm -f *.db data/*.db
rm -f .env

# Начать сначала
./install-fixed.sh  # или install.sh
```

**Помните:** Минимальная установка работает стабильно и быстро!
