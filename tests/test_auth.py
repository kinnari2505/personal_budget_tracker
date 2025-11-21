import pytest

# -------------------------
# 1. Register user
# -------------------------
def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "username":"testuser",
        "email":"test@gmail.com",
        "password":"password123"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@gmail.com"

# ---------------------------
# 2. Fixture to get token
# ---------------------------
@pytest.fixture
def access_token(client):

    # 1. Create user first
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "is_admin": False
    })
    
    # 2. Login
    response = client.post("/api/auth/token", data={
        "username":"testuser",
        "password":"password123"
    })
    assert  response.status_code == 200
    return response.json()["access_token"]

# ----------------------------------------
# 3. Use token fixture for authenticated requests
# ----------------------------------------
def test_get_user_with_token(client, access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response =  client.get("/api/auth/1", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "testuser"

# ----------------------------------------
# 4. Test admin access protection
# ----------------------------------------
def test_admin_access_denied(client,access_token):

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/auth/", headers=headers)
    assert response.status_code == 403