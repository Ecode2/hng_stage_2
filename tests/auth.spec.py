from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.testclient import TestClient
import jwt
from ..main import app
from ..utils import create_access_token

SECRET_KEY = "testing_secret_key"
ALGORITHM = "HS256"

client = TestClient(app)


# Unit Test
def test_create_jwt_token():
    user_id = "user123"
    expires_delta = timedelta(minutes=15)

    token = create_access_token({"user_id": user_id}, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == user_id
    assert datetime.utcfromtimestamp(decoded_token["exp"]) < datetime.utcnow() + expires_delta

def test_organization_access():
    user1_token = client.post("/auth/register", json={"firstName": "elias", "lastName": "code", "email": "ecode@example.com", "password": "password"}).json()["access_token"]
    user2_token = client.post("/auth/register", json={"firstName": "Jane", "lastName": "Doe", "email": "jane@example.com", "password": "password"}).json()["access_token"]

    org_response = client.post("/organizations", headers={"Authorization": f"Bearer {user1_token}"}, json={"name": "elias's Organisation"})
    org_id = org_response.json()["orgId"]

    response = client.get(f"/organizations/{org_id}", headers={"Authorization": f"Bearer {user2_token}"})
    assert response.status_code == 403


#End-to-End testing
def test_register_user_successfully():
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "password": "password"
    })
    assert response.status_code == 201
    data = response.json()["data"]
    assert "accessToken" in data
    assert data["user"]["email"] == "john@example.com"

    new_response = client.get(f"/organizations/{data["user"]["organisation_id"][0]}", headers={"Authorization": f"Bearer {data["accessToken"]}"}).json()
    assert new_response["name"] == "John's Organisation"

def test_login_user_successfully():
    response = client.post("/auth/login", data={"elias": "ecode@example.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert "accessToken" in data
    assert data["user"]["email"] == "ecode@example.com"

def test_missing_fields_registration():
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com"
        # Missing password
    })
    assert response.status_code == 422
    assert "password" in response.json()["detail"][0]["loc"]

def test_duplicate_email_registration():
    response = client.post("/auth/register", json={
        "firstName": "NewJohn",
        "lastName": "NewDoe",
        "email": "newjohn@example.com",
        "password": "password"
    })
    assert response.status_code == 201

    response = client.post("/auth/register", json={
        "firstName": "NewJohn",
        "lastName": "NewDoe",
        "email": "newjohn@example.com",
        "password": "password"
    })
    assert response.status_code == 400
