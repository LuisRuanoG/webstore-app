from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    provider: str
    provider_transaction_id: str
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    status: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
