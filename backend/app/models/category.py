from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    categories_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100, unique=True)
    slug: str = Field(index=True, max_length=120, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
