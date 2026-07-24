from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    reason: str
    reference_id: Optional[int] = None
    staff_id: int = Field(foreign_key="staff.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    change_amount: int
