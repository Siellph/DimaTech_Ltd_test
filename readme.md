## DimaTech Ltd 🚀

📝 Тестовое задание. Backend, Python

🚀 Технологии:

[![Sanic](https://img.shields.io/badge/Sanic-25.3.0-blue?logo=sanic)](https://sanic.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-blue?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-red?logo=python)](https://www.sqlalchemy.org/)

### ⚡️ Запуск проекта

1. 🐳 Убедитесь, что установлен [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/).
2. 📦 Клонируйте репозиторий проекта:
    ```bash
    git clone https://github.com/Siellph/DimaTech_Ltd_test.git
    ```
3. 📂 Перейдите в директорию проекта:
    ```bash
    cd DimaTech_Ltd_test
    ```
4. 🏗️ Соберите и запустите контейнеры:
    ```bash
    docker-compose up --build
    ```

    либо

       ```bash
    docker-compose up --build -d
    ```

    для скрытия отображения выполнения в терминале

3. 🌐 Приложение будет доступно по адресу:
- http://127.0.0.1:8000/

Документация будет доступна после запуска контейнеров по адресам:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/docs/redoc
- http://127.0.0.1:8000/docs/swagger

### 📁 Структура проекта

- `conf/` — конфигурационные файлы проекта
- `docker/` — файлы для сборки и настройки Docker-образов
- `fixture/` — тестовые данные и фикстуры
- `scripts/` — вспомогательные скрипты
- `webappapp/` — исходный код приложения
- `docker-compose.yml` — конфигурация Docker Compose (описание сервисов, БД)
- `pyproject.toml` — зависимости и настройки проекта
- `README.md` — документация проекта

### Примеры для проверки `/api/v1/transaction/webhook/payment` с SECRET_KEY `gfdmhghif38yrf9ew0jkf32` (указан в проекте)

- Добавит платеж счету 1 у пользователя 1, если создан, иначе создаст и затем добавит платеж
    ```json
    {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "account_id": 1,
        "user_id": 1,
        "amount": 100,
        "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
    }
    ```

- Добавит платеж счету 2 у пользователя 1, если создан, иначе создаст и затем добавит платеж
    ```json
    {
        "transaction_id": "baa0c6dd-f694-4474-be8b-d15c52eabc99",
        "account_id": 2,
        "user_id": 1,
        "amount": 1500,
        "signature": "091d98c80c1cef09bb6bf15de820717a3336ba66a70106ccd5f158f948787585"
    }
    ```

- Добавит платеж счету 2 у пользователя 1, если создан, иначе создаст и затем добавит платеж
    ```json
    {
        "transaction_id": "0ba656f1-7aca-414d-b6a4-7a6b82e55cce",
        "account_id": 2,
        "user_id": 1,
        "amount": 540,
        "signature": "c29cbf5ab7d09254ea4376c07e660d7b5ee706a1e385eb2661902e5344ab38ae"
    }
    ```

- Добавит платеж счету 6 у пользователя 2, если создан, иначе создаст и затем добавит платеж
    ```json
    {
        "transaction_id": "7b558fbf-d742-4656-a7df-80e1050ecf20",
        "account_id": 6,
        "user_id": 2,
        "amount": 150,
        "signature": "3cb03bde126237aaf3ee04a77f5269cd083feb0df318f32d7efa9aafad06650a"
    }
    ```
