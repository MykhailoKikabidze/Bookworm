from sqlalchemy import Column, Integer, String, Boolean
from service.db import Base


class UsersModel(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    login = Column(String, index=True, unique=True)
    password = Column(String)
    is_moder = Column(Boolean, index=True)
