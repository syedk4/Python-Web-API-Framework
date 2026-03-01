"""
Test Executor Module
Handles API test execution, HTTP requests, and result tracking
"""

import requests
import json
import time
import urllib3
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class TestResult:
    """Data class for storing test results"""
    test_name: str
    passed: bool
    status_code: int
    expected_status: int
    response_time: float
    response_size: int
    message: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    test_data: Dict[str, Any] = field(default_factory=dict)
    response_body: str = ""
    error: str = ""


class TestExecutor:
    """Executes API tests and tracks results"""

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.current_test = 0
        self.is_running = False
        self.should_stop = False

    def execute_tests(self, test_data_list: List[Dict[str, Any]],
                      progress_callback=None) -> List[TestResult]:
        """Execute a list of tests"""
        self.results = []
        self.total_tests = len(test_data_list)
        self.current_test = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.is_running = True
        self.should_stop = False

        for i, test_data in enumerate(test_data_list, 1):
            if self.should_stop:
                break

            self.current_test = i
            result = self.execute_single_test(test_data, i)
            self.results.append(result)

            if result.passed:
                self.passed_tests += 1
            else:
                self.failed_tests += 1

            if progress_callback:
                progress_callback({
                    'current': i,
                    'total': self.total_tests,
                    'passed': self.passed_tests,
                    'failed': self.failed_tests,
                    'test_name': result.test_name,
                    'status': 'passed' if result.passed else 'failed'
                })

        self.is_running = False
        return self.results

    def execute_single_test(self, test_data: Dict[str, Any], test_number: int) -> TestResult:
        """Execute a single test"""
        test_name = test_data.get('test_name') or test_data.get(
            'description') or f"Test #{test_number}"

        # Build URL
        base_url = test_data.get(
            'base_url') or self.config.get('API_BASE_URL', '')
        endpoint = test_data.get(
            'endpoint') or self.config.get('API_ENDPOINT', '')
        url = f"{base_url}{endpoint}"

        # Build headers
        headers = self._parse_headers(test_data.get('headers', ''))

        # Add API key if not present
        if self.config.get('API_KEY') and 'API-KEY' not in headers:
            headers['API-KEY'] = self.config['API_KEY']

        # Add correlation ID
        if self.config.get('CORRELATION_ID') and 'Correlation-ID' not in headers:
            headers['Correlation-ID'] = self.config['CORRELATION_ID']

        # Prepare body
        body = test_data.get('body', '')
        request_body = self._prepare_body(body)

        # Get method and expected status
        # Use configured METHOD as default if test data doesn't specify one
        default_method = self.config.get('METHOD', 'POST')
        method = test_data.get('method', default_method).upper()
        expected_status = int(test_data.get('expected_status', 200))
        timeout = int(self.config.get('TIMEOUT', 30))

        # Execute request
        start_time = time.time()

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                data=request_body if method in [
                    'POST', 'PUT', 'PATCH'] else None,
                timeout=timeout,
                verify=False
            )

            response_time = time.time() - start_time
            status_code = response.status_code
            response_size = len(response.content)
            passed = (status_code == expected_status)

            # Save PDF if applicable
            pdf_path = None
            if passed and response.headers.get('Content-Type', '').startswith('application/pdf'):
                pdf_path = self._save_pdf(response.content, test_name)

            # Capture error details for failed tests
            error_message = ""
            response_preview = ""
            if not passed:
                # Increased from 500 to 1000
                response_preview = response.text[:1000]
                error_message = f"HTTP {status_code}: {response.text[:200]}"

            return TestResult(
                test_name=test_name,
                passed=passed,
                status_code=status_code,
                expected_status=expected_status,
                response_time=round(response_time, 2),
                response_size=response_size,
                message=f"Status: {status_code} (Expected: {expected_status})",
                test_data=test_data,
                response_body=response_preview,
                error=error_message
            )

        except requests.exceptions.Timeout:
            return TestResult(
                test_name=test_name,
                passed=False,
                status_code=0,
                expected_status=expected_status,
                response_time=timeout,
                response_size=0,
                message="Request timeout",
                test_data=test_data,
                error="Request timed out"
            )
        except Exception as e:
            return TestResult(
                test_name=test_name,
                passed=False,
                status_code=0,
                expected_status=expected_status,
                response_time=0,
                response_size=0,
                message=f"Error: {str(e)}",
                test_data=test_data,
                error=str(e)
            )

    def _parse_headers(self, headers_string: str) -> Dict[str, str]:
        """Parse headers from string format"""
        headers = {'Content-Type': 'application/json'}

        if not headers_string or headers_string == "None":
            return headers

        if isinstance(headers_string, dict):
            return headers_string

        # Support both semicolon and comma separators
        separator = ';' if ';' in headers_string else ','

        for header_pair in headers_string.split(separator):
            header_pair = header_pair.strip()
            if ':' in header_pair:
                key, value = header_pair.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Normalize header names (underscore to hyphen)
                if '_' in key:
                    key = key.replace('_', '-')

                headers[key] = value

        return headers

    def _prepare_body(self, body: Any) -> str:
        """Prepare request body"""
        if not body:
            return ""

        if isinstance(body, str):
            if body.startswith('{') or body.startswith('['):
                return body
            return body

        if isinstance(body, dict):
            # Wrap single object in array for API compatibility
            return json.dumps([body], indent=2)

        if isinstance(body, list):
            return json.dumps(body, indent=2)

        return str(body)

    def _save_pdf(self, content: bytes, test_name: str) -> str:
        """Save PDF file"""
        from pathlib import Path

        # Create output directory
        date_folder = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H-%M-%S")
        output_dir = Path("test-results") / date_folder / f"run_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean filename
        safe_name = "".join(c for c in test_name if c.isalnum()
                            or c in (' ', '-', '_')).strip()
        safe_name = safe_name[:100]  # Limit length

        filename = output_dir / \
            f"{safe_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"

        with open(filename, 'wb') as f:
            f.write(content)

        return str(filename)

    def stop(self):
        """Stop test execution"""
        self.should_stop = True

    def get_summary(self) -> Dict[str, Any]:
        """Get test execution summary"""
        return {
            'total': self.total_tests,
            'passed': self.passed_tests,
            'failed': self.failed_tests,
            'pass_rate': round((self.passed_tests / self.total_tests * 100), 2) if self.total_tests > 0 else 0,
            'is_running': self.is_running,
            'current_test': self.current_test
        }

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all test results as dictionaries"""
        return [
            {
                'test_name': r.test_name,
                'passed': r.passed,
                'status_code': r.status_code,
                'expected_status': r.expected_status,
                'response_time': r.response_time,
                'response_size': r.response_size,
                'message': r.message,
                'timestamp': r.timestamp,
                'error': r.error
            }
            for r in self.results
        ]
