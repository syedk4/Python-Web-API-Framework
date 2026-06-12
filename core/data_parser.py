"""
Data Parser Module
Handles parsing of CSV and JSON test data files with multi-encoding support
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class DataParser:
    """Parses test data from CSV and JSON files"""

    def __init__(self, test_data_dir: str = "Test_Data"):
        self.test_data_dir = test_data_dir
        self.supported_encodings = [
            'utf-8', 'utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']

    def get_test_files(self) -> List[Dict[str, Any]]:
        """Get list of available test data files with metadata"""
        files = []
        test_data_path = Path(self.test_data_dir)

        if not test_data_path.exists():
            return files

        for file_path in test_data_path.glob('*'):
            if file_path.suffix.lower() in ['.csv', '.json']:
                try:
                    file_info = {
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': file_path.stat().st_size,
                        'size_kb': round(file_path.stat().st_size / 1024, 1),
                        'type': file_path.suffix[1:].upper(),
                        'test_count': self._count_tests(file_path),
                        'descriptions': self._get_test_descriptions(file_path)
                    }
                    files.append(file_info)
                except Exception as e:
                    print(f"Error reading {file_path.name}: {e}")

        return sorted(files, key=lambda x: x['name'])

    def _count_tests(self, file_path: Path) -> int:
        """Count number of tests in file"""
        try:
            if file_path.suffix.lower() == '.csv':
                content = self._read_file_with_encoding(file_path)
                if content:
                    reader = csv.DictReader(content.splitlines())
                    return sum(1 for _ in reader)
            elif file_path.suffix.lower() == '.json':
                content = self._read_file_with_encoding(file_path)
                if content:
                    data = json.loads(content)
                    return len(data) if isinstance(data, list) else 1
        except:
            pass
        return 0

    def _get_test_descriptions(self, file_path: Path, max_count: int = 3) -> List[str]:
        """Get first few test descriptions"""
        descriptions = []
        try:
            if file_path.suffix.lower() == '.csv':
                content = self._read_file_with_encoding(file_path)
                if content:
                    reader = csv.DictReader(content.splitlines())
                    for i, row in enumerate(reader):
                        if i >= max_count:
                            break
                        desc = (row.get('testDescription') or
                                row.get('test_name') or
                                row.get('description') or
                                f"Test {i+1}")
                        descriptions.append(desc)
            elif file_path.suffix.lower() == '.json':
                content = self._read_file_with_encoding(file_path)
                if content:
                    data = json.loads(content)
                    if isinstance(data, list):
                        for i, item in enumerate(data[:max_count]):
                            desc = (item.get('testDescription') or
                                    item.get('test_name') or
                                    item.get('description') or
                                    f"Test {i+1}")
                            descriptions.append(desc)
        except:
            pass
        return descriptions

    def _read_file_with_encoding(self, file_path: Path) -> Optional[str]:
        """Read file with multiple encoding attempts"""
        for encoding in self.supported_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        return None

    def parse_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse CSV file and return test data"""
        test_data = []
        content = self._read_file_with_encoding(Path(file_path))

        if not content:
            raise ValueError(
                f"Could not read file with any supported encoding")

        reader = csv.DictReader(content.splitlines())

        for row in reader:
            # Check if this is legacy or dynamic format
            if 'method' in row and 'base_url' in row:
                # Dynamic format
                test_data.append(self._parse_dynamic_row(row))
            else:
                # Legacy format
                test_data.append(self._parse_legacy_row(row))

        return test_data

    def _parse_dynamic_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Parse dynamic format CSV row"""
        return {
            'test_id': row.get('test_id', ''),
            'test_name': row.get('test_name', ''),
            'method': row.get('method', 'POST'),
            'base_url': row.get('base_url', ''),
            'endpoint': row.get('endpoint', ''),
            'body': self._parse_body(row.get('body', '')),
            'headers': row.get('headers', ''),
            'expected_status': row.get('expected_status', '200'),
            'expected_response': row.get('expected_response', ''),
            'expected_response_schema': row.get('expected_response_schema', ''),
            'custom_validator': row.get('custom_validator', ''),
            'description': row.get('description', ''),
            'api_key': row.get('api_key', '')
        }

    def _parse_legacy_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Parse legacy format CSV row"""
        shipto = row.get('shipTo', '')
        if shipto and shipto.isdigit() and len(shipto) == 1:
            shipto = shipto.zfill(2)

        return {
            'test_name': row.get('testDescription', 'Legacy Test'),
            'method': 'POST',
            'base_url': '',
            'endpoint': '',
            'body': {
                'environment': 'AFI',
                'customerNumber': row.get('customerNumber', ''),
                'shipTo': shipto,
                'invoiceNumber': row.get('invoiceNumber', ''),
                'orderNumber': row.get('orderNumber', ''),
                'languageCheck': 'EN-US'
            },
            'headers': 'Content-Type:application/json',
            'expected_status': '200',
            'description': row.get('testDescription', ''),
            'api_key': ''
        }

    def _parse_body(self, body_str: str) -> Any:
        """Parse body string to appropriate format"""
        if not body_str:
            return ''

        body_str = body_str.strip()

        if body_str.startswith('{') or body_str.startswith('['):
            try:
                return json.loads(body_str)
            except json.JSONDecodeError:
                return body_str

        return body_str

    def parse_json(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse JSON file and return test data"""
        content = self._read_file_with_encoding(Path(file_path))

        if not content:
            raise ValueError(
                f"Could not read file with any supported encoding")

        data = json.loads(content)

        if not isinstance(data, list):
            data = [data]

        test_data = []
        for item in data:
            if 'method' in item and 'base_url' in item:
                test_data.append(item)
            else:
                test_data.append(self._parse_legacy_json(item))

        return test_data

    def _parse_legacy_json(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse legacy format JSON item"""
        shipto = item.get('shipTo', '')
        if shipto and str(shipto).isdigit() and len(str(shipto)) == 1:
            shipto = str(shipto).zfill(2)

        return {
            'test_name': item.get('testDescription', 'Legacy Test'),
            'method': 'POST',
            'base_url': '',
            'endpoint': '',
            'body': {
                'environment': 'AFI',
                'customerNumber': item.get('customerNumber', ''),
                'shipTo': shipto,
                'invoiceNumber': item.get('invoiceNumber', ''),
                'orderNumber': item.get('orderNumber', ''),
                'languageCheck': 'EN-US'
            },
            'headers': 'Content-Type:application/json',
            'expected_status': '200',
            'description': item.get('testDescription', ''),
            'api_key': ''
        }

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse file based on extension"""
        path = Path(file_path)

        if path.suffix.lower() == '.csv':
            return self.parse_csv(file_path)
        elif path.suffix.lower() == '.json':
            return self.parse_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
