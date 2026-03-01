"""
API Key Diagnostic Script
Verifies that the API key is being sent correctly
"""

import requests
import json
import urllib3
from core.config_manager import ConfigManager
from core.data_parser import DataParser
from core.test_executor import TestExecutor

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 80)
print("API Key Diagnostic Test")
print("=" * 80)

# Load configuration
config_manager = ConfigManager()
config = config_manager.load_config()

print("\n1. Configuration Loaded:")
print("-" * 80)
for key, value in config.items():
    if 'KEY' in key.upper():
        print(f"  {key}: {value[:10]}...{value[-10:] if len(value) > 20 else ''}")
    else:
        print(f"  {key}: {value}")

# Parse test data
data_parser = DataParser()
test_data_list = data_parser.parse_file("Test_Data/test-data.csv")

print(f"\n2. Test Data Parsed: {len(test_data_list)} tests found")
print("-" * 80)

# Get first test
if test_data_list:
    first_test = test_data_list[0]
    print(f"First test: {first_test.get('test_name', 'Unknown')}")
    print(f"Body: {json.dumps(first_test.get('body'), indent=2)}")

# Create executor
executor = TestExecutor(config)

print("\n3. Test Executor Configuration:")
print("-" * 80)
print(f"API_BASE_URL: {executor.config.get('API_BASE_URL', 'NOT SET')}")
print(f"API_ENDPOINT: {executor.config.get('API_ENDPOINT', 'NOT SET')}")
print(f"API_KEY: {executor.config.get('API_KEY', 'NOT SET')[:10]}...{executor.config.get('API_KEY', '')[-10:]}")
print(f"CORRELATION_ID: {executor.config.get('CORRELATION_ID', 'NOT SET')}")

# Manually build request to see what's being sent
if test_data_list:
    test_data = test_data_list[0]
    
    # Build URL
    base_url = test_data.get('base_url') or executor.config.get('API_BASE_URL', '')
    endpoint = test_data.get('endpoint') or executor.config.get('API_ENDPOINT', '')
    url = f"{base_url}{endpoint}"
    
    # Build headers
    headers = executor._parse_headers(test_data.get('headers', ''))
    
    # Add API key if not present
    if executor.config.get('API_KEY') and 'API-KEY' not in headers:
        headers['API-KEY'] = executor.config['API_KEY']
    
    # Add correlation ID
    if executor.config.get('CORRELATION_ID') and 'Correlation-ID' not in headers:
        headers['Correlation-ID'] = executor.config['CORRELATION_ID']
    
    # Prepare body
    body = test_data.get('body', '')
    request_body = executor._prepare_body(body)
    
    print("\n4. Request Details:")
    print("-" * 80)
    print(f"URL: {url}")
    print(f"\nHeaders:")
    for key, value in headers.items():
        if 'KEY' in key.upper():
            print(f"  {key}: {value[:10]}...{value[-10:] if len(value) > 20 else ''}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\nRequest Body (first 500 chars):")
    print(request_body[:500])
    
    print("\n5. Sending Request...")
    print("-" * 80)
    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=request_body,
            timeout=30,
            verify=False
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Size: {len(response.content)} bytes")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! API returned 200")
        else:
            print(f"\n❌ FAILED! API returned {response.status_code}")
            print(f"\nResponse (first 500 chars):")
            print(response.text[:500])
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("Diagnostic Complete")
print("=" * 80)

