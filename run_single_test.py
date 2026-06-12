"""
Quick Test Runner for Single Test Case
Runs a specific test case from CSV file without web interface
"""

import sys
from core.config_manager import ConfigManager
from core.data_parser import DataParser
from core.test_executor import TestExecutor


def run_single_test(test_file, test_id):
    """Run a single test case by test_id"""

    print("=" * 80)
    print(f"Running Test: {test_id}")
    print("=" * 80)
    print()

    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Parse test data
    data_parser = DataParser()
    test_data_list = data_parser.parse_file(test_file)

    # Filter for specific test
    target_test = None
    for test_data in test_data_list:
        if test_data.get('test_id') == test_id:
            target_test = test_data
            break

    if not target_test:
        print(f"❌ Test {test_id} not found in {test_file}")
        return

    print(f"Found test: {target_test.get('test_name', 'Unnamed test')}")
    print()
    print("DEBUG - Raw test_data keys:")
    for key in sorted(target_test.keys()):
        value = target_test.get(key)
        if key == 'body':
            print(f"  {key}: {str(value)[:300]}")
        else:
            print(f"  {key}: {value}")
    print()
    print("Request Details:")
    print(f"  Method: {target_test.get('method')}")
    print(f"  URL: {target_test.get('base_url')}{target_test.get('endpoint')}")
    print(f"  Schema: {target_test.get('expected_response_schema')}")
    print(f"  Custom Validator: {target_test.get('custom_validator')}")
    print()

    # Execute the test
    executor = TestExecutor(config)
    result = executor.execute_single_test(target_test, 1)

    # Print results
    print()
    print("=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Test ID: {target_test.get('test_id', 'N/A')}")
    print(f"Test Name: {result.test_name}")
    print(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
    print(f"Expected Status: {result.expected_status}")
    print(f"Actual Status: {result.status_code}")
    print(f"Response Time: {result.response_time:.3f}s")
    print(f"Response Size: {result.response_size} bytes")
    print()

    if result.message:
        print("Message:")
        print(result.message)
        print()

    if result.error:
        print("Error:")
        print(result.error)
        print()

    if result.validation_errors:
        print("Validation Errors:")
        for error in result.validation_errors:
            print(f"  - {error}")
        print()

    # Print response snippet
    if result.response_body:
        print("Response (first 800 chars):")
        print(result.response_body[:800])
        if len(result.response_body) > 800:
            print("... (truncated)")
        print()

    print("=" * 80)

    return result.passed


if __name__ == '__main__':
    # Default values
    test_file = 'Test_Data/FA-739-test-schema.csv'
    test_id = 'TC_005'

    # Allow command line arguments
    if len(sys.argv) > 1:
        test_id = sys.argv[1]
    if len(sys.argv) > 2:
        test_file = sys.argv[2]

    success = run_single_test(test_file, test_id)
    sys.exit(0 if success else 1)
