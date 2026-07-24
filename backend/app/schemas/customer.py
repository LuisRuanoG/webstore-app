from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    email: EmailStr
    name: str
    phone: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    firebase_costumer_id: Optional[str] = None
    email: EmailStr
    name: str
    phone: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
