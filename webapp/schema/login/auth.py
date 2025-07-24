from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example='user@example.com')
    password: str = Field(..., example='qwerty')


class LoginResponse(BaseModel):
    access_token: str
