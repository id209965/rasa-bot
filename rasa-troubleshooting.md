# 🔧 Устранение проблем с установкой Rasa

## Проблема: mattermostwrapper и setuptools конфликт

**Ошибка:** `TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'`

**Причина:** Несовместимость между старыми пакетами Rasa и новыми версиями setuptools/packaging.

## ⚡ Решения (по порядку приоритета)

### Решение 1: Понизить версию setuptools
```bash
source venv-rasa/bin/activate
pip install setuptools==57.5.0
pip install packaging==21.3
pip install rasa==3.6.13 rasa-sdk==3.6.2
```

### Решение 2: Использовать Python 3.8 или 3.9
```bash
# Если у вас Python 3.10+, попробуйте более старую версию
python3.8 -m venv venv-rasa-38
source venv-rasa-38/bin/activate
pip install setuptools==57.5.0
pip install rasa==3.6.13
```

### Решение 3: Установка через conda
```bash
# Если у вас есть conda/miniconda
conda create -n rasa-env python=3.9
conda activate rasa-env
conda install -c conda-forge rasa=3.6.13
```

### Решение 4: Docker (рекомендуется)
```bash
# Создать docker-compose-rasa-only.yml
version: '3.8'
services:
  rasa:
    image: rasa/rasa:3.6.13
    ports:
      - "5005:5005"
    volumes:
      - ./app/rasa:/app
    command: >
      bash -c "rasa train --domain domain.yml --data data/ --config config.yml &&
               rasa run --enable-api --cors '*' --debug"
```

```bash
docker-compose -f docker-compose-rasa-only.yml up
```

### Решение 5: Принудительная установка (может быть нестабильно)
```bash
source venv-rasa/bin/activate
pip install --force-reinstall --no-cache-dir setuptools==57.5.0 packaging==21.3
pip install --no-deps mattermostwrapper==2.2
pip install rasa==3.6.13 rasa-sdk==3.6.2
```

## 🐳 Рекомендуемое решение: Docker

Создайте файл `docker-compose-rasa-only.yml`:

```yaml
version: '3.8'

services:
  rasa:
    image: rasa/rasa:3.6.13-full
    ports:
      - "5005:5005"
    volumes:
      - ./app/rasa:/app
    working_dir: /app
    command: >
      bash -c "rasa train &&
               rasa run --enable-api --cors '*' --debug --port 5005"
    environment:
      - RASA_TELEMETRY_ENABLED=false
```

Запуск:
```bash
# В основном терминале - bot без Rasa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# В отдельном терминале - Rasa в Docker
docker-compose -f docker-compose-rasa-only.yml up
```

## ✅ Проверка работы Rasa

После успешной установки проверьте:

```bash
# Проверить статус Rasa сервера
curl http://localhost:5005/status

# Тестовый запрос к Rasa
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "привет"}'
```

## 🚫 Если ничего не помогает

**Рекомендация:** Используйте основной бот без Rasa:

```bash
pip install -r requirements.txt
python main.py
```

Все функции работают (регистрация, мероприятия, друзья, админка), кроме умных диалогов.

## 📝 Альтернативы Rasa для NLP

Если нужны диалоговые функции, рассмотрите:

1. **OpenAI API** - подключить ChatGPT
2. **Dialogflow** - Google решение
3. **Простые правила** - if/else логика для базовых диалогов
4. **spaCy + правила** - более простая NLP библиотека

## 💡 Заключение

Rasa - мощная, но сложная в установке библиотека. Для большинства чат-ботов её функции избыточны.

**Рекомендуется:** 
- Начать с основной версии без Rasa
- Добавить простые диалоговые правила
- При необходимости использовать Rasa в Docker
