from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

# Al poner tags=["Products"], FastAPI creará la sección exclusiva en tu /docs
router = APIRouter(prefix="/products", tags=["Products"])


#endpoint to get all products
@router.get("/", response_model=list[ProductResponse])
def get_products(session: Session = Depends(get_session)): # 👈 Agregamos la sesión
    db_products = session.exec(select(Product)).all()
    return db_products # 👈 FastAPI lo convierte automáticamente al formato de ProductResponse


#endpoint para get por id
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

#endpoint para POST para crear un producto, add try/except for IntegrityError
@router.post("/", response_model=ProductResponse)
def create_product(product_in: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.model_validate(product_in)
    session.add(db_product)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Product with this SKU already exists."
        )
    session.refresh(db_product)
    return db_product

#PATCH endpoint to update a product agregar try/except for IntegrityError
@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_in: ProductUpdate, session: Session = Depends   (get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_in.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Product with this SKU already exists."
        )
    
    session.refresh(db_product)
    return db_product


