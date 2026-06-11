"""
Report Generator Module
Generates HTML reports from test execution results
"""

from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class ReportGenerator:
    """Generates test reports in various formats"""

    def __init__(self, output_dir: str = "test-results"):
        self.output_dir = Path(output_dir)

    def generate_html_report(self, results: List[Dict[str, Any]],
                             summary: Dict[str, Any]) -> str:
        """Generate HTML report from test results"""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pass_rate = summary.get('pass_rate', 0)

        # Generate results rows
        results_html = ""
        for i, result in enumerate(results, 1):
            status_class = "status-pass" if result['passed'] else "status-fail"
            status_text = "PASS" if result['passed'] else "FAIL"
            error_msg = result.get('error', '')
            response_body = result.get('response_body', '')

            # Response validation fields
            response_validation_enabled = result.get(
                'response_validation_enabled', False)
            response_validation_passed = result.get(
                'response_validation_passed', True)
            validation_errors = result.get('validation_errors', [])

            # Escape HTML in response/error for safe display
            import html
            error_escaped = html.escape(error_msg) if error_msg else ''
            response_escaped = html.escape(
                response_body) if response_body else ''

            # Show truncated error with tooltip, full error in expandable section
            if error_msg:
                error_preview = error_msg[:80] + \
                    '...' if len(error_msg) > 80 else error_msg
                error_display = f'<span class="error-preview" title="{error_escaped}">{html.escape(error_preview)}</span>'
            else:
                error_display = '<span class="no-error">-</span>'

            # Response validation indicator
            if response_validation_enabled:
                validation_class = "validation-pass" if response_validation_passed else "validation-fail"
                validation_icon = "✓" if response_validation_passed else "✗"
                validation_display = f'<span class="{validation_class}" title="Response validation: {validation_icon}">{validation_icon}</span>'
            else:
                validation_display = '<span class="validation-na" title="No validation">-</span>'

            results_html += f"""
            <tr class="result-row" onclick="toggleDetails({i})">
                <td>{i}</td>
                <td>{result['test_name']}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{result['status_code']}</td>
                <td>{result['expected_status']}</td>
                <td class="validation-cell">{validation_display}</td>
                <td>{result['response_time']}s</td>
                <td>{self._format_size(result['response_size'])}</td>
                <td>{result['timestamp']}</td>
                <td class="error-cell">{error_display}</td>
            </tr>
            <tr id="details-{i}" class="details-row" style="display: none;">
                <td colspan="10">
                    <div class="details-content">
                        <div class="detail-section">
                            <h4>Response Body:</h4>
                            <pre class="response-body">{response_escaped if response_escaped else '(empty)'}</pre>
                        </div>
                        {f'''<div class="detail-section validation-section">
                            <h4>Response Validation {'✓ PASSED' if response_validation_passed else '✗ FAILED'}:</h4>
                            <ul class="validation-errors">
                                {''.join(f'<li>{html.escape(error)}</li>' for error in validation_errors) if validation_errors else '<li class="validation-success">All validation checks passed</li>'}
                            </ul>
                        </div>''' if response_validation_enabled else ''}
                        {f'''<div class="detail-section error-section">
                            <h4>Error Details:</h4>
                            <pre class="error-details">{error_escaped}</pre>
                        </div>''' if error_msg else ''}
                    </div>
                </td>
            </tr>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Test Report - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #333; }}
        .summary-card .value {{ font-size: 2em; font-weight: bold; }}
        .passed {{ color: #28a745; border-left-color: #28a745; }}
        .failed {{ color: #dc3545; border-left-color: #dc3545; }}
        .total {{ color: #007bff; border-left-color: #007bff; }}
        .pass-rate {{ color: #17a2b8; border-left-color: #17a2b8; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #007bff; color: white; position: sticky; top: 0; z-index: 10; }}
        .result-row {{ cursor: pointer; transition: background-color 0.2s; }}
        .result-row:hover {{ background: #e3f2fd !important; }}
        .result-row:nth-child(4n+1) {{ background: #f8f9fa; }}
        .status-pass {{ color: #28a745; font-weight: bold; }}
        .status-fail {{ color: #dc3545; font-weight: bold; }}
        .error-cell {{ font-size: 0.9em; color: #666; max-width: 300px; }}
        .error-preview {{ color: #d32f2f; font-weight: 500; cursor: help; }}
        .no-error {{ color: #999; }}
        .details-row {{ background: #f0f7ff !important; }}
        .details-content {{ padding: 20px; }}
        .detail-section {{ margin-bottom: 20px; }}
        .detail-section h4 {{ margin: 0 0 10px 0; color: #333; font-size: 14px; text-transform: uppercase; border-bottom: 2px solid #007bff; padding-bottom: 5px; }}
        .detail-section pre {{ background: #263238; color: #aed581; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 13px; line-height: 1.5; margin: 0; white-space: pre-wrap; word-wrap: break-word; }}
        .error-section h4 {{ border-bottom-color: #dc3545; }}
        .error-section pre {{ background: #ffebee; color: #c62828; border-left: 4px solid #dc3545; }}
        .validation-section h4 {{ border-bottom-color: #007bff; }}
        .validation-section ul {{ margin: 0; padding-left: 20px; }}
        .validation-section li {{ padding: 5px 0; }}
        .validation-errors li {{ color: #c62828; }}
        .validation-success {{ color: #28a745; font-style: italic; }}
        .validation-cell {{ text-align: center; font-size: 1.2em; }}
        .validation-pass {{ color: #28a745; font-weight: bold; }}
        .validation-fail {{ color: #dc3545; font-weight: bold; }}
        .validation-na {{ color: #999; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
        .expand-hint {{ font-size: 0.85em; color: #999; font-style: italic; margin-top: 10px; text-align: center; }}
    </style>
    <script>
        function toggleDetails(rowNum) {{
            const detailsRow = document.getElementById('details-' + rowNum);
            if (detailsRow.style.display === 'none') {{
                detailsRow.style.display = 'table-row';
            }} else {{
                detailsRow.style.display = 'none';
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>API Test Report</h1>
            <p>Generated: {timestamp}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>Total Tests</h3>
                <div class="value">{summary['total']}</div>
            </div>
            <div class="summary-card passed">
                <h3>Passed</h3>
                <div class="value">{summary['passed']}</div>
            </div>
            <div class="summary-card failed">
                <h3>Failed</h3>
                <div class="value">{summary['failed']}</div>
            </div>
            <div class="summary-card pass-rate">
                <h3>Pass Rate</h3>
                <div class="value">{pass_rate}%</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <p class="expand-hint">💡 Click any row to view full response body, validation details, and errors</p>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Actual</th>
                    <th>Expected</th>
                    <th>Validation</th>
                    <th>Time</th>
                    <th>Size</th>
                    <th>Timestamp</th>
                    <th>Error Details</th>
                </tr>
            </thead>
            <tbody>
                {results_html}
            </tbody>
        </table>
        
        <div class="footer">
            <p>HTTPie-Python-Web Test Framework</p>
            <p>Total Tests: {summary['total']} | Passed: {summary['passed']} | Failed: {summary['failed']} | Pass Rate: {pass_rate}%</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def _format_size(self, size_bytes: int) -> str:
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def save_report(self, html_content: str, filename: str = None) -> str:
        """Save HTML report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Test_Report_{timestamp}.html"

        # Create output directory
        date_folder = datetime.now().strftime("%Y-%m-%d")
        output_dir = self.output_dir / date_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        filepath = output_dir / filename
        filepath.write_text(html_content, encoding='utf-8')

        return str(filepath)
