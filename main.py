# from typing import Annotated
# from sqlalchemy.orm import Session
# from sqlalchemy import select, insert, update, delete
from fastapi import FastAPI, Depends, HTTPException, Path
# from starlette import status

import models
# from models_todo import ToDoRequest
# from models import Todos
from database import engine#, SessionLocal
from routers import auth, todos, admin, users

app = FastAPI() 

models.Base.metadata.create_all(bind=engine)

app.include_router(router=auth.router)
app.include_router(router=todos.router)
app.include_router(router=admin.router)
app.include_router(router=users.router)

# def get_db():
#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]


# @app.get("/")
# async def read_all(db:db_dependency):
# # This Depends keyword takes care of calling get_db function, opening the connection, and once used, close it afterwards.
#     # db.query(DB_NAME).all()/any other SQL Method
#     return db.scalars(select(Todos)).all()

# @app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def get_todo_item(db: db_dependency, todo_id: int = Path(gt=0)):
#     get_todo_by_id_statement = select(Todos).where(Todos.id == todo_id)
#     todo_model_data = db.scalars(get_todo_by_id_statement).first()

#     if todo_model_data is not None:
#         return todo_model_data
    
#     raise HTTPException(status_code=404, detail='Todo Task not found.')

# @app.post("/todos/add", status_code = status.HTTP_201_CREATED)
# async def add_todo(db: db_dependency, todo_request: ToDoRequest):
#     # new_task_to_add = ToDoItem(**todo_request.model_dump())
#     # new_task_to_add = {key: value for key, value in new_task_to_add.__dict__.items() if key != 'id'}
    
#     # add_statement_to_db = insert(Todos).values(new_task_to_add.__dict__)
    
#     # with db.begin():
#     #     db.execute(add_statement_to_db)

#     new_task_to_add = Todos(**todo_request.model_dump())
#     db.add(new_task_to_add)

#     db.commit()

#     db.refresh(new_task_to_add)


# @app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db: db_dependency, todo_request: ToDoRequest, todo_id: int = Path(gt=0)):
#     # task_to_update = Todos(**todo_request.model_dump())

#     get_todo_by_id_statement = select(Todos).where(Todos.id == todo_id)
#     todo_model_data = db.scalars(get_todo_by_id_statement).first()
#     change_made = False

#     if todo_model_data is not None:

#         # stmt = update(Todos).where(Todos.id == todo_model_data.id).values(task_to_update.__dict__)

#         # with db.begin():
#         #     db.execute(stmt)
        
#         todo_model_data.title = todo_request.title
#         todo_model_data.description = todo_request.description
#         todo_model_data.priority = todo_request.priority
#         todo_model_data.complete = todo_request.complete
        
#         db.add(todo_model_data)
#         db.commit()
#         db.refresh(todo_model_data)

#         change_made = True

#     if not change_made:
#         raise HTTPException(status_code=404, detail='Task ID not available.')


# @app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     get_todo_by_id_statement = select(Todos).where(Todos.id == todo_id)
#     todo_model_data = db.scalars(get_todo_by_id_statement).first()

#     if todo_model_data is None:
#         raise HTTPException(status_code=404, detail='Task ID not available.')
    
#     else:
#         # delete_statment_by_id = delete(Todos).filter(Todos.id == todo_id)
#         db.delete(todo_model_data)

#         db.commit()





