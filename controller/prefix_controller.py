from flask import jsonify, make_response, request
from flask_restful import Resource
from services.search_service import SearchService
from util.errorUtil import create_error_response

class PrefixSearchController(Resource):
    def __init__(self, search_service):
        self.search_service = search_service

    def get(self):
        ip_address_str = request.args.get("ip")

        if not ip_address_str:
            error_message = "IP address not provided"
            return create_error_response(error_message, 400)

        result = self.search_service.search_ip(ip_address_str)
        return jsonify({"result": result})

    def post(self):
        data = request.get_json()

        if not data or not data.get("ips"):
            error_message = "List of IP addresses not provided"
            return create_error_response(error_message, 400)

        results = []
        for ip_address_str in data["ips"]:
            result = self.search_service.search_ip(ip_address_str)
            results.extend(result)

        return jsonify({"result": results})
