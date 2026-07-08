from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

# Al poner tags=["Products"], FastAPI creará la sección exclusiva en tu /docs
router = APIRouter(prefix="/products", tags=["Products"])


# 1. El endpoint de lectura consulta PostgreSQL y devuelve la lista filtrada por el Schema
@router.get("/", response_model=list[ProductResponse])
def get_products(session: Session = Depends(get_session)): # 👈 Agregamos la sesión aquí
    # Ejecuta un 'SELECT * FROM products' en tu base de datos
    products = session.exec(select(Product)).all()
    return products # 👈 FastAPI lo convierte automáticamente al formato de ProductResponse


# 2. El endpoint de creación recibe los datos validados de React y los guarda en la BD
@router.post("/", response_model=ProductResponse)
def create_product(product_in: ProductCreate, session: Session = Depends(get_session)):
    # Convertimos el esquema de validación (Schema) en un modelo real de Base de Datos (Model)
    db_product = Product.model_validate(product_in)
    
    # Abrimos la transacción y guardamos en PostgreSQL
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    
    # Devolvemos el producto guardado (FastAPI lo filtrará con el Schema ProductResponse)
    return db_product