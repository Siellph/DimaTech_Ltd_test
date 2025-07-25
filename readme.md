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
