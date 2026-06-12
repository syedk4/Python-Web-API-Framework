"""
Test Executor Module
Handles API test execution, HTTP requests, and result tracking
"""

from core.schema_validator import SchemaValidator
import requests
import json
import time
import urllib3
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import SchemaValidator for advanced validation


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
    # Response validation fields
    response_validation_enabled: bool = False
    response_validation_passed: bool = True
    validation_errors: List[str] = field(default_factory=list)


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
        # Initialize schema validator for advanced validation
        self.schema_validator = SchemaValidator()

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

        # Add API key from global config if present and not explicitly overridden
        # Treat empty or whitespace-only API_KEY as "no key configured".
        api_key = (self.config.get('API_KEY') or '').strip()
        if api_key and 'API-KEY' not in headers:
            headers['API-KEY'] = api_key

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

        # Get expected response for validation (optional)
        expected_response = test_data.get('expected_response', '')

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

            # Capture response body for ALL tests (both pass and fail) for report visibility
            response_body = response.text[:2000] if response.text else ""

            # Step 1: Validate HTTP status code
            status_passed = (status_code == expected_status)

            # Step 2: Validate response content (if expected_response is provided)
            response_validation_enabled = False
            response_validation_passed = True
            validation_errors = []

            if expected_response:
                response_validation_enabled = True
                # Check if expected_response is a schema path or actual response
                response_validation_passed, validation_errors = self._validate_response(
                    response.text, expected_response, test_data
                )

            # Overall pass/fail: Both status AND response validation must pass
            passed = status_passed and response_validation_passed

            # Save PDF if applicable
            pdf_path = None
            if passed and response.headers.get('Content-Type', '').startswith('application/pdf'):
                pdf_path = self._save_pdf(response.content, test_name)

            # Capture error details for failed tests
            error_message = ""
            if not passed:
                if not status_passed:
                    error_message = f"HTTP {status_code}: {response.text[:500]}"
                elif not response_validation_passed:
                    error_message = f"Response validation failed: {'; '.join(validation_errors)}"

            # Build result message
            message_parts = [
                f"Status: {status_code} (Expected: {expected_status})"]
            if response_validation_enabled:
                validation_status = "✓ PASS" if response_validation_passed else "✗ FAIL"
                message_parts.append(
                    f"Response Validation: {validation_status}")
            message = " | ".join(message_parts)

            return TestResult(
                test_name=test_name,
                passed=passed,
                status_code=status_code,
                expected_status=expected_status,
                response_time=round(response_time, 2),
                response_size=response_size,
                message=message,
                test_data=test_data,
                response_body=response_body,
                error=error_message,
                response_validation_enabled=response_validation_enabled,
                response_validation_passed=response_validation_passed,
                validation_errors=validation_errors
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

        # Try to parse as JSON first (for headers like '{"Content-Type": "application/json"}')
        if isinstance(headers_string, str) and headers_string.strip().startswith('{'):
            try:
                parsed = json.loads(headers_string)
                if isinstance(parsed, dict):
                    headers.update(parsed)
                    return headers
            except json.JSONDecodeError:
                pass  # Fall through to regular parsing

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
        # Only treat None or empty string as "no body"
        # Empty dict {} and empty list [] are still valid JSON structures
        if body is None or body == "":
            return ""

        if isinstance(body, str):
            if body.startswith('{') or body.startswith('['):
                return body
            return body

        if isinstance(body, dict):
            # Serialize dict as-is (do not wrap in array)
            # This includes empty dict {} which becomes "{}"
            return json.dumps(body, indent=2)

        if isinstance(body, list):
            # This includes empty list [] which becomes "[]"
            return json.dumps(body, indent=2)

        return str(body)

    def _validate_response(
        self,
        actual_response_text: str,
        expected_response_str: str,
        test_data: Dict[str, Any] = None
    ) -> tuple[bool, List[str]]:
        """
        Validate actual response against expected response

        HYBRID VALIDATION APPROACH (FA-739 Enhancement):
        1. Schema-based validation (for dynamic/unpredictable data)
        2. Custom validators (for business rules like PO suffix)
        3. Exact match validation (for static/legacy tests - backward compatible)

        Priority order:
        - If schema path found in test_data -> use schema validation
        - Else use legacy exact match validation

        Universal multi-team validation strategy:
        - Supports multiple field naming conventions across different teams/APIs
        - Auto-detects common status and message field patterns
        - Partial match for message fields (flexible)
        - Backward compatible (optional validation)

        Returns:
            tuple: (validation_passed, list_of_validation_errors)
        """
        validation_errors = []

        # If no expected response provided, skip validation (backward compatible)
        if not expected_response_str or expected_response_str.strip() == "":
            return True, []

        # HYBRID APPROACH: Check if test_data has schema_path
        if test_data:
            schema_path = test_data.get('expected_response_schema', '').strip()

            # Option 1: Schema-based validation
            if schema_path:
                try:
                    # Parse actual response
                    actual_data = json.loads(actual_response_text)
                except json.JSONDecodeError:
                    return False, ["Actual response is not valid JSON"]

                # Validate using schema
                schema_valid, schema_errors = self.schema_validator.validate_from_file(
                    actual_data, schema_path
                )

                if not schema_valid:
                    return False, schema_errors

                # Check for custom validators
                custom_validator = test_data.get(
                    'custom_validator', '').strip()
                if custom_validator:
                    custom_valid, custom_errors = self._apply_custom_validator(
                        actual_data, custom_validator, test_data
                    )
                    if not custom_valid:
                        return False, custom_errors

                return True, []

        # Option 2: Legacy exact-match validation (backward compatible)

        try:
            # Parse expected response
            expected = json.loads(expected_response_str)
        except json.JSONDecodeError as e:
            validation_errors.append(
                f"Invalid expected_response JSON format: {str(e)}")
            return False, validation_errors

        try:
            # Parse actual response
            actual = json.loads(actual_response_text)
        except json.JSONDecodeError:
            validation_errors.append("Actual response is not valid JSON")
            return False, validation_errors

        # Common field names used across different APIs/teams
        # Ordered by priority (most common first)
        STATUS_FIELDS = [
            'OUTSTATUS',      # Ashley Furniture standard
            'status',         # Generic REST API
            'statusCode',     # Common alternative
            'code',           # Short form
            'result',         # Result-based APIs
            'state',          # State-based APIs
            'outcome',        # Outcome-based APIs
            'success'         # Boolean success indicator
        ]

        MESSAGE_FIELDS = [
            'OUTMESSAGE',     # Ashley Furniture standard
            'OREASON',        # Ashley Furniture RA/reason variant
            'message',        # Generic REST API
            'errorMessage',   # Error-specific
            'error',          # Simple error field
            'description',    # Descriptive field
            'detail',         # Detail field
            'reason',         # Reason field
            'msg',            # Abbreviated message
            'text',           # Generic text
            'info'            # Information field
        ]

        # 1. Validate STATUS field (smart detection)
        status_field_found = None
        for field_name in STATUS_FIELDS:
            if field_name in expected:
                status_field_found = field_name
                expected_status = expected.get(field_name)
                actual_status = actual.get(field_name)

                # Handle both string and boolean status values
                if actual_status != expected_status:
                    validation_errors.append(
                        f"{field_name} mismatch: expected '{expected_status}', got '{actual_status}'"
                    )
                break  # Only validate first matching status field

        # 2. Validate MESSAGE field (smart detection with partial match)
        message_field_found = None
        for field_name in MESSAGE_FIELDS:
            if field_name in expected:
                message_field_found = field_name
                expected_message = expected.get(field_name, '')
                actual_message = actual.get(field_name, '')

                # Convert to string for comparison (handles non-string types)
                expected_message_str = str(
                    expected_message) if expected_message else ''
                actual_message_str = str(
                    actual_message) if actual_message else ''

                # Partial match: actual should contain expected
                if expected_message_str and expected_message_str not in actual_message_str:
                    validation_errors.append(
                        f"{field_name} mismatch: expected containing '{expected_message_str}', got '{actual_message_str}'"
                    )
                break  # Only validate first matching message field

        # Validation passes if no errors
        validation_passed = len(validation_errors) == 0
        return validation_passed, validation_errors

    def _apply_custom_validator(
        self,
        response_data: Any,
        validator_type: str,
        test_data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """
        Apply custom business logic validators

        Supports FA-739 custom validators like:
        - po_suffix_sh: Validates poNumber ends with --SH
        - date_range: Validates dates fall within specified range
        - amount_calculation: Validates financial calculations

        Args:
            response_data: Parsed JSON response
            validator_type: Type of custom validator to apply
            test_data: Original test data (may contain validator params)

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        try:
            # Custom Validator: PO Suffix --SH
            if validator_type == 'po_suffix_sh':
                invoices = response_data.get('invoices', [])
                for idx, invoice in enumerate(invoices):
                    po_number = invoice.get('poNumber', '')
                    if not po_number.endswith('--SH'):
                        errors.append(
                            f"Invoice[{idx}] poNumber '{po_number}' does not end with --SH"
                        )

            # Custom Validator: Date Range
            elif validator_type == 'date_range':
                from datetime import datetime as dt

                # Extract fromDate and toDate from request body JSON
                from_date_str = ''
                to_date_str = ''

                # Try to parse from body field in test_data
                body_str = test_data.get('body', '')
                if body_str:
                    try:
                        body_json = json.loads(body_str)
                        from_date_str = body_json.get('fromDate', '')
                        to_date_str = body_json.get('toDate', '')
                    except (json.JSONDecodeError, AttributeError):
                        # If body parsing fails, try direct test_data fields
                        from_date_str = test_data.get('fromDate', '')
                        to_date_str = test_data.get('toDate', '')
                else:
                    # Fallback: check if dates are direct columns in CSV
                    from_date_str = test_data.get('fromDate', '')
                    to_date_str = test_data.get('toDate', '')

                if from_date_str and to_date_str:
                    from_date = dt.fromisoformat(from_date_str)
                    to_date = dt.fromisoformat(to_date_str)

                    invoices = response_data.get('invoices', [])
                    for idx, invoice in enumerate(invoices):
                        invoice_date_str = invoice.get('invoiceDate', '')
                        if invoice_date_str:
                            invoice_date = dt.fromisoformat(
                                invoice_date_str.split('T')[0])
                            if not (from_date <= invoice_date <= to_date):
                                errors.append(
                                    f"Invoice[{idx}] date '{invoice_date_str}' is outside range {from_date_str} to {to_date_str}"
                                )
                else:
                    errors.append(
                        "date_range validator: fromDate and toDate not found in request body or test data"
                    )

            # Custom Validator: Amount Calculation
            elif validator_type == 'amount_calculation':
                invoices = response_data.get('invoices', [])
                for idx, invoice in enumerate(invoices):
                    invoice_amount = float(invoice.get('invoiceAmount', 0))
                    paid_amount = float(invoice.get('paidAmount', 0))
                    open_amount = float(invoice.get('openAmount', 0))

                    expected_total = paid_amount + open_amount
                    # Allow small floating point differences
                    if abs(invoice_amount - expected_total) > 0.01:
                        errors.append(
                            f"Invoice[{idx}] amount mismatch: {invoice_amount} != {paid_amount} + {open_amount}"
                        )

            else:
                errors.append(f"Unknown custom validator: {validator_type}")

            return (len(errors) == 0, errors)

        except Exception as e:
            return False, [f"Custom validator error: {str(e)}"]

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
                'error': r.error,
                'response_body': r.response_body
            }
            for r in self.results
        ]
