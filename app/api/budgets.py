from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetUpdate
from app.models.category import Category

router = APIRouter(prefix="/api/budgets", tags=["budgets"])

# ---------------------------
# Create Budget
# ---------------------------
@router.post("/", response_model=BudgetOut)
def create_budget(budget_in: BudgetCreate, db: Session = Depends(get_db),current_user : User = Depends(get_current_user)):

    # Validate category
    if budget_in.category_id:
        category = (
            db.query(Category)
            .filter(
                Category.id == budget_in.category_id,
                Category.user_id == current_user.id,
            )
            .first()
        )
        if not category:
            raise HTTPException(status_code=400, detail="Invalid Category")
    
    budget = Budget(
        user_id =current_user.id,
        category_id=budget_in.category_id,
        amount=budget_in.amount,
        month=budget_in.month,
        year=budget_in.year,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

# ---------------------------
# List Budgets
# ---------------------------
@router.get("/", response_model=List[BudgetOut])
def list_budgets(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return (
        db.query(Budget)
        .filter(Budget.user_id == current_user.id)
        .order_by(Budget.year.desc(),Budget.month.desc())
        .all()
    )

# ---------------------------
# Get Budget by ID
# ---------------------------
@router.get("/{budget_id}", response_model=BudgetOut)
def get_budget(budget_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    budget = (
        db.query(Budget)
        .filter(Budget.id == budget_id,Budget.user_id == current_user.id)
        .first()
    )
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    return budget

# ---------------------------
# Update Budget
# ---------------------------
@router.put("/{budget_id}", response_model=BudgetOut)
def update_budget(budget_id: int,budget_in: BudgetUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == current_user.id
        )
        .first()
    )
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    # Validate category
    if budget.category_id:
        category = (
            db.query(Category)
            .filter(
                Category.id == budget_in.category_id,
                Category.user_id == current_user.id
            )
            .first()
        )
        if not category:
            raise HTTPException(status_code=400, detail="Invalid Category")
        
    budget.amount = budget_in.amount
    budget.month = budget_in.month
    budget.year = budget_in.year
    budget.category_id = budget_in.category_id

    db.commit()
    db.refresh(budget)
    return budget

# ---------------------------
# Delete Budget
# ---------------------------
@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == current_user.id
        )
        .first()
    )
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}
