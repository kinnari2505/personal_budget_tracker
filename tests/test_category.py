def register_and_login(client):
    # Register
    client.post("/api/auth/register", json={
        "username":"user1",
        "email":"user1@example.com",
        "password":"pwd123"
    })
    # Login
    response = client.post("/api/auth/token", data={
        "username":"user1",
        "password":"pwd123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_category(client):
    
    headers = register_and_login(client)
    response = client.post("/api/categories/", json={
        "name":"Food"
    }, headers=headers)

    assert  response.status_code == 201
    assert response.json()["name"] == "Food"


def test_get_categories(client):

    headers = register_and_login(client)
    response = client.get("/api/categories", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_category_by_id(client):

    headers = register_and_login(client)
    
    # create category
    cat = client.post("/api/categories/", json={"name": "Travel"}, headers=headers).json()

    response = client.get(f"/api/categories/{cat['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Travel"

def test_delete_category(client):

    headers = register_and_login(client)

    # create category
    cat = client.post("/api/categories/", json={"name": "Rent"}, headers=headers).json()

    # delete
    response = client.delete(f"/api/categories/{cat['id']}", headers=headers)
    assert response.status_code == 204

