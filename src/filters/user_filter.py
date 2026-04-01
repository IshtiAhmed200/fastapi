from pydantic import BaseModel, EmailStr,Field
from typing import List,Optional

class UserFilter(BaseModel):
    first_name:Optional[str] = Field(None,min_length=1)
    last_name:Optional[str] = Field(None,min_length=1)
    email:Optional[EmailStr] = None