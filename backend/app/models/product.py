from typing import Optional
from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    __tablename__: str = "products"

    # Campos de la tabla
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    stock: int
    image_url: Optional[str] = None