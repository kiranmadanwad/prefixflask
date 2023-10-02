from flask import Flask
from util.errorUtil import create_error_response

def test_create_error_response():
    # Create a Flask app context
    app = Flask(__name__)
    with app.app_context():
        response = create_error_response("Test Error", 404)
        assert response.status_code == 404
        assert response.headers["Content-Type"] == "application/json"
        assert response.get_json() == {"error": "Test Error"}
