from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.v1.user import UserCreate,UserResponse
from src.config.database import get_db
from typing import List

router = APIRouter()

@router.get('/',response_model=List[UserResponse])
def list_users(db:Session = Depends(get_db)):
    return db.query(User).all()



@router.post('/',response_model=UserResponse)
def create_users(user_data:UserCreate,db:Session = Depends(get_db)):
    try:
        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        return "Error"