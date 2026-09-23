# 🐍 Python Quest

A gamified, interactive Python learning platform designed for bootcamp students. Features 19 topics, 38+ coding challenges, 57+ quiz questions, XP progression, leaderboard, and live code execution.

---

## 🚀 Live Demo

| Service | URL |
|---------|-----|
| Frontend | https://python-quest-frontend.onrender.com |
| Backend API | https://python-quest-backend.onrender.com |
| API Docs | https://python-quest-backend.onrender.com/docs |
| Execution Service | https://python-quest-execution.onrender.com |

> ⚠️ Free tier services spin down after 15 minutes of inactivity. First request may take ~30 seconds.

---

## 🗂 Project Structure

```
python-quest/
├── frontend/           # React + Vite + Tailwind CSS
├── backend/            # FastAPI backend API
├── execution-service/  # Isolated Python code runner
├── database/           # Seed data (19 topics, 38+ challenges)
├── render.yaml         # Render deployment blueprint
├── .env.example        # Template for environment variables
└── README.md
```

---

## ⚙️ Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/python-quest.git
cd python-quest
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

# Copy .env and configure
cp ../.env.example .env
# Edit .env — defaults work for local SQLite dev

# Start backend
uvicorn app.main:app --reload --port 8000
```
Backend runs at: http://localhost:8000  
API docs: http://localhost:8000/docs

### 3. Execution Service Setup
```bash
cd execution-service
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

# Start execution service
uvicorn app.main:app --reload --port 8001
```
Execution service runs at: http://localhost:8001

### 4. Seed the Database (local)
```bash
cd database
python seed_data.py
```
This creates 19 topics, 38+ challenges, 57+ quiz questions in your local SQLite database.

### 5. Frontend Setup
```bash
cd frontend
npm install

# Local dev .env (already created)
# VITE_API_BASE_URL=http://localhost:8000

npm run dev
```
Frontend runs at: http://localhost:5173

---

## 🌐 Render Deployment Guide

### Overview of Services on Render

| Service | Type | Purpose |
|---------|------|---------|
| `python-quest-db` | PostgreSQL DB | Database |
| `python-quest-backend` | Web Service (Python) | FastAPI API |
| `python-quest-execution` | Web Service (Python) | Code execution sandbox |
| `python-quest-frontend` | Static Site | React frontend |

---

### Step-by-Step Deployment

#### Step 1 — Push Code to GitHub

```bash
git add .
git commit -m "feat: production deployment configuration"
git push origin main
```

#### Step 2 — Create a Render Account

1. Go to https://render.com and sign up / log in
2. Connect your GitHub account

#### Step 3 — Deploy via Blueprint (render.yaml)

1. In the Render dashboard, click **"New"** → **"Blueprint"**
2. Select your GitHub repo (`python-quest`)
3. Render will auto-detect `render.yaml` and show you all 4 services
4. Click **"Apply"**
5. Render will:
   - Create the PostgreSQL database (`python-quest-db`)
   - Deploy the backend (`python-quest-backend`)
   - Deploy the execution service (`python-quest-execution`)
   - Deploy the frontend static site (`python-quest-frontend`)

> ⏱ First deploy takes ~5-10 minutes.

#### Step 4 — Note Service URLs

After deploy, collect these URLs from the Render dashboard:
- Backend: `https://python-quest-backend.onrender.com`
- Execution: `https://python-quest-execution.onrender.com`
- Frontend: `https://python-quest-frontend.onrender.com`

#### Step 5 — Update CORS and Execution URL (Backend)

In Render Dashboard → `python-quest-backend` → **Environment**:

| Key | Value |
|-----|-------|
| `CORS_ORIGINS` | `https://python-quest-frontend.onrender.com` |
| `CODE_EXECUTION_URL` | `https://python-quest-execution.onrender.com/run` |

Click **"Save Changes"** — backend will redeploy automatically.

#### Step 6 — Update Frontend API URL (if needed)

If the `VITE_API_BASE_URL` wasn't picked up from `frontend/.env.production`, set it manually:

In Render Dashboard → `python-quest-frontend` → **Environment**:

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://python-quest-backend.onrender.com` |

Then click **"Manual Deploy"** → **"Deploy latest commit"**.

#### Step 7 — Seed the Production Database

Get the PostgreSQL connection string from Render:
- Dashboard → `python-quest-db` → **Connect** tab → copy **External Database URL**

Run the seed script from your local machine:

```powershell
# Windows PowerShell
$env:DATABASE_URL = "postgresql://python_quest_user:PASSWORD@HOST/python_quest"
cd database
python seed_data.py
```

```bash
# Linux / Mac
DATABASE_URL="postgresql://python_quest_user:PASSWORD@HOST/python_quest" python database/seed_data.py
```

> ✅ This seeds 19 topics, 38+ challenges, 57+ quiz questions, and XP configuration.

#### Step 8 — Verify Deployment

Run these checks to confirm everything works:

```bash
# Backend health
curl https://python-quest-backend.onrender.com/health

# Execution service health
curl https://python-quest-execution.onrender.com/health

# Topics (should return 19 topics after seeding)
curl https://python-quest-backend.onrender.com/api/topics

# Leaderboard
curl https://python-quest-backend.onrender.com/api/leaderboard
```

Or open the API docs: https://python-quest-backend.onrender.com/docs

---

## 🔑 Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL or SQLite URL | `sqlite:///./python_quest.db` |
| `SECRET_KEY` | App secret key | dev value |
| `JWT_SECRET` | JWT signing secret | dev value |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `1440` (24h) |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173` |
| `CODE_EXECUTION_URL` | URL to execution service `/run` endpoint | `http://127.0.0.1:8001/run` |

### Execution Service (`execution-service/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `ALLOWED_ORIGINS` | Comma-separated allowed CORS origins | `*` (all — dev only) |

### Frontend (`frontend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | URL to the backend API | `http://localhost:8000` |

---

## 🗄 Database

### Local (SQLite)
No setup needed — SQLite file is created automatically at `backend/python_quest.db`.

### Production (PostgreSQL on Render)
- Render creates and manages the PostgreSQL instance
- Connection string is injected as `DATABASE_URL` automatically
- The backend handles both `postgres://` and `postgresql://` URL schemes

---

## 🧪 API Endpoints

### Auth
```
POST /api/auth/register    — Register new student
POST /api/auth/login       — Login
GET  /api/auth/me          — Get current user profile
```

### Topics & Learning
```
GET  /api/topics                          — List all 19 topics
GET  /api/topics/{id}                     — Topic details
GET  /api/topics/{id}/lessons             — Topic lessons
GET  /api/topics/{id}/challenges          — Topic challenges
GET  /api/topics/{id}/quizzes             — Topic quizzes
```

### Challenges & Code Execution
```
GET  /api/challenges/{id}                 — Get challenge details
POST /api/challenges/{id}/run             — Dry run code (no XP)
POST /api/challenges/{id}/submit          — Submit solution (awards XP)
GET  /api/users/me/submissions            — My submission history
```

### Quizzes
```
POST /api/quizzes/{id}/submit             — Submit quiz answers (awards XP)
GET  /api/quizzes/{id}/attempts           — Quiz attempt history
GET  /api/users/me/quiz-history           — All my quiz history
```

### Progress & Gamification
```
GET  /api/progress         — My XP, level, badges, topic completion
GET  /api/leaderboard      — Global leaderboard
GET  /api/badges           — All available badges
```

### Health
```
GET  /health               — Backend health (no auth required)
```

---

## 🏆 XP & Leveling System

| Action | XP |
|--------|-----|
| Lesson viewed | +20 XP |
| Challenge completed | +50 XP |
| Quiz passed | +75 XP |
| Boss challenge | +250 XP |

| Level | XP Required |
|-------|-------------|
| 1 | 0 |
| 2 | 100 |
| 3 | 250 |
| 4 | 500 |
| 5 | 850 |
| ... | ... |

---

## 🐛 Troubleshooting

### Frontend shows "Network Error"
- Check `VITE_API_BASE_URL` in Render dashboard → frontend service
- Ensure it points to `https://python-quest-backend.onrender.com`
- Trigger a manual redeploy of the frontend

### Backend returns CORS errors
- Update `CORS_ORIGINS` in Render → backend service env vars
- Format: `https://python-quest-frontend.onrender.com` (no trailing slash)
- Save changes — backend redeploys automatically

### Topics list is empty (no data)
- The database has not been seeded yet
- Run the seed command in Step 7 above using your production DB URL

### Code execution fails / times out
- Check execution service is running: `curl https://python-quest-execution.onrender.com/health`
- Verify `CODE_EXECUTION_URL` in backend env vars points to the correct execution service URL

### Cold start delays
- Free tier Render services sleep after 15 minutes of inactivity
- First request after sleep takes ~20-30 seconds
- Consider upgrading to a paid plan to eliminate cold starts

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, Monaco Editor |
| Backend | FastAPI, SQLAlchemy, Pydantic, Python-Jose |
| Database | PostgreSQL (production), SQLite (local dev) |
| Code Execution | Isolated FastAPI subprocess runner |
| Deployment | Render (all services) |
| Auth | JWT Bearer tokens, bcrypt password hashing |
