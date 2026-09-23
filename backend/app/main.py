from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth, topics, challenges, quizzes, leaderboard

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# Auto-seed the database if it is empty
import sys
import os
import subprocess
from app.core.database import SessionLocal
from app.models.models import Topic

try:
    db = SessionLocal()
    # Check if we have any topics
    if db.query(Topic).count() == 0:
        print("Database is empty. Auto-running seed script...")
        seed_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "seed_data.py"))
        if os.path.exists(seed_script_path):
            # Run the seed script as a subprocess (it will pick up DATABASE_URL)
            # Pass a special arg or just run it. We will run it as is, which drops and recreates tables.
            subprocess.run([sys.executable, seed_script_path])
            print("Database auto-seeding completed.")
    db.close()
except Exception as e:
    print(f"Warning: Error checking/seeding database: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unauthenticated health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}

# Include API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(topics.router, prefix=settings.API_V1_STR)
app.include_router(challenges.router, prefix=settings.API_V1_STR)
app.include_router(quizzes.router, prefix=settings.API_V1_STR)
app.include_router(leaderboard.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
