from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError  # de sqlalchemy.exc, NO de psycopg2
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse

router = APIRouter(prefix="/staff", tags=["Staff"])

# POST endpoint to create a new staff member
@router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(payload: StaffCreate, session: Session = Depends(get_session)):
    # firebase_staff_id no se setea aquí — se queda en None hasta que
    # conectemos el link con Firebase en la fase de seguridad.
    db_staff = Staff(email=payload.email, name=payload.name, role=payload.role)

    session.add(db_staff)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff with this email already exists."
        )
    session.refresh(db_staff)
    return db_staff

# GET endpoint to retrieve all staff members and GET by ID, PATCH to update staff member
@router.get("/", response_model=list[StaffResponse])
def get_all_staff(session: Session = Depends(get_session)):
    db_staff = session.exec(select(Staff)).all()
    return db_staff

# GET endpoint to retrieve a staff member by ID
@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff_by_id(staff_id: int, session: Session = Depends(get_session)):
    db_staff = session.get(Staff, staff_id)
    if not db_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return db_staff

# PATCH endpoint to update a staff member
@router.patch("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, payload: StaffUpdate, session: Session = Depends(get_session)):
    db_staff = session.get(Staff, staff_id)
    if not db_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    # exclude_unset=True: solo pisa los campos que sí vinieron en el request,
    # si no, los que faltan se sobreescriben con None (bug que ya cazamos en products).
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_staff, key, value)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Staff with this email already exists."
        )
    session.refresh(db_staff)
    return db_staff