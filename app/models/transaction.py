from sqlalchemy import Column, Integer, ForeignKey, Enum as sqlEnum, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
from  enum import Enum 
from sqlalchemy import func

class TxnTypeEnum(str, Enum):
    
    income = "income"
    expense = "expense"

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"),nullable=True)
    transaction_type = Column(sqlEnum(TxnTypeEnum),nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
