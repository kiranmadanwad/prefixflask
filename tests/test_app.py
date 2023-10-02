import json
import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from app import PrefixSearchResource, app, prefix_data

class TestPrefixSearchResource(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_get_valid_ip(self):
        ip_address = "192.124.249.1"
        response = self.app.get(f"/api/v1/prefixes?ip={ip_address}")
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", data)

    def test_get_invalid_ip(self):
        invalid_ip = "invalid_ip"
        response = self.app.get(f"/api/v1/prefixes?ip={invalid_ip}")
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)        
        self.assertIn("result", data)
        result_data = data["result"]        
        self.assertEqual(len(result_data), 1)
        error_item = result_data[0]        
        self.assertIn("error", error_item)
        self.assertEqual(error_item["error"], "Invalid IP address format invalid_ip")

    @patch("app.search_ip")  # Mock the search_ip function
    def test_post_valid_ips(self, mock_search_ip):
        mock_search_ip.return_value = [{"subnet": "192.124.249.0/24", "provider": "Sucuri", "ip": "192.124.249.1", "tags": ["Cloud", "CDN/WAF"]}]
        request_data = {"ips": ["192.124.249.1"]}
        response = self.app.post("/api/v1/prefixes", json=request_data)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", data)

    def test_post_invalid_data(self):
        invalid_data = {}
        response = self.app.post("/api/v1/prefixes", json=invalid_data)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
