from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase


class BaseSQL(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
