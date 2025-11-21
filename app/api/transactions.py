from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut

router = APIRouter(prefix="/api/transactions", tags=['transactions'])

# ---------------------------
# Create a Transaction
# ---------------------------
@router.post("/", response_model=TransactionOut,status_code=201)
def create_transaction(tx_in: TransactionCreate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):

    category = None
    # If category_id is provided, verify it belongs to this user
    if tx_in.category_id is not None:
        category = (
            db.query(Category)
            .filter(Category.id == tx_in.category_id,
            Category.user_id == current_user.id,
            ).first())
    
        if not category:
            raise HTTPException(status_code=400, detail="Invalid Category")
    
    tx = Transaction(
        user_id=current_user.id,
        category_id=tx_in.category_id,
        transaction_type=tx_in.transaction_type,
        amount=tx_in.amount,
        date=tx_in.date,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx 

# ---------------------------
# List All Transactions of the User
# ---------------------------
@router.get("/", response_model=List[TransactionOut])
def list_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    return(
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .all()
    )

# ---------------------------
# Get Specific Transaction
# ---------------------------
@router.get("/{tx_id}", response_model=TransactionOut)
def get_transaction(tx_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    tx = (
        db.query(Transaction)
        .filter(Transaction.id == tx_id,Transaction.user_id == current_user.id,)
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx 

# ---------------------------
# Update Transaction
# ---------------------------
@router.put("/{tx_id}",response_model=TransactionOut)
def update_transaction(
    tx_id: int,
    tx_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    tx = (
        db.query(Transaction)
        .filter(Transaction.id == tx_id, Transaction.user_id == current_user.id)
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Validate category
    if tx_in.category_id:
        category = (
            db.query(Category)
            .filter(
                Category.id == tx_in.category_id,
                Category.user_id == current_user.id
            )
            .first()
        )
        if not category:
            raise HTTPException(status_code=400, detail="Invalid Category")
    
    # Apply updates safely
    if tx_in.transaction_type is not None:
        tx.transaction_type = tx_in.transaction_type
    if tx_in.amount is not None:
        tx.amount = tx_in.amount
    if tx_in.category_id is not None:
        tx.category_id = tx_in.category_id
    if tx_in.date is not None:
        tx.date = tx_in.date

    db.commit()
    db.refresh(tx)
    return tx 

# ---------------------------
# Delete Transaction
# ---------------------------
@router.delete("/{tx_id}")
def delete_transaction(tx_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    tx = (
        db.query(Transaction)
        .filter(
            Transaction.id == tx_id,
            Transaction.user_id == current_user.id,
        )
        .first()
    )
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(tx)
    db.commit()
    return {"message": "Transaction deleted successfully"}
