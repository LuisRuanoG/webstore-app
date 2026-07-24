from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_id: int
    delivery_note: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    delivery_note: Optional[str] = None

    model_config = {"from_attributes": True}
