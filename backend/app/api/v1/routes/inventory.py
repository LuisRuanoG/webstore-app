from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.staff import Staff
from app.schemas.inventory import InventoryCreate, InventoryResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(payload: InventoryCreate, session: Session = Depends(get_session)):
    db_product = session.get(Product, payload.product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db_staff = session.get(Staff, payload.staff_id)
    if not db_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    db_inventory = Inventory(
        product_id=payload.product_id,
        staff_id=payload.staff_id,
        reason=payload.reason,
        change_amount=payload.change_amount,
        reference_id=payload.reference_id,
    )
    db_product.stock_quantity += payload.change_amount

    session.add(db_inventory)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create inventory record."
        )
    session.refresh(db_inventory)
    return db_inventory


@router.get("/", response_model=list[InventoryResponse])
def get_all_inventory(product_id: Optional[int] = None, session: Session = Depends(get_session)):
    statement = select(Inventory)
    if product_id is not None:
        statement = statement.where(Inventory.product_id == product_id)

    db_inventory = session.exec(statement).all()
    return db_inventory
