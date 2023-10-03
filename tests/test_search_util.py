import unittest
from ipaddress import ip_network
from util.searchUtil import search_ip

class TestSearchUtil(unittest.TestCase):

    def test_search_ip_valid_ip(self):
        ip_address_str = "192.168.1.5"
        flattened_prefix_data = [
            {"provider": "provider1", "prefix": "192.168.1.0/24", "tags": ["tag1"]},
            {"provider": "provider2", "prefix": "10.0.0.0/8", "tags": ["tag2"]}
        ]

        result = search_ip(ip_address_str, flattened_prefix_data)
        expected_result = [
            {"subnet": "192.168.1.0/24", "provider": "provider1", "ip": "192.168.1.5", "tags": ["tag1"]}
        ]
        self.assertEqual(result, expected_result)

    def test_search_ip_invalid_ip(self):
        ip_address_str = "invalid_ip_format"
        flattened_prefix_data = [
            {"provider": "provider1", "prefix": "192.168.1.0/24", "tags": ["tag1"]}
        ]

        result = search_ip(ip_address_str, flattened_prefix_data)
        expected_result = [{"error": "Invalid IP address format invalid_ip_format"}]
        self.assertEqual(result, expected_result)

    def test_search_ip_no_matching_prefix(self):
        ip_address_str = "192.168.2.5"
        flattened_prefix_data = [
            {"provider": "provider1", "prefix": "192.168.1.0/24", "tags": ["tag1"]}
        ]

        result = search_ip(ip_address_str, flattened_prefix_data)
        expected_result = []
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
