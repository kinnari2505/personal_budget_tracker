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
@router.post("/", response_model=BudgetOut,status_code=201)
def create_budget(budget_in: BudgetCreate, db: Session = Depends(get_db),current_user : User = Depends(get_current_user)):

    # Validate category belongs to user
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
    
    # Prevent duplicate budget for same month+year+category
    existing = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category_id == budget_in.category_id,
        Budget.month == budget_in.month,
        Budget.year == budget_in.year
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Budget already exists for this category in the selected month/year."
        )

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
def update_budget(budget_id: int,budget_in: BudgetUpdate, 
                  db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):

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
    
    # Validate new category
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
    
    # Prevent duplicate for updated values
    new_category = budget_in.category_id or budget.category_id
    new_month = budget_in.month or budget.month
    new_year = budget_in.year or budget.year 

    duplicate = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category_id == new_category,
        Budget.month == new_month,
        Budget.year == new_year,
        Budget.id !=  budget_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Another budget already exists for this category/month/year."
        )
    
    # Apply updates
    if budget_in.amount is not None: 
        budget.amount = budget_in.amount
    if budget_in.month is not None:
        budget.month = budget_in.month
    if budget_in.year is not None:
        budget.year = budget_in.year
    if budget_in.category_id is not None:
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
