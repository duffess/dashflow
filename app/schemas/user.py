from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#schema de criação de usuario

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str

#schema de login

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# schema de resposta do usuario sem senha

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

#schema de token

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None