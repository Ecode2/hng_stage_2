from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from requests import Response
from ..main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_login(client = Depends(client)):
    response: Response = client.post("/auth/login",
        json={"email": "ecode5814@gmail.com",
            "password": "2005abubakar"}
        )
    access_token = response.json().get("access_token")
    assert response.status_code == 200
    assert access_token != None

