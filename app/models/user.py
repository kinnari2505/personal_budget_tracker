'''
This class defines a users table using SQLAlchemy ORM.
Each user has: id, username, email, hashed_password

Relationships: A user can have multiple categories, transactions, and budgets.
back_populates connects both sides of the relationship.
cascade="all, delete-orphan" ensures child records are cleaned up when a user is deleted.
'''

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    categories =  relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all,delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")