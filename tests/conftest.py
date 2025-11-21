import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app 
from app.db.base import Base
from app.api.deps import get_db

# ----------------------------
# Create TEST database (SQLite)
# ----------------------------
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------
# Override get_db dependency
# ----------------------------
def override_get_db():
    
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
        db.close()

# apply override
app.dependency_overrides[get_db] = override_get_db

# Run before tests → create tables
@pytest.fixture(scope="session", autouse=True)
def create_test_ab():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# ----------------------------
# Provide TestClient
# ----------------------------
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
