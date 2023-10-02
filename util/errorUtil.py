
from flask import make_response
import json

def create_error_response(message, status_code):
    response_data = {"error": message}
    response = make_response(json.dumps(response_data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response