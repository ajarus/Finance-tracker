# app/db/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, Integer

class Base:
    @declared_attr
    def __tablename__(cls):
        # Автоматическое именование таблиц: User -> users
        return cls.__name__.lower() + 's'
    
    id = Column(Integer, primary_key=True, index=True)

Base = declarative_base(cls=Base)