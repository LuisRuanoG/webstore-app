from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.order import Order
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse

router = APIRouter(tags=["Transactions"])


@router.get("/orders/{order_id}/transactions", response_model=list[TransactionResponse])
def get_all_transactions(order_id: int, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db_transactions = session.exec(
        select(Transaction).where(Transaction.order_id == order_id)
    ).all()
    return db_transactions


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(transaction_id: int, session: Session = Depends(get_session)):
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return db_transaction
