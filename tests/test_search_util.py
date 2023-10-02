from util.searchUtil import search_ip
from ipaddress import ip_address

def test_search_ip_valid():
    # Test a valid IPv4 address in a matching subnet
    ip_address_str = "192.124.249.1"
    prefix_data = {
        "provider1": [{"prefixes": ["192.124.249.0/24"], "tags": ["tag1"]}],
    }

    results = search_ip(ip_address_str, prefix_data)
    assert len(results) == 1
    assert results[0]["ip"] == ip_address_str

def test_search_ip_invalid_format():
    # Test an invalid IP address format
    ip_address_str = "invalid_ip_format"
    prefix_data = {
        "provider1": [{"prefixes": ["192.124.249.0/24"], "tags": ["tag1"]}],
    }

    results = search_ip(ip_address_str, prefix_data)
    assert len(results) == 1
    assert "error" in results[0]

def test_search_ip_no_match():
    # Test an IP address that doesn't match any prefix
    ip_address_str = "10.0.0.1"
    prefix_data = {
        "provider1": [{"prefixes": ["192.124.249.0/24"], "tags": ["tag1"]}],
    }

    results = search_ip(ip_address_str, prefix_data)
    assert len(results) == 0

def test_search_ip_multiple_matches():
    # Test an IP address that matches multiple prefixes
    ip_address_str = "3.11.53.1"
    prefix_data = {
        "provider1": [{"prefixes": ["3.11.53.0/24"], "tags": ["tag1"]}],
        "provider2": [{"prefixes": ["3.8.0.0/14"], "tags": ["tag2"]}],
    }

    results = search_ip(ip_address_str, prefix_data)
    assert len(results) == 2
    # Verify the specific results based on your data
    assert results[0]["provider"] == "provider1"
    assert results[1]["provider"] == "provider2"
