from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from flasgger import Swagger
import json
import os
import yaml
import logging
from util.searchUtil import search_ip
from util.errorUtil import create_error_response

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Configuring logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', level=logging.INFO, format=log_format)

# Load Swagger documentation from YAML file
swagger_yaml_path = os.path.join("config", "swagger.yaml")
with open(swagger_yaml_path, "r") as swagger_yaml_file:
    swagger_config = yaml.load(swagger_yaml_file, Loader=yaml.FullLoader)
    swagger.template = swagger_config

# Global dictionary to store the prefixes data
prefix_data = {}

# Load data from prefixes.json into the global dictionary
json_file_path = os.path.join("data", "prefixes.json")
with open(json_file_path, "r") as json_file:
    prefix_data = json.load(json_file)

class PrefixSearchResource(Resource):
    def get(self):
        ip_address_str = request.args.get("ip")

        if not ip_address_str:
            error_message = "IP address not provided"
            logging.error(f"Error: {error_message}")
            return create_error_response(error_message, 400)

        result = search_ip(ip_address_str, prefix_data)
        return jsonify({"result": result})

    def post(self):
        data = request.get_json()

        if not data or not data.get("ips"):
            error_message = "List of IP addresses not provided"
            logging.error(f"Error: {error_message}")
            return create_error_response(error_message, 400)

        results = []
        for ip_address_str in data["ips"]:
            result = search_ip(ip_address_str, prefix_data)
            results.extend(result)

        return jsonify({"result": results})
    

api.add_resource(PrefixSearchResource, "/api/v1/prefixes")

if __name__ == "__main__":
    app.run(debug=True)
