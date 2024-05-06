from sqlalchemy import UUID, Column, Date, String, TIMESTAMP, Enum
from enums import Environments, Domains
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True)
    create_ad = Column(Date)
    login = Column(String)
    password = Column(String)
    project_id = Column(UUID)
    env = Column(Enum(Environments))
    domain = Column(Enum(Domains))
    locktime = Column(TIMESTAMP)