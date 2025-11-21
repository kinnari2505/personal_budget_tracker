from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api import auth, categories, transactions, budgets

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Budget Tracker API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(budgets.router)

