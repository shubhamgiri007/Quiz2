# Employee Analytics (Django + DRF)

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Configure .env (optional) with DATABASE_URL for PostgreSQL or use default SQLite
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
python manage.py seed_demo --employees 5
python manage.py runserver
```

- Swagger UI: http://127.0.0.1:8000/swagger/
- Redoc: http://127.0.0.1:8000/redoc/
- JWT: POST to `/api/token/` with username/password
- Health: `/api/health/`
- Charts: `/api/charts/`

## Environment

Create `.env` in project root:

```
DEBUG=True
SECRET_KEY=dev-secret-key-change-me
ALLOWED_HOSTS=localhost,127.0.0.1
# DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
```

## Models

- Department, Role, Employee, Attendance, PerformanceReview, Project, Assignment

## APIs

- CRUD for all core models via routers under `/api/`
- Analytics summary at `/api/analytics/summary/`
- Employee detail summary at `/api/employees/{id}/summary/`

## Throttling & Auth

- JWT via SimpleJWT
- DRF throttling configured (anon 30/min, user 120/min)

## Notes

- Default DB is SQLite for local dev. Set `DATABASE_URL` to use PostgreSQL (e.g. Neon.tech)
- Demo data created via `seed_demo` command


