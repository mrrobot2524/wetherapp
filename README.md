# 🌤️ Погодное веб-приложение на FastAPI

Веб-приложение, где пользователь вводит название города и получает прогноз погоды. Реализована авторизация, история запросов, тёмная/светлая тема, автодополнение и многое другое.

---

## 🚀 Возможности

- Поиск прогноза по городу
- История просмотров (по пользователю)
- Автодополнение города
- Хранение последнего города
- Тёмная / светлая тема
- Адаптивный frontend на HTML/CSS/JS
- JWT аутентификация (регистрация / логин)
- PostgreSQL + Alembic миграции
- Open-Meteo API

---

## 🛠️ Используемые технологии

- **Backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, Pydantic
- **Frontend**: HTML5, CSS3, JavaScript (без фреймворков)
- **API погоды**: https://open-meteo.com
- **Аутентификация**: JWT + Cookie
- **База данных**: PostgreSQL
- **Автодополнение**: Open-Meteo `autocomplete` endpoint

---

## ⚙️ Установка и запуск

# 2. Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить .env файл
cp .env.example .env

# 5. Применить миграции
alembic upgrade head

# 6. Запустить сервер
uvicorn app.main:app --reload
