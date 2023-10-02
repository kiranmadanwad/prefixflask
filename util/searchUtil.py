from ipaddress import ip_address, ip_network
import logging

# Configuring logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', level=logging.INFO, format=log_format)

def search_ip(ip_address_str, prefix_data):
    try:
        ip = ip_address(ip_address_str)
    except ValueError:
        error_message = "Invalid IP address format " + ip_address_str
        logging.error(f"Error: {error_message}")
        return [{"error": error_message}]

    # Search for matching prefixes in the loaded data
    matching_results = []
    for provider, prefix_groups in prefix_data.items():
        for group in prefix_groups:
            for prefix in group["prefixes"]:
                if ip in ip_network(prefix, strict=False):
                    matching_results.append(
                        {
                            "subnet": prefix,
                            "provider": provider,
                            "ip": ip_address_str,
                            "tags": group["tags"],
                        }
                    )

    return matching_results
