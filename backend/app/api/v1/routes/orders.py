from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.customer import Customer
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, session: Session = Depends(get_session)):
    db_customer = session.get(Customer, payload.customer_id)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    db_order = Order(customer_id=payload.customer_id, delivery_note=payload.delivery_note)

    session.add(db_order)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create order."
        )
    session.refresh(db_order)
    return db_order


@router.get("/", response_model=list[OrderResponse])
def get_all_orders(session: Session = Depends(get_session)):
    db_orders = session.exec(select(Order)).all()
    return db_orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return db_order


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, payload: OrderUpdate, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update order."
        )
    session.refresh(db_order)
    return db_order
