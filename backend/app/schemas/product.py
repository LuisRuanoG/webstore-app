from typing import Optional
from pydantic import BaseModel, Field

# 1. EL MOLDE PADRE: Contiene los datos que comparten la entrada y la salida
class ProductBase(BaseModel):
    name: str = Field(..., description="Nombre del producto")
    description: str = Field(..., description="Descripción detallada")
    price: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    image_url: Optional[str] = None


# 2. EL MOLDE DE ENTRADA (Para POST / PUT): Se usa cuando React nos envía datos
# Nota: No tiene ID porque la base de datos lo genera sola al guardar
class ProductCreate(ProductBase):
    pass  # Hereda todo lo de ProductBase sin cambios adicionales


# 3. EL MOLDE DE SALIDA (Para GET): Lo que FastAPI le responde a tu Axios
# Nota: Aquí SÍ incluimos el ID porque el producto ya existe en la base de datos
class ProductResponse(ProductBase):
    id: int

    # Esta pequeña configuración le permite a Pydantic leer los datos
    # directamente desde tu base de datos (SQLModel/SQLAlchemy) y transformarlos a JSON
    model_config = {"from_attributes": True}