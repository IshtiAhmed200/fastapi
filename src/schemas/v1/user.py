from pydantic import BaseModel,EmailStr,Field


class User(BaseModel):
    name: str = Field(...,min_length=3,max_length=10)
    email: EmailStr
    password: str