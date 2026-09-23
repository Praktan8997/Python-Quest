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
    is_empty = db.query(Topic).count() == 0
    db.close()
    
    if is_empty:
        print("Database is empty. Auto-running seed script...", flush=True)
        # Import seed function directly to avoid subprocess pool deadlocks
        import sys, os
        seed_script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database"))
        if seed_script_dir not in sys.path:
            sys.path.insert(0, seed_script_dir)
        
        try:
            from seed_data import seed
            # Run without dropping tables to avoid locking issues on startup
            seed(drop_tables=False)
            print("Database auto-seeding completed.", flush=True)
        except ImportError as ie:
            print(f"Could not import seed module: {ie}", flush=True)
except Exception as e:
    print(f"Warning: Error checking/seeding database: {e}", flush=True)

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
