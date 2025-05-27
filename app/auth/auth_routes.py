from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import SessionLocal
from app.schemas.user import UserCreate
from app.auth.auth_handler import create_access_token, verify_password
from app.crud import user as crud_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = crud_user.create_user(db, user.email, user.password)
    return {"id": new_user.id, "email": new_user.email}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
