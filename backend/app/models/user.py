from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=100)
    email: str = Field(index=True, max_length=100)
    password: str = Field(max_length=100)