from uuid import UUID

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import models
import schema
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Получение локаольной сессии работы с базой данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get_users", response_model=list[schema.User])
def get_users(db: Session = Depends(get_db)):
    """Запрос на получение списка всех созданных пользователей"""
    return crud.get_users(db)


@app.post("/create")
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """Запрос на создание нового пользователя"""
    return crud.create_user(db=db, user=user)


@app.put("/lock/{user_id}")
def acquire_lock(user_id: UUID, db: Session = Depends(get_db)):
    """Запрос на блокировку пользователя"""
    return crud.lock_user(db, user_id)


@app.put("/unlock/{user_id}")
def release_lock(user_id: UUID, db: Session = Depends(get_db)):
    """Запрос на разблокировку пользователя"""
    return crud.unlock_user(db, user_id)
