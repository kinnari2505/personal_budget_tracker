from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user, oauth2_scheme
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.models.category import Category
from app.models.user import User


router =  APIRouter(prefix="/api/categories", tags=["categories"])

# ---------------------------
# Create Category
# ---------------------------
@router.post("/",response_model=CategoryOut)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db), current_user :User = Depends(get_current_user)):
    
    category = Category(name=category_in.name, user_id=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# ---------------------------
# List All Category of the User
# ---------------------------

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Category).filter(Category.user_id == current_user.id).all()

# ---------------------------
# Get Category by ID
# ---------------------------
@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    cat = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

# ---------------------------
# Update Category by id
# ---------------------------
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):

    cat = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Catgeory not found")
    cat.name = category_in.name
    db.commit()
    db.refresh(cat)
    return cat 

# ---------------------------
# Delete Category  by ID
# ---------------------------
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    cat = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"Ok":True}





