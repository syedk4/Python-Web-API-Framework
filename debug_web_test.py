"""
Debug script to simulate web application test execution
"""

from core.config_manager import ConfigManager
from core.data_parser import DataParser
from core.test_executor import TestExecutor
from core.report_generator import ReportGenerator

print("=" * 80)
print("Web Application Test Execution Debug")
print("=" * 80)

# Simulate what the web application does
config_manager = ConfigManager()
data_parser = DataParser()
report_generator = ReportGenerator()

# Load configuration (same as web app)
config = config_manager.load_config()
print("\n1. Configuration Loaded:")
print("-" * 80)
for key, value in config.items():
    if key == 'API_KEY':
        print(f"  {key}: {value[:10]}...")
    else:
        print(f"  {key}: {value}")

# Parse test data (same as web app)
test_file = "test-data.csv"
test_data_list = data_parser.parse_file(f"Test_Data/{test_file}")
print(f"\n2. Test Data Parsed:")
print("-" * 80)
print(f"  Number of tests: {len(test_data_list)}")
print(f"  First test: {test_data_list[0].get('test_name', 'Unknown')}")

# Create executor (same as web app)
executor = TestExecutor(config)

# Progress callback (same as web app)
progress_data = []
def progress_callback(progress):
    progress_data.append(progress)
    print(f"  [{progress['current']}/{progress['total']}] {progress['test_name']}: {progress['status']}")

print(f"\n3. Executing Tests:")
print("-" * 80)

# Execute tests (same as web app)
results = executor.execute_tests(test_data_list, progress_callback)

# Get summary (same as web app)
summary = executor.get_summary()
print(f"\n4. Test Summary:")
print("-" * 80)
print(f"  Total: {summary['total']}")
print(f"  Passed: {summary['passed']}")
print(f"  Failed: {summary['failed']}")
print(f"  Pass Rate: {summary['pass_rate']}%")

# Generate report (same as web app)
html_report = report_generator.generate_html_report(
    executor.get_results(),
    summary
)
report_path = report_generator.save_report(html_report)

print(f"\n5. Report Generated:")
print("-" * 80)
print(f"  Report path: {report_path}")

# Check individual results
print(f"\n6. Individual Test Results:")
print("-" * 80)
for i, result in enumerate(executor.get_results(), 1):
    status = "✅ PASS" if result['passed'] else "❌ FAIL"
    print(f"  {i}. {result['test_name']}: {status}")
    print(f"     Status: {result['status_code']} (Expected: {result['expected_status']})")
    if result['error']:
        print(f"     Error: {result['error'][:100]}")

# Check progress callback data
print(f"\n7. Progress Callback Data:")
print("-" * 80)
print(f"  Total progress updates: {len(progress_data)}")
if progress_data:
    last_progress = progress_data[-1]
    print(f"  Last progress update:")
    print(f"    Current: {last_progress['current']}")
    print(f"    Total: {last_progress['total']}")
    print(f"    Passed: {last_progress['passed']}")
    print(f"    Failed: {last_progress['failed']}")
    print(f"    Status: {last_progress['status']}")

print("\n" + "=" * 80)
print("Debug Complete")
print("=" * 80)

