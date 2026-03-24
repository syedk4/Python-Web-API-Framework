"""
CSV Verification Script
Verifies that the generated CSV has the correct base_url and endpoint values
"""

import csv
import os
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

def verify_csv(csv_path, expected_base_url, expected_endpoint):
    """
    Verify CSV file has correct base_url and endpoint
    
    Args:
        csv_path: Path to CSV file
        expected_base_url: Expected base URL value
        expected_endpoint: Expected endpoint value
    """
    
    if not os.path.exists(csv_path):
        print(f"{Fore.RED}❌ CSV file not found: {csv_path}")
        print(f"{Fore.YELLOW}💡 Generate scenarios first using the Scenario Generator")
        return False
    
    try:
        # Read CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            scenarios = list(reader)
        
        if not scenarios:
            print(f"{Fore.RED}❌ CSV file is empty!")
            return False
        
        # Print header
        print("=" * 80)
        print(f"{Fore.CYAN}{Style.BRIGHT}CSV VERIFICATION RESULTS")
        print("=" * 80)
        print(f"{Fore.WHITE}File: {csv_path}")
        print(f"{Fore.WHITE}Total scenarios: {len(scenarios)}")
        print("=" * 80)
        
        # Check first scenario
        first = scenarios[0]
        print(f"\n{Fore.CYAN}{Style.BRIGHT}First Scenario Details:")
        print(f"{Fore.WHITE}Test ID: {first.get('test_id', 'N/A')}")
        print(f"{Fore.WHITE}Test Name: {first.get('test_name', 'N/A')}")
        print(f"{Fore.WHITE}Method: {first.get('method', 'N/A')}")
        print(f"{Fore.WHITE}Base URL: {first.get('base_url', 'N/A')}")
        print(f"{Fore.WHITE}Endpoint: {first.get('endpoint', 'N/A')}")
        
        # Verify base_url
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Verification:")
        print("-" * 80)
        
        actual_base_url = first.get('base_url', '')
        actual_endpoint = first.get('endpoint', '')
        
        base_url_correct = actual_base_url == expected_base_url
        endpoint_correct = actual_endpoint == expected_endpoint
        
        # Base URL check
        if base_url_correct:
            print(f"{Fore.GREEN}✅ Base URL is CORRECT!")
            print(f"{Fore.GREEN}   {actual_base_url}")
        else:
            print(f"{Fore.RED}❌ Base URL is WRONG!")
            print(f"{Fore.YELLOW}   Expected: {expected_base_url}")
            print(f"{Fore.RED}   Actual:   {actual_base_url}")
        
        # Endpoint check
        if endpoint_correct:
            print(f"{Fore.GREEN}✅ Endpoint is CORRECT!")
            print(f"{Fore.GREEN}   {actual_endpoint}")
        else:
            print(f"{Fore.RED}❌ Endpoint is WRONG!")
            print(f"{Fore.YELLOW}   Expected: {expected_endpoint}")
            print(f"{Fore.RED}   Actual:   {actual_endpoint}")
        
        # Check all scenarios
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Checking All Scenarios:")
        print("-" * 80)
        
        all_base_urls = set(s.get('base_url', '') for s in scenarios)
        all_endpoints = set(s.get('endpoint', '') for s in scenarios)
        
        if len(all_base_urls) == 1:
            print(f"{Fore.GREEN}✅ All scenarios use the same base_url")
        else:
            print(f"{Fore.YELLOW}⚠️  Multiple base_urls found:")
            for url in all_base_urls:
                print(f"{Fore.YELLOW}   - {url}")
        
        if len(all_endpoints) == 1:
            print(f"{Fore.GREEN}✅ All scenarios use the same endpoint")
        else:
            print(f"{Fore.YELLOW}⚠️  Multiple endpoints found:")
            for ep in all_endpoints:
                print(f"{Fore.YELLOW}   - {ep}")
        
        # Check for hardcoded default
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Checking for Hardcoded Defaults:")
        print("-" * 80)
        
        has_jsonplaceholder = any('jsonplaceholder.typicode.com' in s.get('base_url', '') for s in scenarios)
        has_example_com = any('api.example.com' in s.get('base_url', '') for s in scenarios)
        
        if has_jsonplaceholder:
            print(f"{Fore.RED}❌ Found hardcoded jsonplaceholder.typicode.com!")
        else:
            print(f"{Fore.GREEN}✅ No jsonplaceholder.typicode.com found")
        
        if has_example_com:
            print(f"{Fore.RED}❌ Found hardcoded api.example.com!")
        else:
            print(f"{Fore.GREEN}✅ No api.example.com found")
        
        # Final result
        print("\n" + "=" * 80)
        if base_url_correct and endpoint_correct and not has_jsonplaceholder and not has_example_com:
            print(f"{Fore.GREEN}{Style.BRIGHT}🎉 VERIFICATION PASSED! All checks successful!")
            print("=" * 80)
            return True
        else:
            print(f"{Fore.RED}{Style.BRIGHT}❌ VERIFICATION FAILED! Please check the issues above.")
            print("=" * 80)
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading CSV: {e}")
        return False


if __name__ == "__main__":
    # Configuration
    CSV_PATH = "Test_Data/generated-scenarios.csv"
    EXPECTED_BASE_URL = "http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction"
    EXPECTED_ENDPOINT = "/PDFViewer"
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Base URL Extraction Fix - CSV Verification")
    print(f"{Fore.CYAN}{'=' * 80}\n")
    
    # Run verification
    success = verify_csv(CSV_PATH, EXPECTED_BASE_URL, EXPECTED_ENDPOINT)
    
    # Exit with appropriate code
    exit(0 if success else 1)

