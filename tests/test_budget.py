from tests.test_category import register_and_login
import uuid

def setup_user_category(client):
    
    headers = register_and_login(client)
    unique_name = f"cat_{uuid.uuid4().hex[:6]}"
    # create category
    category = client.post("/api/categories/", json={"name":"Food"}, headers=headers).json()
    return headers, category

def test_create_budget(client):
    
    headers, category = setup_user_category(client)

    response = client.post("/api/budgets/", json={
        "category_id": category["id"],
        "amount": 5000,
        "month": 1,
        "year": 2025
    }, headers=headers)

    assert response.status_code == 201
    assert response.json()["amount"] == 5000


def test_duplicate_budget_not_allowed(client):

    headers, category = setup_user_category(client)

    payload = {
        "category_id": category["id"],
        "amount": 3000,
        "month": 1,
        "year": 2025
    }

    client.post("/api/budgets/", json=payload, headers=headers)
    response = client.post("/api/budgets/", json=payload, headers=headers)
    assert response.status_code == 400 # unique per user/category/month

def test_get_budgets(client):

    headers = register_and_login(client)

    response = client.get("/api/budgets/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(),list)