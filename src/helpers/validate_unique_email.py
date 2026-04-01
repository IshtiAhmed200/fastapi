from fastapi import APIRouter, Depends , status,HTTPException
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.user import User
from src.schemas.v1.user import UserCreate

def validate_unique_email(user_data:UserCreate,db:Session = Depends(get_db)):
    is_existing_email = db.query(User).filter(User.email == user_data.email).first()
    if is_existing_email:
        raise HTTPException(
            status_code=422,
            detail="Email Already Exists."
        )
    return user_data