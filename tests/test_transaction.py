from tests.test_category import register_and_login

def setup_category(client):

    headers = register_and_login(client)
    category = client.post("/api/categories/",json={"name":"Shopping"},headers=headers).json()
    return headers, category

def test_create_transactions(client):

    headers, cat =  setup_category(client)
    response = client.post("/api/transactions/", json={
        "amount": 1500,
        "transaction_type":"expense",
        "category_id": cat["id"]
    },headers=headers)

    assert response.status_code == 201
    assert response.json()["amount"] == 1500
    assert response.json()["transaction_type"] == "expense"


def test_get_transactions(client):

    headers = register_and_login(client)
    response = client.get("/api/transactions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

