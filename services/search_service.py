from ipaddress import ip_address, ip_network
import logging

class SearchService:
    def __init__(self, flattened_prefix_data):
        self.flattened_prefix_data = flattened_prefix_data

    def search_ip(self, ip_address_str):
        try:
            ip = ip_address(ip_address_str)
        except ValueError:
            error_message = "Invalid IP address format " + ip_address_str
            logging.error(f"Error: {error_message}")
            return [{"error": error_message}]

        matching_results = []
        for entry in self.flattened_prefix_data:
            prefix = entry["prefix"]
            if ip in ip_network(prefix, strict=False):
                matching_results.append(
                    {
                        "subnet": prefix,
                        "provider": entry["provider"],
                        "ip": ip_address_str,
                        "tags": entry["tags"],
                    }
                )

        return matching_results
