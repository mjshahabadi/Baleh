from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, index=True)
    BaleUserId = Column(String(50), unique=True, index=True)
    FirstName = Column(String(100))
    Username = Column(String(100))
    CreatedAt = Column(DateTime, default=func.now())