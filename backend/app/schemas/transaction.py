from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    order_id: int
    provider: str
    provider_transaction_id: str
    amount: Decimal
    status: str


class TransactionResponse(BaseModel):
    id: int
    order_id: int
    provider: str
    provider_transaction_id: str
    amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
