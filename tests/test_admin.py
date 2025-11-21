from tests.test_category import register_and_login


def create_admin(client):

    client.post("/api/auth/register", json={
        "username":"admin1",
        "email":"admin@gmail.com",
        "password":"admin123",
        "is_admin":True
    })

    response = client.post("/api/auth/token", data={
        "username":"admin1",
        "password":"admin123"
    })

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_admin_can_get_users(client):

    headers =  create_admin(client)
    response = client.get("/api/auth/", headers=headers)
    assert isinstance(response.json(), list)

def test_non_admin_cannot_get_users(client):

    headers = register_and_login(client)
    response = client.get("/api/auth/", headers=headers)
    assert response.status_code == 403