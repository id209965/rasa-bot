#!/bin/bash

# Запуск Rasa локально (альтернатива Docker)

set -e

echo "🐍 Локальный запуск Rasa"
echo "======================="
echo ""

# Проверяем, что файлы Rasa существуют
if [ ! -f "app/rasa/domain.yml" ]; then
    echo "❌ Файл app/rasa/domain.yml не найден!"
    echo "Убедитесь, что вы запускаете скрипт из корня проекта."
    exit 1
fi

echo "✅ Найдены файлы конфигурации Rasa"
echo ""

# Создаем символическую ссылку на данные в директории rasa
if [ ! -L "app/rasa/data" ]; then
    ln -sf "$(pwd)/data" "app/rasa/data"
fi

# Переходим в директорию Rasa
cd app/rasa

# Проверяем установку Rasa
if ! command -v rasa &> /dev/null; then
    echo "⬇️ Rasa не найден. Устанавливаем..."
    pip install rasa==3.6.13
fi

echo "📦 Шаг 1: Обучение модели Rasa..."
echo "Это может занять несколько минут..."

# Обучаем модель
rasa train --domain domain.yml --data data/ --config config.yml

if [ $? -eq 0 ]; then
    echo "✅ Модель успешно обучена!"
else
    echo "❌ Ошибка обучения модели"
    exit 1
fi

echo ""
echo "🚀 Шаг 2: Запуск Rasa сервера..."
echo "Сервер будет доступен на http://localhost:5005"
echo "Для остановки нажмите Ctrl+C"
echo ""

# Запускаем сервер
export RASA_TELEMETRY_ENABLED=false
rasa run --enable-api --cors '*' --debug --port 5005
