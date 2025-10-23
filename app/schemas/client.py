from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class ClientResponse(BaseModel):
    id: str
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    company: Optional[str]
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True