from typing import Annotated
from sqlalchemy.orm import Session, defer
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status
from passlib.context import CryptContext

from pydantic import BaseModel, Field
from models import Users
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

class UserPassword(BaseModel):
    password: str = Field(
        min_length=4,
        # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$",
        description="New password to reset"

    )

@router.get('/user', status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detial='Authentication Failed.')
    
    stmt = select(Users).filter(Users.id == user.get('id')).options(defer(Users.hashed_password), defer(Users.is_active))

    return db.scalars(stmt).first()

@router.put('/user/change-password/', status_code=status.HTTP_201_CREATED)
async def change_password(user: user_dependency, db: db_dependency, new_password: UserPassword):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    stmt = select(Users).where(Users.id == user.get('id'))

    user_model = db.scalars(stmt).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No User Found.')

    user_model.hashed_password = bcrypt_context.hash(new_password.password)

    db.commit()

    db.refresh(user_model)

    return user_model

    
