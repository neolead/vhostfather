import os
import subprocess
import sys
import requests
from requests.exceptions import RequestException
import urllib3

# Disable InsecureRequestWarning warnings from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_help():
    """Prints usage instructions."""
    print("""
Usage: python3 vhostfather.py ip.txt vhost.txt [--offline]

Parameters:
    ip.txt       - File containing a list of IP addresses, one per line (or ip:port pairs if --offline is specified)
    vhost.txt    - File containing a list of virtual hosts, one per line
    --offline    - Optional flag to use a pre-scanned list of ip:port pairs from ip.txt

Description:
    This script performs the following steps:
    1. Scans all IPs and ports (1-65535) from ip.txt using masscan with a rate of 50,000 packets/second if --offline is not specified.
    2. Checks which IP:port combinations are available for HTTP/HTTPS.
    3. Makes GET requests to each IP and checks if different VHosts return different content sizes.
    4. Outputs only when the VHost response size differs from the base IP response size.
""")
    sys.exit(1)

def run_masscan(input_file, output_file):
    """Runs masscan to scan all ports on all IPs from the input file."""
    try:
        print(f"[*] Scanning all IPs from {input_file} with masscan...")
        subprocess.run([
            'masscan', '-iL', input_file, '-p1-65535', '--rate', '50000', '-oL', output_file
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error running masscan: {e}")
        return False
    return True

def parse_masscan_output(file):
    """Parses masscan output and returns a list of IP:port pairs."""
    if not os.path.exists(file):
        print(f"[-] File {file} not found.")
        return []

    results = []
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('open'):
                parts = line.split()
                if len(parts) >= 4:
                    ip = parts[3]
                    port = parts[2]
                    results.append(f"{ip}:{port}")
    return results

def check_http_https(ip, port):
    """Checks if a given port on the IP returns a valid HTTP/HTTPS response."""
    # First, check HTTPS
    print(f"[*] Checking HTTPS on {ip}:{port}")
    url_https = f"https://{ip}:{port}"
    try:
        response = requests.get(url_https, timeout=5, verify=False)
        print(f"[+] HTTPS check on {ip}:{port} returned status code: {response.status_code}")
        return "https"
    except RequestException:
        pass  # Do not print error message

    # Then, check HTTP
    print(f"[*] Checking HTTP on {ip}:{port}")
    url_http = f"http://{ip}:{port}"
    try:
        response = requests.get(url_http, timeout=5, verify=False)
        print(f"[+] HTTP check on {ip}:{port} returned status code: {response.status_code}")
        return "http"
    except RequestException:
        pass  # Do not print error message

    return None

def get_vhosts(vhost_file):
    """Reads VHosts from a file and returns them as a list."""
    with open(vhost_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_page_size(url, host=None):
    """Performs a GET request and returns the size of the response content."""
    headers = {}
    if host:
        headers['Host'] = host

    try:
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        return len(response.content)
    except RequestException:
        return None

def main(ip_file, vhost_file, offline):
    masscan_output = 'masscan_output.txt'
    ip_port_file = 'ip_tmp.txt'

    # Step 1: If offline mode, use ip_file directly as the list of ip:port pairs
    if offline:
        print(f"[*] Using {ip_file} as a list of IP:port pairs in offline mode.")
        # Check if the file exists and contains ip:port pairs
        if not os.path.exists(ip_file):
            print(f"[-] Error: {ip_file} does not exist or is not a valid file.")
            sys.exit(1)
        with open(ip_file, 'r') as f:
            pairs = [line.strip() for line in f if line.strip()]
        if not pairs:
            print(f"[-] Error: {ip_file} is empty or does not contain valid IP:port pairs.")
            sys.exit(1)
    else:
        # Step 2: Run masscan to scan all ports
        if not run_masscan(ip_file, masscan_output):
            print("[-] Error during masscan scanning.")
            return

        # Step 3: Parse masscan results
        pairs = parse_masscan_output(masscan_output)
        with open(ip_port_file, 'w') as f:
            for pair in pairs:
                f.write(pair + '\n')

        print(f"[+] Scan completed. Found {len(pairs)} open ports.")

    # Step 4: Read VHosts from file
    vhosts = get_vhosts(vhost_file)

    # Step 5: Check each IP:port pair for HTTP/HTTPS availability
    for entry in pairs:
        if ':' not in entry:
            print(f"[-] Invalid IP:port entry: {entry}")
            continue
        ip, port_str = entry.split(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            print(f"[-] Invalid port number: {port_str} for IP: {ip}")
            continue

        # Check HTTP/HTTPS availability
        protocol = check_http_https(ip, port)
        if not protocol:
            continue

        url = f"{protocol}://{ip}:{port}"

        # Get base page size without Host header
        base_size = get_page_size(url)
        if base_size is None:
            print(f"[-] Failed to get page size for {url}")
            continue

        print(f"[+] Page size for {url} without VHost: {base_size} bytes")

        # Check sizes for each VHost
        vhost_sizes = {}
        for vhost in vhosts:
            size = get_page_size(url, host=vhost)
            if size is not None and size != base_size:
                vhost_sizes[vhost] = size

        # Output only if VHost sizes differ from the base size
        if vhost_sizes:
            for vhost, size in vhost_sizes.items():
                print(f"[+] Page size for {vhost} on {url}: {size} bytes")

if __name__ == "__main__":
    # Check for correct usage
    if len(sys.argv) < 3:
        print_help()

    ip_file = sys.argv[1]
    vhost_file = sys.argv[2]
    offline = '--offline' in sys.argv

    if not os.path.exists(ip_file) or not os.path.exists(vhost_file):
        print("[-] Error: One or both input files do not exist.")
        sys.exit(1)

    main(ip_file, vhost_file, offline)
