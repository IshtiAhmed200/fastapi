from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    first_name: str = Field(default="", max_length=50)
    last_name: str = Field(default="", max_length=50)


class UserCreate(User):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserUpdateWithPassword(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = Field(None, min_length=6)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str