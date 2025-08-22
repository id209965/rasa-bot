#!/bin/bash

# Пошаговый запуск Rasa в Docker

set -e

echo "🐳 Rasa Docker Setup"
echo "==================="
echo ""

# Проверяем, что файлы Rasa существуют
if [ ! -f "app/rasa/domain.yml" ]; then
    echo "❌ Файл app/rasa/domain.yml не найден!"
    echo "Убедитесь, что вы запускаете скрипт из корня проекта."
    exit 1
fi

echo "✅ Найдены файлы конфигурации Rasa"
echo ""

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие Rasa контейнеры..."
docker-compose -f docker-compose-rasa-only.yml down 2>/dev/null || true
docker-compose -f docker-compose-rasa-fixed.yml down 2>/dev/null || true

# Создаем директорию для моделей, если не существует
mkdir -p app/rasa/models

echo "📦 Шаг 1: Обучение модели Rasa..."
echo "Это может занять несколько минут..."

# Обучаем модель в отдельном контейнере
docker run --rm \
  -v "$(pwd)/app/rasa:/app" \
  -v "$(pwd)/data:/app/data" \
  -w /app \
  rasa/rasa:3.6.13-full \
  rasa train --domain domain.yml --data data/ --config config.yml

if [ $? -eq 0 ]; then
    echo "✅ Модель успешно обучена!"
else
    echo "❌ Ошибка обучения модели"
    exit 1
fi

echo ""
echo "🚀 Шаг 2: Запуск Rasa сервера..."

# Запускаем сервер с обученной моделью
docker-compose -f docker-compose-rasa-fixed.yml up -d

echo ""
echo "⏳ Ожидание запуска сервера..."
sleep 5

# Проверяем статус
echo "🔍 Проверка статуса Rasa..."

for i in {1..12}; do
    if curl -s http://localhost:5005/status > /dev/null; then
        echo "✅ Rasa сервер запущен успешно!"
        echo ""
        echo "🧪 Можете тестировать Rasa:"
        echo "1. Статус: curl http://localhost:5005/status"
        echo "2. Тест: python test_rasa.py"
        echo "3. Веб: откройте rasa-tester.html в браузере"
        echo ""
        echo "📋 Управление:"
        echo "Логи: docker-compose -f docker-compose-rasa-fixed.yml logs -f"
        echo "Стоп: docker-compose -f docker-compose-rasa-fixed.yml down"
        exit 0
    fi
    echo "Ожидание... ($i/12)"
    sleep 5
done

echo "⚠️ Rasa сервер не отвечает после 60 секунд"
echo "Проверьте логи: docker-compose -f docker-compose-rasa-fixed.yml logs"
exit 1
