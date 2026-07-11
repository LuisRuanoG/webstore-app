from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name", max_length=100)


class ProductResponse(ProductBase):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal = Field(default=0.0, ge=0.0, max_digits=10, decimal_places=2)
    stock_quantity: int
    category_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    sku: Optional[str] = Field(default=None, max_length=50, description="Stock Keeping Unit (SKU)")

    model_config = {"from_attributes": True}

class ProductCreate(ProductBase):
    description: Optional[str] = None
    price: Decimal = Field(default=0.0, ge=0.0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: Optional[int] = None
    is_active: bool = Field(default=True)
    sku : Optional[str] = Field(default=None, max_length=50, description="Stock Keeping Unit (SKU)")


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

