from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from slugify import slugify  # pip install python-slugify

from app.core.database import get_session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate



router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, session: Session = Depends(get_session)):
    db_category = Category(
        name=payload.name,
        slug=slugify(payload.name)
    )
    session.add(db_category)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists."
        )
    session.refresh(db_category)
    return db_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(session: Session = Depends(get_session)):
    # Ejecuta un 'SELECT * FROM categories' en tu base de datos
    categories = session.query(Category).all()
    return categories

# Endpoint para actualizar una categoría existente
@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryUpdate, session: Session = Depends(get_session)):
    db_category = session.query(Category).filter(Category.categories_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if payload.name is not None:
        db_category.name = payload.name
        db_category.slug = slugify(payload.name)
    
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists."
        )
    
    session.refresh(db_category)
    return db_category

