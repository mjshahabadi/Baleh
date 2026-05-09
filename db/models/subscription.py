from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from db.models.user import Base

class Subscription(Base):
    __tablename__ = "Subscriptions"

    Id = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey("Users.Id"))
    PlanId = Column(Integer)
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=func.now())