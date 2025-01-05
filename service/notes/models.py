from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from db import Base


class CheckpointModel(Base):
    __tablename__ = "checkpoints"

    id_user = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    id_book = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    page = Column(Integer)


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    id_book = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    page = Column(Integer, index=True)
    description = Column(String)
    quote = Column(String)
    character = Column(Integer)


class GroupModel(Base):
    __tablename__ = "groups"

    id_user = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    id_book = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    is_favourite = Column(Boolean)
    want_to_read = Column(Boolean)
    now_reading = Column(Boolean)
    have_read = Column(Boolean)
