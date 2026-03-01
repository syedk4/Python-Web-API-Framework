"""
API Diagnostic Script
Tests the API directly to see what error is being returned
"""

import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
API_BASE_URL = "http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction"
API_ENDPOINT = "/PDFViewer"
API_KEY = "0b4b24cf-0211-4deb-8f2f-280ab556ca78"
CORRELATION_ID = "test"

# Test data (from first test case)
test_body = {
    'environment': 'AFI',
    'customerNumber': '9946600',
    'shipTo': 'D63',
    'invoiceNumber': '40756307',
    'orderNumber': 'C746966',
    'languageCheck': 'EN-US'
}

# Build request
url = f"{API_BASE_URL}{API_ENDPOINT}"
headers = {
    'Content-Type': 'application/json',
    'API-KEY': API_KEY,
    'Correlation-ID': CORRELATION_ID
}

# Wrap in array as the API expects
body_array = [test_body]

print("=" * 80)
print("API Diagnostic Test")
print("=" * 80)
print(f"\nURL: {url}")
print(f"\nHeaders:")
for key, value in headers.items():
    if key == 'API-KEY':
        print(f"  {key}: {value[:10]}...{value[-10:]}")
    else:
        print(f"  {key}: {value}")

print(f"\nRequest Body:")
print(json.dumps(body_array, indent=2))

print("\n" + "=" * 80)
print("Sending Request...")
print("=" * 80)

try:
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(body_array),
        timeout=30,
        verify=False
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Size: {len(response.content)} bytes")
    print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    
    print(f"\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nResponse Body:")
    print("-" * 80)
    try:
        # Try to parse as JSON
        response_json = response.json()
        print(json.dumps(response_json, indent=2))
    except:
        # If not JSON, print as text
        print(response.text)
    print("-" * 80)
    
except requests.exceptions.Timeout:
    print("\n❌ ERROR: Request timed out")
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ ERROR: Connection failed - {e}")
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("Diagnostic Complete")
print("=" * 80)

