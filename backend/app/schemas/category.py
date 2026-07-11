from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., description="Nombre de la categoria")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="Nombre de la categoria")


class CategoryResponse(CategoryBase):
    categories_id: int
    slug: str
    created_at: datetime

    model_config = {"from_attributes": True}
