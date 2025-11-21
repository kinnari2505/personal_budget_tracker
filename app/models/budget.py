from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Budget(Base):

    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"),nullable=True)
    amount = Column(Float, nullable=False)
    month = Column(Integer,nullable=False)
    year = Column(Integer, nullable=False)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category",back_populates="budgets")