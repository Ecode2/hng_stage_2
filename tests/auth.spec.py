from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

def test_login():
    response = client.post("/auth/login",
        json={"email": "user@example.com",
            "password": "string"}
        )
    access_token = response.json().get("access_token")
    assert access_token != None