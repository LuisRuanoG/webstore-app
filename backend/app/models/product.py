from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Column, DateTime

class Product(SQLModel, table=True):
    __tablename__: str = "products"

    # Campos de la tabla
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: Decimal = Field(default=0.0, ge=0.0, max_digits=10, decimal_places=2)
    sku: Optional[str] = Field(default=None, index=True, unique=True)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.categories_id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc, tzinfo=timezone.utc)
                                 , sa_column=Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)))
    