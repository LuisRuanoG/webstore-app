from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InventoryCreate(BaseModel):
    product_id: int
    staff_id: int
    reason: str
    change_amount: int
    reference_id: Optional[int] = None


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    reason: str
    reference_id: Optional[int] = None
    staff_id: int
    created_at: datetime
    change_amount: int

    model_config = {"from_attributes": True}
