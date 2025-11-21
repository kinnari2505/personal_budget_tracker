from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class BudgetBase(BaseModel):
    category_id: int = Field(...,gt=0)
    amount: float = Field(...,ft=0, description="Amount must be greater than 0")
    month: int = Field(..., ge=1, le=12, description="Month must be between 1 and 12")
    year: int = Field(..., ge=2000, le=datetime.now().year+1) #Cannot exceed current year + 1 (ex: budget for next year allowed)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category_id: Optional[int] = Field(None, gt=0)
    amount: Optional[float] = Field(None,gt=0)
    month: Optional[int] = Field(None, ge=1, le=12)
    year: Optional[int] = Field(None, ge=2000, le=datetime.now().year+1)

class BudgetOut(BudgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
