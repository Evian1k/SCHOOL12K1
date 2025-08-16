# EduManage

Full-stack school management system.

## Tech Stack
- Backend: Flask, SQLAlchemy, JWT, Marshmallow, CORS, Requests
- Frontend: React (Vite), React Router, Axios, Tailwind
- Database: PostgreSQL
- Payments: Safaricom Daraja API (M-Pesa STK Push)

## Structure
- `backend/`: Flask app, models, routes, services
- `frontend/`: Vite React app with Tailwind

## Quick Start

Backend:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
flask db init && flask db migrate -m "init" && flask db upgrade
python manage.py
```

Frontend:
```bash
cd ../frontend
npm install
npm run dev
```

Visit the frontend at `http://localhost:5173`. API runs at `http://localhost:5000`.