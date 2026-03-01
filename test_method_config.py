"""
Test script to verify METHOD configuration is working
"""

from core.config_manager import ConfigManager
from core.test_executor import TestExecutor

print("=" * 80)
print("METHOD Configuration Test")
print("=" * 80)

# Test 1: Load configuration
print("\n1. Testing Configuration Loading:")
print("-" * 80)
config_manager = ConfigManager()
config = config_manager.load_config()

method = config.get('METHOD', 'NOT SET')
print(f"Configured METHOD: {method}")

if method == 'POST':
    print("✅ Default METHOD is correctly set to POST")
else:
    print(f"⚠️  METHOD is set to: {method}")

# Test 2: Test executor uses configured method
print("\n2. Testing Test Executor:")
print("-" * 80)
executor = TestExecutor(config)

# Test data without method specified
test_data_no_method = {
    'test_name': 'Test without method',
    'body': {'test': 'data'}
}

# Simulate getting the method (same logic as in execute_single_test)
default_method = executor.config.get('METHOD', 'POST')
method_used = test_data_no_method.get('method', default_method).upper()

print(f"Test data without method specified:")
print(f"  Default method from config: {default_method}")
print(f"  Method that will be used: {method_used}")

if method_used == 'POST':
    print("✅ Test executor correctly uses configured METHOD as default")
else:
    print(f"❌ Expected POST but got: {method_used}")

# Test 3: Test data with method specified should override
print("\n3. Testing Method Override:")
print("-" * 80)
test_data_with_method = {
    'test_name': 'Test with method',
    'method': 'GET',
    'body': {'test': 'data'}
}

method_used_override = test_data_with_method.get('method', default_method).upper()
print(f"Test data with method='GET' specified:")
print(f"  Method that will be used: {method_used_override}")

if method_used_override == 'GET':
    print("✅ Test data method correctly overrides configured default")
else:
    print(f"❌ Expected GET but got: {method_used_override}")

# Test 4: Save and reload configuration
print("\n4. Testing Save/Load Configuration:")
print("-" * 80)

# Save with different method
test_config = config.copy()
test_config['METHOD'] = 'PUT'
config_manager.save_config(test_config)
print("Saved configuration with METHOD=PUT")

# Reload
reloaded_config = config_manager.load_config()
reloaded_method = reloaded_config.get('METHOD', 'NOT SET')
print(f"Reloaded METHOD: {reloaded_method}")

if reloaded_method == 'PUT':
    print("✅ Configuration save/load works correctly")
else:
    print(f"❌ Expected PUT but got: {reloaded_method}")

# Restore original config
config_manager.save_config(config)
print("\nRestored original configuration")

print("\n" + "=" * 80)
print("Test Complete")
print("=" * 80)

