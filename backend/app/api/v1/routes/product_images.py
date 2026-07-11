from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.core.database import get_session
from app.models.product import Product
from app.models.product_image import ProductImage
from app.schemas.product_image import ProductImageCreate, ProductImageUpdate, ProductImageResponse

router = APIRouter(tags=["Product Images"])

@router.post("/products/{product_id}/images", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
def create_product_image(product_id: int, payload: ProductImageCreate, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db_image = ProductImage(product_id=product_id, url=payload.url, sort_order=payload.sort_order)
    session.add(db_image)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create product image.")
    session.refresh(db_image)
    return db_image


@router.patch("/product-images/{image_id}", response_model=ProductImageResponse)
def update_product_image(image_id: int, payload: ProductImageUpdate, session: Session = Depends(get_session)):
    db_image = session.get(ProductImage, image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_image, key, value)

    session.commit()
    session.refresh(db_image)
    return db_image


@router.delete("/product-images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_image(image_id: int, session: Session = Depends(get_session)):
    db_image = session.get(ProductImage, image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")

    session.delete(db_image)
    session.commit()
    return None