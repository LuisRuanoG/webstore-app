from typing import Optional
from sqlmodel import Field, SQLModel

class ProductImage(SQLModel, table=True):
    __tablename__ = "product_images"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    image_url: str = Field(max_length=255)
    sort_order: Optional[int] = Field(default=None)
