from uuid import UUID

from pydantic import BaseModel, PastDate

from enums import Environments, Domains


class UserBase(BaseModel):
    """Базовая схема работы с пользователем. Используется для взаимодействия сс пользователем по ID"""
    id: UUID


class User(UserBase):
    """Схема для чтения данных о пользователе. Не подразумевает передачу пароля."""
    create_ad: PastDate
    login: str
    project_id: UUID
    env: Environments
    domain: Domains

    class Config:
        from_attributes = True


class UserCreate(User):
    """Схема для создания пользователя через внесение полной информации о нем"""
    password: str
