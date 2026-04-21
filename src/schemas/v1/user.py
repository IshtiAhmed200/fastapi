from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=0, max_length=50)
    last_name: str = Field(..., min_length=0, max_length=50)


class UserCreate(User):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = Field(None, min_length=0, max_length=50)
    last_name: str | None = Field(None, min_length=0, max_length=50)


class UserUpdateWithPassword(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = Field(None, min_length=0, max_length=50)
    last_name: str | None = Field(None, min_length=0, max_length=50)
    password: str | None = Field(None, min_length=6)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str