from pydantic import BaseModel,EmailStr,Field


class User(BaseModel):
    email: EmailStr
    first_name: str = Field(...,min_length=0,max_length=50)
    last_name: str = Field(...,min_length=0,max_length=50)


class UserCreate(User):
    pass


class UserResponse(User):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

