#!/bin/bash

# Быстрый тест Rasa

echo "🧪 Быстрый тест Rasa"
echo "===================="
echo ""

# Проверка статуса
echo "1. Проверка статуса..."
if curl -s http://localhost:5005/status | jq . 2>/dev/null; then
    echo "✅ Rasa онлайн"
else
    echo "❌ Rasa офлайн"
    echo "Запустите: ./rasa-docker-setup.sh"
    exit 1
fi

echo ""
echo "2. Тест основных сообщений:"
echo ""

# Тестовые сообщения
test_messages=(
    "привет"
    "как дела?"
    "отлично"
    "ты бот?"
    "помощь"
    "пока"
)

for message in "${test_messages[@]}"; do
    echo "⮩️ Пользователь: $message"
    
    response=$(curl -s -X POST http://localhost:5005/webhooks/rest/webhook \
        -H "Content-Type: application/json" \
        -d "{\"sender\": \"test\", \"message\": \"$message\"}")
    
    if [ $? -eq 0 ] && [ -n "$response" ] && [ "$response" != "[]" ]; then
        # Парсим JSON ответ
        bot_response=$(echo "$response" | jq -r '.[0].text // "(нет ответа)"' 2>/dev/null)
        echo "🤖 Rasa: $bot_response"
    else
        echo "🤖 Rasa: (нет ответа)"
    fi
    
    echo ""
    sleep 0.5
done

echo "✅ Тест завершён!"
echo ""
echo "📝 Для интерактивного теста: python test_rasa.py"
echo "🌐 Для веб-интерфейса: откройте rasa-tester.html"
