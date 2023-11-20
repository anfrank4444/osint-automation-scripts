import os
import subprocess
import requests
import json

# Input domain to investigate
domain = "example.com"

# Create a directory to store results
os.makedirs(domain, exist_ok=True)

# Perform a DNS lookup
dns_results = subprocess.check_output(["nslookup", domain]).decode("utf-8")
with open(f"{domain}/dns_lookup.txt", "w") as dns_file:
    dns_file.write(dns_results)

# Perform a WHOIS lookup
whois_results = subprocess.check_output(["whois", domain]).decode("utf-8")
with open(f"{domain}/whois.txt", "w") as whois_file:
    whois_file.write(whois_results)

# Fetch SSL certificate information
ssl_info = subprocess.check_output(["openssl", "s_client", "-connect", f"{domain}:443"], stderr=subprocess.DEVNULL).decode("utf-8")
with open(f"{domain}/ssl_info.txt", "w") as ssl_file:
    ssl_file.write(ssl_info)

# Perform an HTTP request to retrieve website headers
try:
    response = requests.head(f"http://{domain}")
    headers = response.headers
    with open(f"{domain}/http_headers.json", "w") as headers_file:
        json.dump(dict(headers), headers_file, indent=4)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

# Perform a subdomain enumeration using Sublist3r
subdomain_results = subprocess.check_output(["python", "Sublist3r.py", "-d", domain]).decode("utf-8")
with open(f"{domain}/subdomains.txt", "w") as subdomains_file:
    subdomains_file.write(subdomain_results)

print("OSINT data collection complete.")
