
🚀 VHostFather - The Ultimate VHost Enumeration & Port Scanning Tool 🚀

![VHostFather](https://img.shields.io/badge/python-v3.9%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

## 🌟 Overview
**VHostFather** is a powerful Python-based tool designed to streamline VHost enumeration and port scanning. Combining the speed of `masscan` for high-speed port discovery with HTTP/HTTPS service detection, VHostFather helps you identify potential vulnerabilities in web applications using virtual hosts.

VHostFather: **“I'm your father... of VHost enumeration!”** 👾

---

## 📋 Features
- ⚡ **High-Speed Port Scanning** using `masscan` (rate of 50,000 packets/second).
- 🌐 **HTTP/HTTPS Detection** with a 3-second timeout for service availability.
- 🛠️ **VHost Enumeration** to detect differences in web responses between IP and VHost requests.
- 🚀 **Optimized Output**:
  - Displays only VHost responses that differ in size from the IP response.
  - Automatically handles SSL certificate warnings.
- 🖥️ **Cross-Platform** and lightweight — works on Linux, macOS, and Windows.

---

## 📦 Installation

### Prerequisites
Ensure you have the following tools installed:
- **Python 3.9+**
- **`masscan`** for high-speed port scanning
- **`requests`** Python library for HTTP/HTTPS requests

### Install Dependencies
```bash
pip install requests
```

### Installing `masscan`
On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install masscan
```

---

## 🚀 Usage

### Basic Usage
```bash
python3 vhostfather.py ip.txt vhost.txt
```

### Input Files
- **`ip.txt`**: A list of IP addresses, one per line.
  ```
  192.168.1.10
  10.0.0.5
  172.16.0.25
  ```
- **`vhost.txt`**: A list of virtual hosts, one per line.
  ```
  example.com
  subdomain.example.com
  testsite.local
  ```

### Example Output
```
[*] Scanning all IPs from ip.txt with masscan...
[+] Scan completed. Found 46 open ports.
[+] Page size for https://192.168.1.10:443 without VHost: 3000 bytes
[+] Page size for assets.example.com on https://192.168.1.10:443: 1823 bytes
[+] Page size for api.example.com on https://192.168.1.10:443: 1920 bytes
```

---

## ⚙️ Command-Line Options
```
Usage: python3 vhostfather.py ip.txt vhost.txt

Parameters:
    ip.txt      - File containing a list of IP addresses, one per line
    vhost.txt   - File containing a list of virtual hosts, one per line
```

---

## 🛠️ How It Works
1. **Port Scanning**:
   - Uses `masscan` to scan all ports (1-65535) on each IP address from `ip.txt` with a rate of 50,000 packets/second.
2. **HTTP/HTTPS Detection**:
   - Checks if open ports support HTTP (80) or HTTPS (443).
3. **VHost Enumeration**:
   - Performs GET requests to each IP and VHost.
   - Displays VHost responses only if their size differs from the base IP response.

---

## 📂 Project Structure
```
VHostFather/
├── vhostfather.py       # Main script
├── ip.txt          # Sample IP file
├── vhost.txt       # Sample VHost file
└── README.md       # Project documentation
```

---

## 🛡️ Security & Limitations
- Ensure you have permission before running scans on any external network.
- Use responsibly and in compliance with applicable laws.

---

## 📜 License
This project is licensed under the MIT License.

---

## 🛠️ Contributing
Contributions are welcome! Feel free to open issues, submit pull requests, or suggest new features.

---

## 🤝 Acknowledgements
Special thanks to the creators of `masscan` and `requests` for providing the powerful tools that made VHostFather possible!

---

## ✨ Inspiration
**“I'm your father... of VHost enumeration!”**

---

Happy Hacking! 🚀👾
