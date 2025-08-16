# EduManage Backend (Flask)

## Setup

1. Create and activate venv
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment
- Copy `.env.example` to `.env` and fill values.
- Ensure PostgreSQL is running and `DATABASE_URL` is valid.

4. Initialize database
```bash
export FLASK_APP=manage.py
flask db init
flask db migrate -m "init db"
flask db upgrade
```

5. Run server
```bash
python manage.py
```

## API Prefix
All endpoints are under `/api/*`.

## Auth
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`
- Me: `GET /api/auth/me` (JWT)

## Payments (Daraja)
- Initiate STK: `POST /api/payments/stk-push` (JWT: admin/parent)
- Callback: `POST /api/payments/callback` (public URL configured in Daraja)

Note: For sandbox, expose callback with a public URL (e.g., ngrok) and set `DARAJA_CALLBACK_URL` accordingly.