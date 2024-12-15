from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db import Base


class UsersModel(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    login = Column(String, index=True, unique=True)
    password = Column(String)
    is_moder = Column(Boolean, index=True)

    books_checkpoints = relationship(
        "BookModel", secondary="checkpoints", back_populates="users_checkpoints"
    )
    books_notes = relationship(
        "BookModel", secondary="notes", back_populates="users_notes"
    )
