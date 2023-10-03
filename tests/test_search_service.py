import pytest
from services.search_service import SearchService
from ipaddress import ip_network

@pytest.fixture
def flattened_prefix_data():
    return [
        {"provider": "Provider1", "prefix": "192.168.1.0/24", "tags": ["tag1", "tag2"]},
        {"provider": "Provider2", "prefix": "10.0.0.0/8", "tags": ["tag3", "tag4"]}        
    ]

def test_search_ip_valid(flattened_prefix_data):
    search_service = SearchService(flattened_prefix_data)
    result = search_service.search_ip("192.168.1.5")
    assert len(result) == 1
    assert result[0]["subnet"] == "192.168.1.0/24"
    assert result[0]["provider"] == "Provider1"
    assert result[0]["ip"] == "192.168.1.5"
    assert result[0]["tags"] == ["tag1", "tag2"]

def test_search_ip_invalid(flattened_prefix_data):
    search_service = SearchService(flattened_prefix_data)
    result = search_service.search_ip("172.16.0.1")
    assert result == []

def test_search_ip_invalid_format(flattened_prefix_data):
    search_service = SearchService(flattened_prefix_data)
    result = search_service.search_ip("invalid_ip_format")
    assert len(result) == 1
    assert "error" in result[0]
