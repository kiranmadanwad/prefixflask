import pytest
from flask import Flask
from flask.testing import FlaskClient
from services.search_service import SearchService
from controller.prefix_controller import PrefixSearchController
from app import api, app

@pytest.fixture
def client():
    # Create a Flask test client
    with app.test_client() as client:
        yield client

@pytest.fixture
def search_service():
    return SearchService([
            {"provider": "provider1", "prefix": "192.168.1.0/24", "tags": ["tag1"]},
            {"provider": "provider2", "prefix": "10.0.0.0/8", "tags": ["tag2"]}
        ])

def test_get_valid_ip(client, search_service):
    controller = PrefixSearchController(search_service)
    response = client.get("/api/v1/prefixes?ip=192.168.1.5")
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] == []

def test_get_invalid_ip(client, search_service):
    controller = PrefixSearchController(search_service)
    response = client.get("/api/v1/prefixes?ip=invalid_ip_format")

    assert response.status_code == 200
    data = response.get_json()
    result_data = data["result"]        
    assert len(result_data) == 1
    error_item = result_data[0]
    assert error_item["error"] == "Invalid IP address format invalid_ip_format"

def test_post_valid_ips(client, search_service):
    controller = PrefixSearchController(search_service)
    data = {"ips": ["192.168.1.5", "10.0.0.1"]}
    response = client.post("/api/v1/prefixes", json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] == []

def test_post_invalid_ips(client, search_service):
    controller = PrefixSearchController(search_service)
    response = client.post("/api/v1/prefixes", json={})

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
