from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.transaction import TxnTypeEnum


class TransactionBase(BaseModel):
    transaction_type: TxnTypeEnum
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    category_id: Optional[int] = Field(None,gt=0)
    date: Optional[datetime] = None

    @field_validator("date")
    def validate_date(cls,value):
        if value and value > datetime.now():
            raise ValueError("Date cannot be in the future")
        return value

class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)
    transaction_type: Optional[TxnTypeEnum] = None
    date: Optional[datetime] = None


class TransactionOut(TransactionBase):
    id: int

    class Config:
        from_attributes = True
