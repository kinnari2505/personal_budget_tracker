from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.transaction import TxnTypeEnum


class TransactionBase(BaseModel):
    transaction_type: TxnTypeEnum
    amount: float
    category_id: Optional[int] = None
    date: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category_id: Optional[int] = None
    transaction_type: Optional[TxnTypeEnum] = None
    date: Optional[datetime] = None


class TransactionOut(TransactionBase):
    id: int

    class Config:
        from_attributes = True
