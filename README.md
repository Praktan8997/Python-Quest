# 🐍 Python Quest — Gamified Python Learning Platform

Python Quest is an interactive, gamified learning application designed for Python bootcamp students. Inspired by modern competitive learning platforms, it combines Duolingo-style progression, hands-on coding challenges with isolated execution, quizzes, badges, streaks, and real-time leaderboards.

---

## 🌟 Key Features

- **Dual Navigation Modes**:
  - **Guided Path**: Structured progression across 5 levels (Basics → Control Flow → Collections → Functions → Environment).
  - **Explore Mode**: Unlocked access to jump directly to any of the 23 Python topics.
- **Interactive Learning Loop**: Concept Learn → Code Example → Try It → Practice Challenge → Quiz → Earn XP & Level Up.
- **Isolated Code Execution**: Student code runs safely in a separate microservice.
- **Gamification**: Dynamic XP rewards, automatic level calculation, streak tracking 🔥, badges 🏆, and global leaderboards.
- **Instructor Dashboard Analytics**: Overview of student progress, quiz accuracy, and topic difficulty distribution.

---

## 🏗 Project Architecture

```text
python-quest/
├── frontend/           # React + Vite + Tailwind CSS + Monaco Code Editor
├── backend/            # FastAPI + SQLAlchemy REST API
├── execution-service/  # Isolated Python runner service (Port 8001)
├── database/           # Database seed script for 23 topics, lessons, quizzes
├── .env.example
├── .gitignore
├── agent.md
├── gemini.md
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Isolated Execution Service Setup
```bash
cd execution-service
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
```

### 3. Backend Setup & Seed Data
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Seed curriculum database
python ../database/seed_data.py

# Start Backend Server
uvicorn app.main:app --port 8000 --reload
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 🛡 API Endpoints & Health Check

- **Health Check**: `GET http://localhost:8000/health` -> `{"status": "ok"}`
- **Auth**: `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/users/me`
- **Topics**: `GET /api/topics`, `GET /api/topics/{id}`
- **Challenges**: `POST /api/challenges/{id}/submit`
- **Quizzes**: `POST /api/quizzes/{id}/submit`
- **Leaderboard**: `GET /api/leaderboard`

---

## 🌐 Production Deployment

- **Frontend**: Deploy `frontend` build (`npm run build`) to Vercel/Netlify. Set `VITE_API_BASE_URL`.
- **Backend**: Deploy `backend` to Render/Railway using `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Configure `DATABASE_URL` (MySQL/PostgreSQL) and `CORS_ORIGINS`.
- **Code Execution**: Deploy `execution-service` to isolated container instance.
