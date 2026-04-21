from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.user import User
from src.schemas.v1.user import UserCreate, UserResponse, UserUpdateWithPassword
from src.config.database import get_db
from typing import List, Optional
from src.helpers.get_current_user import get_current_user

router = APIRouter()


@router.get('', response_model=dict)
@router.get('/', response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if first_name:
        query = query.filter(User.first_name.like(f"%{first_name}%"))

    if last_name:
        query = query.filter(User.last_name.like(f"%{last_name}%"))

    if email:
        query = query.filter(User.email == email)

    if search:
        query = query.filter(
            or_(
                User.first_name.like(f"%{search}%"),
                User.last_name.like(f"%{search}%"),
                User.email.like(f"%{search}%")
            )
        )

    total = query.count()
    total_pages = (total + limit - 1) // limit
    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": [{"id": user.id, "email": user.email, "first_name": user.first_name or "", "last_name": user.last_name or ""} for user in items],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }


@router.get('/search', response_model=List[UserResponse])
def search_users(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if name:
        query = query.filter(
            or_(User.first_name.like(f"%{name}%"), User.last_name.like(f"%{name}%"))
        )
        
    if email:
        query = query.filter(User.email.like(f"%{email}%"))

    items = query.all()
    return [UserResponse(id=user.id, email=user.email, first_name=user.first_name or "", last_name=user.last_name or "") for user in items]


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_users(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = User.hash_password(user_data.password)
    user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this user.")
    return current_user


@router.put('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user_data: UserUpdateWithPassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    update_fields = user_data.model_dump(exclude_unset=True)
    
    if 'password' in update_fields and update_fields['password']:
        update_fields['password'] = User.hash_password(update_fields['password'])
    
    for field, value in update_fields.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    db.delete(user)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "message": "The User is Deleted Successfully"}