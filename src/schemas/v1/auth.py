from pydantic import BaseModel, EmailStr, Field


class Register(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=0, max_length=50)
    last_name: str = Field(..., min_length=0, max_length=50)
    password: str = Field(..., min_length=6)


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None