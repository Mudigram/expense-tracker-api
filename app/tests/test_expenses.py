from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_expense():
    # 1. Registration
    client.post("/api/v1/auth/register/", json={
        "username": "testuser10000",
        "email": "test10000@example.com",
        "password": "password10000"
    })

    # 2. Log in
    login_response = client.post(
        "/api/v1/auth/login", 
        data={"identifier": "testuser10000", "password": "password10000"} 
    )
    
    # Check if login actually returned data
    resp_data = login_response.json()
    print(f"Login Response Body: {resp_data}") # Check if access_token exists here
    
    token = resp_data.get("access_token")
    assert token is not None, "Access token was not found in login response!"

    # 3. Create expense
    headers = {"Authorization": f"Bearer {token}"}
    expense_payload = {"amount": 100.0, "category": "Food", "description": "Lunch"}
    response = client.post("/api/v1/expenses/", json=expense_payload, headers=headers)
    
    if response.status_code != 201:
        print(f"Expense Creation Failed: {response.json()}")
        
    assert response.status_code == 201