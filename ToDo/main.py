from fastapi import FastAPI, Depends, Path, HTTPException
from starlette import status
from models import Base, Todo
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from typing import Annotated
from pydantic import BaseModel, Field
from routers.auth import router as auth_router
app = FastAPI()
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=1000)
    priority: int = Field(gt=0,lt=6)
    complete: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dp_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/read_all")
async def read_all(db: dp_dependecy):
      return db.query(Todo).all()

@app.get("/get_by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: dp_dependecy, todo_id: int=Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: dp_dependecy, todo_request: TodoRequest):
    todo = Todo(**todo_request.dict())
    db.add(todo)
    db.commit()

@app.put("/update_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: dp_dependecy,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()

@app.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async  def delete_todo(db: dp_dependecy, todo_id: int = Path(gt=0)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    db.delete(todo)
    db.commit()














def hello_world():
    return 'Hello World!'

HelloDependency = Annotated[str, Depends(hello_world)]
def get_hello_world(hello: HelloDependency):
    return f"Hello {hello}"

@app.get('/hello')
def hello(message: str = Depends(get_hello_world)):
    return {'message': message}


