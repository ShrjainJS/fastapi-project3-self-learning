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
    prefix='/tasks',
    tags=['todos']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def read_all(user: user_dependency, db:db_dependency):
# This Depends keyword takes care of calling get_db function, opening the connection, and once used, close it afterwards.
    # db.query(DB_NAME).all()/any other SQL Method
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    return db.scalars(select(Todos).filter(Todos.owner_id == user.get('id'))).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    get_todo_by_id_statement = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)
    todo_model_data = db.scalars(get_todo_by_id_statement).first()

    if todo_model_data is not None:
        return todo_model_data
    
    raise HTTPException(status_code=404, detail='Todo Task not found.')

@router.post("/todos", status_code = status.HTTP_201_CREATED)
async def add_todo(user: user_dependency, db: db_dependency, todo_request: ToDoRequest):
    # new_task_to_add = ToDoItem(**todo_request.model_dump())
    # new_task_to_add = {key: value for key, value in new_task_to_add.__dict__.items() if key != 'id'}
    
    # add_statement_to_db = insert(Todos).values(new_task_to_add.__dict__)
    
    # with db.begin():
    #     db.execute(add_statement_to_db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')

    new_task_to_add = Todos(**todo_request.model_dump(), owner_id = user.get('id'))
    db.add(new_task_to_add)

    db.commit()

    db.refresh(new_task_to_add)


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: ToDoRequest, todo_id: int = Path(gt=0)):
    # task_to_update = Todos(**todo_request.model_dump())

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    
    get_todo_by_id_statement = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)
    todo_model_data = db.scalars(get_todo_by_id_statement).first()
    change_made = False

    if todo_model_data is not None:

        # stmt = update(Todos).where(Todos.id == todo_model_data.id).values(task_to_update.__dict__)

        # with db.begin():
        #     db.execute(stmt)
        
        todo_model_data.title = todo_request.title
        todo_model_data.description = todo_request.description
        todo_model_data.priority = todo_request.priority
        todo_model_data.complete = todo_request.complete
        
        db.add(todo_model_data)
        db.commit()
        db.refresh(todo_model_data)

        change_made = True

    if not change_made:
        raise HTTPException(status_code=404, detail='Task ID not available.')


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    get_todo_by_id_statement = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)
    todo_model_data = db.scalars(get_todo_by_id_statement).first()

    if todo_model_data is None:
        raise HTTPException(status_code=404, detail='Task ID not available.')
    
    else:
        # delete_statment_by_id = delete(Todos).filter(Todos.id == todo_id)
        db.delete(todo_model_data)

        db.commit()


