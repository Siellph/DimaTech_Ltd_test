from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from webapp.schema.account.account import AccountRead


class UserCreate(BaseModel):
    username: str = Field(..., example='johndoe')
    email: EmailStr = Field(..., example='johndoe@example.com')
    full_name: str = Field(..., example='John Doe')
    password: str = Field(..., min_length=6, example='secure_password')


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    full_name: str
    role: str = 'user'
    accounts: List[AccountRead] = []
