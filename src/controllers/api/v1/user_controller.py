from fastapi import APIRouter, Depends , status,HTTPException, Query
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.v1.user import UserCreate, UserResponse, UserUpdate
from src.config.database import get_db
from typing import List,Annotated
from src.helpers.validate_unique_email import validate_unique_email 
from src.filters.user_filter import UserFilter

router = APIRouter()

@router.get('/',response_model=List[UserResponse])
def list_users(filters: Annotated[UserFilter, Query()], db:Session = Depends(get_db)):
    query= db.query(User)

    if filters.first_name:
       query = query.filter(User.first_name.like(f"%{filters.first_name}%"))
    
    if filters.last_name:
       query = query.filter(User.last_name.like(f"%{filters.last_name}%"))
    
    if filters.email:
       query = query.filter(User.email == filters.email)

    return query.all()


@router.post('/',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_users(user_data:UserCreate = Depends(validate_unique_email),db:Session = Depends(get_db)):
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
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create user."
        )


@router.put('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    update_fields = user_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "message": "The User is Deleted Successfully"}