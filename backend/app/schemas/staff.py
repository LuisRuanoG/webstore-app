from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Lo que manda el cliente al crear un empleado.
# firebase_staff_id fuera a propósito: no lo controla el cliente, se linkea después.
class StaffCreate(BaseModel):
    email: EmailStr  # valida formato de email automáticamente
    name: str
    role: str


# Todo opcional, para permitir PATCH parcial.
# No reusar StaffCreate aquí — email/name/role obligatorios ahí tumbarían
# cualquier PATCH que no los incluya (ver bug que ya cazamos en categories).
class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


# Lo que devuelve el servidor. Incluye todo lo que el frontend necesita ver,
# incluyendo campos generados por el servidor (id, timestamps, firebase_staff_id).
class StaffResponse(BaseModel):
    id: int
    firebase_staff_id: Optional[str] = None
    email: EmailStr
    name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # permite leer directo del objeto SQLModel