"""
Test script to verify template variable replacement
"""

from core.data_parser import DataParser
import json

print("=" * 80)
print("Template Variable Replacement Test")
print("=" * 80)

# Parse the InvoiceExtraction-TestCases.csv file
parser = DataParser()
test_data_list = parser.parse_file("Test_Data/InvoiceExtraction-TestCases.csv")

print(f"\n1. Parsed {len(test_data_list)} tests from InvoiceExtraction-TestCases.csv")
print("-" * 80)

# Check first test
first_test = test_data_list[0]
print(f"\nFirst test: {first_test['test_name']}")
print(f"Body type: {type(first_test['body'])}")
print(f"Body content:")
print(json.dumps(first_test['body'], indent=2))

# Simulate what the web app does
language = 'EN-US'

print(f"\n2. Applying template replacement (language={language}):")
print("-" * 80)

for test_data in test_data_list:
    body = test_data.get('body')
    
    # Handle both dict and list body formats
    if isinstance(body, dict):
        # Replace template variables
        if 'environment' in body and body['environment'] == '{{environment}}':
            body['environment'] = 'AFI'
        if 'languageCheck' in body:
            body['languageCheck'] = language
            
    elif isinstance(body, list):
        # Body is a list (from dynamic CSV format)
        for item in body:
            if isinstance(item, dict):
                # Replace template variables
                if 'environment' in item and item['environment'] == '{{environment}}':
                    item['environment'] = 'AFI'
                if 'languageCheck' in item:
                    item['languageCheck'] = language

# Check first test after replacement
first_test_after = test_data_list[0]
print(f"\nFirst test after replacement:")
print(f"Body content:")
print(json.dumps(first_test_after['body'], indent=2))

# Verify replacement worked
body = first_test_after['body']
if isinstance(body, list) and len(body) > 0:
    item = body[0]
    if isinstance(item, dict):
        env = item.get('environment')
        lang = item.get('languageCheck')
        
        print(f"\n3. Verification:")
        print("-" * 80)
        print(f"Environment: {env} (Expected: AFI)")
        print(f"Language: {lang} (Expected: {language})")
        
        if env == 'AFI' and lang == language:
            print("\n✅ Template replacement working correctly!")
        else:
            print("\n❌ Template replacement FAILED!")
            if env != 'AFI':
                print(f"   - Environment is '{env}' instead of 'AFI'")
            if lang != language:
                print(f"   - Language is '{lang}' instead of '{language}'")
else:
    print("\n❌ Body format unexpected!")

print("\n" + "=" * 80)
print("Test Complete")
print("=" * 80)

