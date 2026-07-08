from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from ...models.user import User
from ...schemas.user import UserCreate, UserResponse

#router con sus tags
router = APIRouter(prefix="/users", tags=["Users"])

#Endpoint get para obtener todos los usuarios
@router.get("/", response_model=list[UserResponse])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

#Endpoint post para crear un nuevo usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user