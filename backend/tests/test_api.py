import pytest
from fastapi.testclient import TestClient
import os
import sys
import uuid

# Ensure backend module and root modules are importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.main import app
from app.core.database import Base, engine
from database.seed_data import seed

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    seed()
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_user_registration_and_login():
    uid = uuid.uuid4().hex[:6]
    reg_payload = {
        "username": f"student_{uid}",
        "email": f"student_{uid}@test.com",
        "password": "Password123!",
        "full_name": "Test Student"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code == 200
    assert res_reg.json()["username"] == f"student_{uid}"

    # Login
    login_payload = {
        "username": f"student_{uid}",
        "password": "Password123!"
    }
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    assert token is not None

    # Get Me
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["username"] == f"student_{uid}"

def test_topics_endpoint():
    res = client.get("/api/topics")
    assert res.status_code == 200
    topics = res.json()
    assert len(topics) == 21

def test_challenge_submission():
    uid = uuid.uuid4().hex[:6]
    reg_payload = {
        "username": f"runner_{uid}",
        "email": f"runner_{uid}@test.com",
        "password": "Password123!",
        "full_name": "Runner Student"
    }
    client.post("/api/auth/register", json=reg_payload)
    login_payload = {"username": f"runner_{uid}", "password": "Password123!"}
    res_login = client.post("/api/auth/login", json=login_payload)
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Submit correct code for Challenge 1
    submit_payload = {
        "code": "print('Welcome, Python Quest!')"
    }
    res_sub = client.post("/api/challenges/1/submit", json=submit_payload, headers=headers)
    assert res_sub.status_code == 200
    data = res_sub.json()
    assert data["passed"] == True
    assert data["xp_gained"] == 50

def test_leaderboard_endpoint():
    res = client.get("/api/leaderboard")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_daily_puzzle_endpoint():
    res = client.get("/api/quizzes/daily-puzzle")
    assert res.status_code == 200
    data = res.json()
    assert "question_text" in data
    assert "id" in data
    assert "puzzle_date" in data

def test_quiz_with_different_question_types():
    """Test that quizzes with multiple choice, true/false, fill-in-blank render correctly."""
    # Query topic 1 quizzes to verify question_type field is present
    res_quizzes = client.get("/api/topics/1/quizzes")
    assert res_quizzes.status_code == 200
    quizzes = res_quizzes.json()
    assert len(quizzes) > 0
    # Verify question_type is returned in schema
    for q in quizzes[0].get("questions", []):
        assert "question_type" in q
