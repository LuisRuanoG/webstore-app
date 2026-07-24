from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.core.database import get_session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order_item import OrderItemCreate, OrderItemResponse

router = APIRouter(tags=["Order Items"])


@router.post("/orders/{order_id}/items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def create_order_item(order_id: int, payload: OrderItemCreate, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db_product = session.get(Product, payload.product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    unit_price = db_product.price
    subtotal = unit_price * payload.quantity
    db_order_item = OrderItem(
        order_id=order_id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        unit_price=unit_price,
        subtotal=subtotal,
    )

    session.add(db_order_item)
    db_order.total_amount += subtotal
    session.add(db_order)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create order item."
        )
    session.refresh(db_order_item)
    return db_order_item
