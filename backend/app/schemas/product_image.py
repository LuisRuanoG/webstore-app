from pydantic import BaseModel
from typing import Optional

class ProductImageCreate(BaseModel):
    image_url: str
    sort_order: Optional[int] = None


class ProductImageResponse(BaseModel):
    id : int
    product_id: int
    image_url: str
    sort_order: Optional[int] = None

    model_config = {"from_attributes": True}

class ProductImageUpdate(BaseModel):
    sort_order: Optional[int] = None