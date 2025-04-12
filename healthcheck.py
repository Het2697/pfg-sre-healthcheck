#!/usr/bin/env python3

import requests
import socket
import ssl
import csv
import time
from datetime import datetime
from urllib.parse import urlparse

# Configuration
ENDPOINTS = ["https://ac.pfgltd.com/testhealth", "https://secure.pfgltd.com/testhealth"]
CSV_FILE = "health_data.csv"
DURATION_MINUTES = 60

# Functions
def get_internal_ip():
    return socket.gethostbyname(socket.gethostname())

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Unavailable"

def get_endpoint_ip(url):
    hostname = urlparse(url).hostname
    try:
        return socket.gethostbyname(hostname)
    except:
        return "DNS_Fail"

def get_latency_and_status(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start) * 1000, 2)  # milliseconds
        status = response.status_code
        return latency, status
    except requests.exceptions.RequestException:
        return None, "DOWN"

def get_cert_expiry(url):
    hostname = urlparse(url).hostname
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                return expire_date.strftime('%Y-%m-%d')
    except:
        return "Cert_Error"

def write_header():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Timestamp_Local",
            "Endpoint",
            "Internal_IP",
            "External_IP",
            "Endpoint_IP",
            "Latency_ms",
            "HTTP_Status",
            "Cert_Expiry"
        ])

def append_row(data):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Main logic
def main():
    write_header()
    for _ in range(DURATION_MINUTES):
        # Get the current time in the local time zone
        timestamp = datetime.now(ZoneInfo("America/New_York")).isoformat()
        internal_ip = get_internal_ip()
        external_ip = get_external_ip()

        for url in ENDPOINTS:
            endpoint_ip = get_endpoint_ip(url)
            latency, status = get_latency_and_status(url)
            cert_expiry = get_cert_expiry(url)
            row = [timestamp, url, internal_ip, external_ip, endpoint_ip, latency, status, cert_expiry]
            append_row(row)


if __name__ == "__main__":
    main()
