from uuid import UUID
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
import models, schema


def get_users(db: Session):
    """Получение списка всех пользователей из базы данных"""
    return db.query(models.User).all()


def create_user(db: Session, user: schema.UserCreate):
    """Создание нового пользователя, если он уже не существует"""
    if not db.query(models.User).filter(models.User.id == user.id).first():
        hasher = hashlib.sha512()
        hasher.update(user.password.encode())
        hashed_password = hasher.hexdigest()
        db_user = models.User(id=user.id, create_ad=user.create_ad, login=user.login, password=hashed_password,
                              project_id=user.project_id, env=user.env, domain=user.domain, locktime=None)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return f'Created user {user.login}'
    else:
        return f'User with id {user.id} already exists'


def lock_user(db: Session, user_id: UUID):
    """Попытка блокировки пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user.locktime:
        user.locktime = current_timestamp()
        db.add(user)
        db.commit()
        db.refresh(user)
        return f'User {user_id} is locked now'
    else:
        return f'User {user_id} has been locked since {user.locktime}'


def unlock_user(db: Session, user_id: UUID):
    """Попытка разблокировки польщователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user.locktime:
        user.locktime = None
        db.add(user)
        db.commit()
        db.refresh(user)
        return f'User {user_id} is no longer locked'
    else:
        return f'User {user_id} is not locked now'
