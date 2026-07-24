from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, session: Session = Depends(get_session)):
    db_customer = Customer(email=payload.email, name=payload.name, phone=payload.phone)

    session.add(db_customer)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists."
        )
    session.refresh(db_customer)
    return db_customer


@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(session: Session = Depends(get_session)):
    db_customers = session.exec(select(Customer)).all()
    return db_customers


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id: int, session: Session = Depends(get_session)):
    db_customer = session.get(Customer, customer_id)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate, session: Session = Depends(get_session)):
    db_customer = session.get(Customer, customer_id)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_customer, key, value)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update customer."
        )
    session.refresh(db_customer)
    return db_customer
