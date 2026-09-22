from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_current_user(token: Optional[str] = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)) -> User:
    """Returns authenticated user if token present, or automatically falls back to default guest user."""
    if token:
        user_id = decode_access_token(token)
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                return user
    
    # Fallback to default guest user
    guest = db.query(User).filter(User.username == "guest_coder").first()
    if not guest:
        guest = User(
            username="guest_coder",
            email="guest@pythonquest.dev",
            hashed_password="guest",
            full_name="Python Coder",
            role="student",
            level=1,
            xp=0,
            current_streak=1
        )
        db.add(guest)
        db.commit()
        db.refresh(guest)
    return guest

def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)) -> Optional[User]:
    return get_current_user(token, db)

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name or user_data.username
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
