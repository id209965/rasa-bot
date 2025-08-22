# Rasa Docker Fix

## Проблема

В логах Docker контейнера появлялась ошибка:
```
rasa: error: argument {init,run,shell,train,interactive,telemetry,test,visualize,data,export,x,evaluate}: invalid choice: 'bash'
```

## Причина

Проблема была в неправильной команде в `docker-compose-rasa-only.yml`:
```yaml
command: >
  bash -c "rasa train --domain domain.yml --data data/ --config config.yml &&
           rasa run --enable-api --cors '*' --debug --port 5005"
```

Rasa Docker образ имеет свой entrypoint, который ожидает команды Rasa напрямую, а не через bash.

## Решения

### ✅ Решение 1: Исправленный Docker (рекомендуется)

**Файлы:**
- `docker-compose-rasa-fixed.yml` - исправленная конфигурация
- `rasa-docker-setup.sh` - скрипт для обучения и запуска
- `test-rasa-quick.sh` - быстрый тест

**Запуск:**
```bash
# Автоматическая настройка и запуск
./rasa-docker-setup.sh

# Тестирование
./test-rasa-quick.sh
```

**Как это работает:**
1. Сначала обучается модель в отдельном контейнере
2. Затем запускается сервер с готовой моделью
3. Разделение процессов решает проблему с bash командами

### ✅ Решение 2: Локальный запуск (альтернатива)

**Файл:** `run-rasa-local.sh`

**Запуск:**
```bash
./run-rasa-local.sh
```

Запускает Rasa напрямую в системе без Docker.

## Технические детали

### Исправления в docker-compose-rasa-fixed.yml:

```yaml
# ❌ Старая версия (не работает)
command: >
  bash -c "rasa train && rasa run"

# ✅ Новая версия (работает)
command: [
  "rasa", "run", 
  "--enable-api", 
  "--cors", "*", 
  "--debug", 
  "--port", "5005",
  "--model", "/app/models"
]
```

### Почему это работает:

1. **Убрали bash -c**: Rasa образ имеет собственный entrypoint
2. **Разделили обучение и запуск**: обучение происходит заранее
3. **Явно указали путь к модели**: `--model /app/models`
4. **Используем array syntax**: более надежно для Docker

## Использование

### Docker версия:
```bash
# Полный цикл: обучение + запуск
./rasa-docker-setup.sh

# Просмотр логов
docker-compose -f docker-compose-rasa-fixed.yml logs -f

# Остановка
docker-compose -f docker-compose-rasa-fixed.yml down

# Только обучение модели
docker run --rm -v "$(pwd)/app/rasa:/app" -w /app rasa/rasa:3.6.13-full rasa train
```

### Локальная версия:
```bash
# Установка и запуск
./run-rasa-local.sh
```

### Тестирование:
```bash
# Быстрый автотест
./test-rasa-quick.sh

# Интерактивный тест
python test_rasa.py

# Веб-интерфейс
# Откройте rasa-tester.html в браузере
```

### Ручное тестирование:
```bash
# Проверка статуса
curl http://localhost:5005/status

# Отправка сообщения
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "привет"}'
```

## Структура файлов

```
.
├── docker-compose-rasa-fixed.yml   # ✅ Исправленная Docker конфигурация
├── docker-compose-rasa-only.yml    # ❌ Старая версия с ошибкой
├── rasa-docker-setup.sh             # 🚀 Автоматический Docker setup
├── run-rasa-local.sh                # 🐍 Локальный запуск без Docker
├── test-rasa-quick.sh               # 🧪 Быстрое тестирование
└── app/rasa/
    ├── config.yml
    ├── domain.yml
    ├── data/
    └── models/
```

## Советы

1. **Используйте Docker версию** для продакшена
2. **Используйте локальную версию** для быстрой разработки
3. **Всегда проверяйте логи** при проблемах: `docker-compose logs -f`
4. **Убедитесь в наличии обученной модели** в `app/rasa/models/`
5. **Проверяйте порт 5005** - он должен быть свободен

## Устранение проблем

### Docker не запускается:
```bash
# Проверьте Docker daemon
docker version

# Перезапустите Docker
sudo systemctl restart docker
```

### Rasa не отвечает:
```bash
# Проверьте логи
docker-compose -f docker-compose-rasa-fixed.yml logs

# Проверьте процессы
docker ps

# Перезапустите
docker-compose -f docker-compose-rasa-fixed.yml restart
```

### Модель не найдена:
```bash
# Проверьте наличие модели
ls -la app/rasa/models/

# Переобучите модель
docker run --rm -v "$(pwd)/app/rasa:/app" -w /app rasa/rasa:3.6.13-full rasa train
```
