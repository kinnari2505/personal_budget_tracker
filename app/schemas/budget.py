from pydantic import BaseModel
from typing import Optional


class BudgetBase(BaseModel):
    category_id: int
    amount: float
    month: int 
    year: int 


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None


class BudgetOut(BudgetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
