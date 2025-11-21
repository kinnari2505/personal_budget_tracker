'''
| Component                 | Meaning                                       |
| ------------------------- | --------------------------------------------- |
| `create_engine`           | Creates database connection engine            |
| `SessionLocal`            | Creates database sessions from the engine     |
| `SQLALCHEMY_DATABASE_URL` | Specifies which database we are using         |
| `check_same_thread=False` | Needed for SQLite to allow multithread access |
| `autocommit=False`        | Requires manual commit()                      |
| `autoflush=False`         | Does not automatically flush changes          |
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./budget.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)