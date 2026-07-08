from typing import Optional
from pydantic import BaseModel, Field

# base model for users need username, email 
class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)

#post and put model for users, AQUÍ pedimos contraseña al user para registrarlo
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, description="La contraseña debe tener entre 8 y 100 caracteres")

#response model for users, AQUÍ NO va la contraseña. Solo datos seguros para React.
class UserResponse(UserBase):
    id: int
    model_config = {"from_attributes": True}

