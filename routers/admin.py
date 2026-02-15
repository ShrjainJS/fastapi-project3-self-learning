from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from models_todo import ToDoRequest
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    return db.scalars(select(Todos)).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    stmt = select(Todos).where(Todos.id == todo_id)

    data_model_returned = db.scalars(statement=stmt).first()

    if data_model_returned is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task Not Found.')
    
    db.delete(data_model_returned)

    db.commit()
    
