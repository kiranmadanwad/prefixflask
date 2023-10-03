from ipaddress import ip_address, ip_network
import logging

# Configuring logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', level=logging.INFO, format=log_format)

def search_ip(ip_address_str, flattened_prefix_data):
    try:
        ip = ip_address(ip_address_str)
    except ValueError:
        error_message = "Invalid IP address format " + ip_address_str
        logging.error(f"Error: {error_message}")
        return [{"error": error_message}]

    # Search for matching prefixes in the loaded data
    matching_results = []
    for entry in flattened_prefix_data:
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
