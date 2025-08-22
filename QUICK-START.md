# 🚀 Быстрый старт Test Bot

## ⚡ МГНОВЕННОЕ РЕШЕНИЕ ПРОБЛЕМЫ

Если у вас ошибки с зависимостями Rasa:

```bash
# Просто запустите это:
./quick-install.sh
```

Это установит бота без Rasa, но со всеми основными функциями!

---

## Ручная установка (если скрипт не работает)

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 2. Обновить pip
pip install --upgrade pip

# 3. Установить рабочие зависимости
pip install -r requirements-working.txt

# 4. Настроить конфигурацию
cp .env.example .env
# Отредактируйте .env с вашим бот токеном

# 5. Инициализировать базу данных
python manage.py init-db

# 6. Запустить бота
python main.py
```

## Если и это не работает

```bash
# Минимальная установка только основных пакетов:
pip install fastapi aiogram sqlalchemy aiosqlite uvicorn python-multipart python-dotenv
```

## Как получить Telegram Bot Token

1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте: `/newbot`
4. Следуйте инструкциям
5. Скопируйте токен в .env файл

## Пример .env файла

```env
TELEGRAM_BOT_TOKEN=1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
API_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite+aiosqlite:///./test_bot.db
ADMIN_PHONES=+1234567890
```

## Что работает без Rasa

✅ Регистрация пользователей  
✅ Профиль пользователя  
✅ Создание мероприятий  
✅ Поиск друзей  
✅ Меню бота  
✅ Админ панель  
✅ Загрузка файлов  
✅ Яндекс.Карты API  

❌ Умные диалоги (Rasa NLP)

## Как добавить Rasa потом

Если хотите добавить NLP потом:

```bash
# Осторожно! Это может сломать существующую установку
pip install -r requirements-with-rasa.txt
```

## Помощь

Если что-то не работает:

1. Прочитайте `TROUBLESHOOTING.md`
2. Проверьте Python версию: `python3 --version` (нужно 3.8+)
3. Проверьте .env файл
4. Попробуйте пересоздать venv: `rm -rf venv && python3 -m venv venv`

**Главное: quick-install.sh должен работать!** 🚀
