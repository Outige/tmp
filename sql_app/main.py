from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import sql_app.crud as crud
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Route to delete all the users
- Just added this in so we can clean the database and repopulate it for the unit tests.
- I don't actually like this way of doing it. We would obviously need some kind of
unit test db when doing the real thing. Also I don't like in general that such a route
exists.
- Also note something else I don't like: crud.get_users is limited to 100 as default.
Can we remove that so we can return all entries? Maybe that just doesn't scale nicely.
- I was also unable to pass setup_file as part of the json like I can pass the other args for UserCreate for example.
"""
@app.get("/test/")#, response_model=schemas.User)
def test_route(setup_file: str = '../sql_app/setup.sql', db: Session = Depends(get_db)):
    sqlstr = open(setup_file).read()
    db.execute(sqlstr)
    db.commit()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items