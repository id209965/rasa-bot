# ⚠️ ВАЖНО: Решение проблемы с зависимостями Rasa

Rasa имеет строгие ограничения на версии пакетов, что может вызывать конфликты.

## 🔧 Быстрое решение

**Вариант 1 (Рекомендуется): Установка без Rasa**
```bash
pip install -r requirements-minimal.txt
```
Это даст вам все основные функции бота без NLP.

**Вариант 2: Установка с Rasa (экспериментально)**
```bash
# Сначала установить Rasa и его зависимости
pip install -r requirements-rasa.txt
# Затем остальные пакеты
pip install -r requirements-minimal.txt
```

---

# 🚀 Инструкция по установке Test Bot

## 📦 Варианты файлов зависимостей

- **`requirements.txt`** - Полный набор зависимостей (включая Rasa)
- **`requirements-minimal.txt`** - Минимальные зависимости для быстрого старта
- **`requirements-dev.txt`** - Для разработки (инструменты тестирования и отладки)
- **`requirements-prod.txt`** - Оптимизированные для продакшена

## 🎯 Автоматическая установка (рекомендуется)

### Linux/macOS:
```bash
git clone <repository-url>
cd test-bot
./install.sh
```

### Windows:
```cmd
git clone <repository-url>
cd test-bot
install.bat
```

Скрипт автоматически:
- Создаст виртуальное окружение
- Предложит выбор типа установки:
  1. **Полная** - все функции включая Rasa NLP
  2. **Минимальная** - быстрый старт без Rasa
  3. **Разработка** - с инструментами разработчика
- Установит зависимости
- Создаст .env файл

## 🔧 Ручная установка

### Минимальная установка (без Rasa):
```bash
# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate.bat  # Windows

# Установить минимальные зависимости
pip install -r requirements-minimal.txt

# Настроить окружение
cp .env.example .env
# Отредактируйте .env файл

# Инициализация базы данных
python manage.py init-db

# Запуск
python main.py
```

### Полная установка (с Rasa):
```bash
# Установка всех зависимостей
pip install -r requirements.txt

# Обучение Rasa модели
cd app/rasa
rasa train
cd ../..

# Запуск с Rasa (в отдельных терминалах)
python manage.py rasa &  # запустить Rasa
python main.py           # запустить бот
```

## 🐳 Docker установка

```bash
# Создать .env файл
cp .env.example .env
# Отредактировать .env с вашими ключами

# Запустить с Docker Compose
docker-compose up -d
```

## ⚙️ Настройка .env файла

Обязательные переменные:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
API_SECRET_KEY=your_secret_key_here
```

Опциональные:
```env
YANDEX_MAPS_API_KEY=your_yandex_maps_api_key_here
ADMIN_PHONES=+1234567890,+0987654321
DATABASE_URL=sqlite+aiosqlite:///./test_bot.db
```

## 🎯 Выбор типа установки

1. **Минимальная** - Быстро попробовать бота без NLP функций
   - Время установки: 2-3 минуты
   - Размер: ~200MB
   - Функции: Основной бот, API, база данных

2. **Полная** - Все функции включая Rasa NLP
   - Время установки: 15-20 минут
   - Размер: ~3GB
   - Функции: Все + интеллектуальные диалоги

3. **Разработка** - Для вклада в проект
   - Включает инструменты тестирования и отладки
   - pre-commit hooks, linters, formatters

## 🚀 Быстрый старт после установки

1. Отредактируйте `.env` файл с вашими ключами
2. Инициализируйте базу данных: `python manage.py init-db`
3. (Опционально) Создайте админа: `python manage.py create-admin`
4. Запустите бот: `python main.py`

## ❓ Устранение неполадок

### Проблемы с установкой Rasa:
```bash
# Используйте минимальную установку
pip install -r requirements-minimal.txt
```

### Ошибки с базой данных:
```bash
# Пересоздать базу данных
rm -f *.db
python manage.py init-db
```

### Проблемы с виртуальным окружением:
```bash
# Пересоздать окружение
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```
