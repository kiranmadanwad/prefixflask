from flask import Flask
from flask_restful import Api
from flasgger import Swagger
import json
import os
import yaml
import logging
from services.search_service import SearchService
from controller.prefix_controller import PrefixSearchController
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


# Global list to store flattened prefixes data
flattened_prefix_data = []

# Load data from prefixes.json into the global list of dictionaries
json_file_path = os.path.join("data", "prefixes.json")
with open(json_file_path, "r") as json_file:
    prefix_data = json.load(json_file)
    
    for provider, prefix_groups in prefix_data.items():
        for group in prefix_groups:
            for prefix in group["prefixes"]:
                flattened_prefix_data.append({
                    "provider": provider,
                    "prefix": prefix,
                    "tags": group["tags"]
                })

# Initialize the service and controller
search_service = SearchService(flattened_prefix_data)
prefix_search_controller = PrefixSearchController(search_service)

api.add_resource(PrefixSearchController, "/api/v1/prefixes", resource_class_kwargs={'search_service': search_service})

if __name__ == "__main__":
    app.run(debug=True)
