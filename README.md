# Lab1: Healthcheck API, Docker Compose, CI

Навчальний вебзастосунок на Flask із системними ендпоінтами перевірки стану
(Liveness / Readiness), контейнеризацією та CI на GitHub Actions.

![CI](https://github.com/IO45SizonenkoArtem/Lab1/actions/workflows/ci.yml/badge.svg)

## Стек

- Python 3.11, Flask, gunicorn
- Docker, Docker Compose
- GitHub Actions, ruff (лінтер)

## Вимоги

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (або Docker Engine + плагін Compose)
- Git

Python локально встановлювати не потрібно: усе запускається в контейнері.

## Запуск через Docker Compose

1. Склонуйте репозиторій:

   ```bash
   git clone https://github.com/<ваш-логін>/Lab1.git
   cd Lab1
   ```

2. Зберіть і запустіть сервіс:

   ```bash
   docker compose up --build
   ```

3. Застосунок буде доступний на `http://localhost:8080`.

Якщо порт 8080 на вашій машині зайнятий або заблокований, задайте інший
через змінну `HOST_PORT`:

```bash
# Linux / macOS
HOST_PORT=8081 docker compose up --build

# Windows PowerShell
$env:HOST_PORT = "8081"
docker compose up --build
```

Запуск у фоновому режимі: `docker compose up --build -d`.
Зупинка та видалення контейнера: `docker compose down`.

## Ендпоінти

### `GET /healthz/live` (Liveness)

Перевіряє, що процес застосунку працює. Повертає `200 OK`:

```json
{
  "status": "alive",
  "timestamp": "2026-10-28T13:01:03.292827+00:00"
}
```

### `GET /healthz/ready` (Readiness)

Перевіряє готовність приймати трафік. На цьому етапі зовнішніх залежностей
немає. Повертає `200 OK`:

```json
{
  "status": "ready",
  "database": "not_connected_yet",
  "timestamp": "2026-10-28T13:01:05.783831+00:00"
}
```

Приклад перевірки:

```bash
curl http://localhost:8080/healthz/live
curl http://localhost:8080/healthz/ready
```

## Локальна розробка (без Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python -m app.views              # порт задається змінною PORT (за замовчуванням 8080)
ruff check .                     # лінтер
```

## Структура проєкту

```
.
├── .github/workflows/ci.yml   # CI: лінтер, збірка образу, валідація compose
├── app/
│   ├── __init__.py
│   └── views.py               # healthcheck-ендпоінти
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt           # залежності застосунку
├── requirements-dev.txt       # інструменти розробки (ruff)
└── README.md
```

## CI

При кожному `push` і `pull_request` у `main`/`master` GitHub Actions:

1. встановлює залежності розробки та запускає `ruff check .`;
2. збирає Docker-образ;
3. перевіряє конфігурацію `docker compose config`.