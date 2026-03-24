"""
Scenario Generator Module
Generate comprehensive test scenarios from parsed requirements
Phase 3: Supports both LLM-generated and rule-based scenarios
"""

import json
from typing import List, Dict, Any, Optional
from .test_data_generator import TestDataGenerator


class ScenarioGenerator:
    """
    Generate test scenarios from parsed requirements
    Phase 3: Supports LLM-generated scenarios
    """

    def __init__(self, llm_service=None):
        self.data_generator = TestDataGenerator()
        self.test_id_counter = 1
        self.llm_service = llm_service

    def generate(self, parsed_requirements: Dict[str, Any], use_llm: bool = False, requirements_text: str = "") -> List[Dict[str, Any]]:
        """
        Generate comprehensive test scenarios

        Phase 3: Try LLM generation first if enabled, fallback to rule-based

        Args:
            parsed_requirements: Dictionary from RequirementParser
            use_llm: Whether to use LLM for scenario generation (Phase 3)
            requirements_text: Original requirements text (needed for LLM)

        Returns:
            List of test scenario dictionaries
        """

        # Phase 3: Try LLM scenario generation if enabled
        if use_llm and self.llm_service and self.llm_service.is_available():
            try:
                llm_scenarios = self.llm_service.generate_scenarios(
                    requirements_text, parsed_requirements)
                if llm_scenarios:
                    print(f"\n🤖 LLM Generated {len(llm_scenarios)} scenarios")
                    return llm_scenarios
            except Exception as e:
                print(
                    f"⚠️  LLM scenario generation failed, using rule-based: {e}")

        # Fallback: Rule-based scenario generation (Phase 1)
        print(f"\n📋 Rule-based generation")
        return self._generate_rule_based(parsed_requirements)

    def _generate_rule_based(self, parsed_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate scenarios using rule-based templates (Phase 1)

        Args:
            parsed_requirements: Dictionary from RequirementParser

        Returns:
            List of test scenario dictionaries
        """

        scenarios = []
        entity = parsed_requirements['entity']
        operations = parsed_requirements['operations']
        fields = parsed_requirements['fields']
        validations = parsed_requirements['validations']

        # Reset counter
        self.test_id_counter = 1

        # Generate positive tests
        scenarios.extend(self._generate_positive_tests(
            entity, operations, fields, parsed_requirements
        ))

        # Generate validation tests
        if validations or fields:
            scenarios.extend(self._generate_validation_tests(
                entity, fields, validations, parsed_requirements
            ))

        # Generate edge case tests
        scenarios.extend(self._generate_edge_cases(
            entity, fields, parsed_requirements
        ))

        # Generate security tests
        scenarios.extend(self._generate_security_tests(
            entity, fields, parsed_requirements
        ))

        return scenarios

    def _get_next_test_id(self) -> str:
        """Generate next test ID"""
        test_id = f"TC-{self.test_id_counter:03d}"
        self.test_id_counter += 1
        return test_id

    def _get_endpoint(self, entity: str, endpoint_override: str = None) -> str:
        """Generate or return endpoint"""
        if endpoint_override:
            return endpoint_override

        # Pluralize entity for RESTful convention
        if entity.endswith('y'):
            plural = entity[:-1] + 'ies'
        elif entity.endswith('s'):
            plural = entity + 'es'
        else:
            plural = entity + 's'

        return f'/api/{plural}'

    def _generate_positive_tests(self, entity, operations, fields, req) -> List[Dict]:
        """Generate happy path scenarios"""
        scenarios = []
        endpoint = self._get_endpoint(entity, req.get('endpoint'))

        if 'create' in operations or req.get('method') == 'POST':
            # Generate valid test data
            test_data = self.data_generator.generate_valid_data(
                fields) if fields else {}

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with valid data',
                'test_category': 'Functional',
                'priority': 'P0',
                'method': 'POST',
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': str(req['status_codes']['success'][0]),
                'expected_response': '',
                'description': f'Happy path - valid {entity} creation',
                'preconditions': '',
                'test_data_set': 'valid_data',
                'automation_ready': 'Yes'
            })

        if 'read' in operations or req.get('method') == 'GET':
            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Get {entity} by ID',
                'test_category': 'Functional',
                'priority': 'P0',
                'method': 'GET',
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': f'{endpoint}/1',
                'headers': 'Content-Type: application/json',
                'body': '',
                'expected_status': '200',
                'expected_response': '',
                'description': f'Retrieve existing {entity}',
                'preconditions': f'{entity} with ID 1 exists',
                'test_data_set': 'existing_id',
                'automation_ready': 'Yes'
            })

        if 'update' in operations or req.get('method') in ['PUT', 'PATCH']:
            test_data = self.data_generator.generate_valid_data(
                fields) if fields else {}

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Update {entity} with valid data',
                'test_category': 'Functional',
                'priority': 'P0',
                'method': 'PUT',
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': f'{endpoint}/1',
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '200',
                'expected_response': '',
                'description': f'Update existing {entity}',
                'preconditions': f'{entity} with ID 1 exists',
                'test_data_set': 'valid_update_data',
                'automation_ready': 'Yes'
            })

        if 'delete' in operations or req.get('method') == 'DELETE':
            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Delete {entity}',
                'test_category': 'Functional',
                'priority': 'P1',
                'method': 'DELETE',
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': f'{endpoint}/1',
                'headers': 'Content-Type: application/json',
                'body': '',
                'expected_status': '200',
                'expected_response': '',
                'description': f'Delete existing {entity}',
                'preconditions': f'{entity} with ID 1 exists',
                'test_data_set': 'existing_id',
                'automation_ready': 'Yes'
            })

        return scenarios

    def _generate_validation_tests(self, entity, fields, validations, req) -> List[Dict]:
        """Generate validation error scenarios"""
        scenarios = []
        endpoint = self._get_endpoint(entity, req.get('endpoint'))
        method = req.get('method', 'POST')

        # Invalid email test
        email_validation = next(
            (v for v in validations if v.get('field') == 'email'), None)
        if email_validation or any(f['type'] == 'email' for f in fields):
            test_data = self.data_generator.generate_valid_data(
                fields) if fields else {}
            if 'email' in test_data:
                test_data['email'] = self.data_generator.generate_invalid_email()

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with invalid email format',
                'test_category': 'Validation',
                'priority': 'P0',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '400',
                'expected_response': 'error',
                'description': 'Validation - invalid email format',
                'preconditions': '',
                'test_data_set': 'invalid_email',
                'automation_ready': 'Yes'
            })

        # Short password test
        password_validation = next(
            (v for v in validations if v.get('field') == 'password'), None)
        if password_validation or any(f['type'] == 'password' for f in fields):
            test_data = self.data_generator.generate_valid_data(
                fields) if fields else {}
            if 'password' in test_data:
                test_data['password'] = 'short'

            min_length = password_validation.get(
                'value', 8) if password_validation else 8

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with short password',
                'test_category': 'Validation',
                'priority': 'P0',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '400',
                'expected_response': 'error',
                'description': f'Validation - password less than {min_length} characters',
                'preconditions': '',
                'test_data_set': 'short_password',
                'automation_ready': 'Yes'
            })

        # Missing required fields
        for field in fields[:3]:  # Limit to first 3 fields to avoid too many scenarios
            test_data = self.data_generator.generate_valid_data(
                fields) if fields else {}
            if field['name'] in test_data:
                del test_data[field['name']]

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with missing {field["name"]}',
                'test_category': 'Validation',
                'priority': 'P1',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '400',
                'expected_response': 'error',
                'description': f'Validation - missing required field: {field["name"]}',
                'preconditions': '',
                'test_data_set': f'missing_{field["name"]}',
                'automation_ready': 'Yes'
            })

        # Duplicate/unique constraint test
        unique_validation = next(
            (v for v in validations if v.get('rule') == 'unique'), None)
        if unique_validation:
            test_data = self.data_generator.generate_valid_data(
                fields) if fields else {}

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with duplicate data',
                'test_category': 'Business Logic',
                'priority': 'P0',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '400',
                'expected_response': 'error',
                'description': f'Business rule - duplicate {entity}',
                'preconditions': f'Same {entity} already exists',
                'test_data_set': 'duplicate_data',
                'automation_ready': 'Yes'
            })

        return scenarios

    def _generate_edge_cases(self, entity, fields, req) -> List[Dict]:
        """Generate edge case scenarios"""
        scenarios = []
        endpoint = self._get_endpoint(entity, req.get('endpoint'))
        method = req.get('method', 'POST')

        # Empty body
        scenarios.append({
            'test_id': self._get_next_test_id(),
            'test_name': f'Create {entity} with empty body',
            'test_category': 'Edge Case',
            'priority': 'P1',
            'method': method,
            'base_url': req.get('base_url') or 'http://api.example.com',
            'endpoint': endpoint,
            'headers': 'Content-Type: application/json',
            'body': '{}',
            'expected_status': '400',
            'expected_response': 'error',
            'description': 'Edge case - empty request body',
            'preconditions': '',
            'test_data_set': 'empty_body',
            'automation_ready': 'Yes'
        })

        # Null values
        if fields:
            test_data = {field['name']: None for field in fields}

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with null values',
                'test_category': 'Edge Case',
                'priority': 'P1',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data),
                'expected_status': '400',
                'expected_response': 'error',
                'description': 'Edge case - null values in all fields',
                'preconditions': '',
                'test_data_set': 'null_values',
                'automation_ready': 'Yes'
            })

        return scenarios

    def _generate_security_tests(self, entity, fields, req) -> List[Dict]:
        """Generate security test scenarios"""
        scenarios = []
        endpoint = self._get_endpoint(entity, req.get('endpoint'))
        method = req.get('method', 'POST')

        # SQL Injection
        if fields:
            test_data = self.data_generator.generate_valid_data(fields)
            if test_data:
                first_field = list(test_data.keys())[0]
                test_data[first_field] = self.data_generator.generate_sql_injection()

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with SQL injection attempt',
                'test_category': 'Security',
                'priority': 'P2',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '400',
                'expected_response': 'error',
                'description': 'Security - SQL injection attack',
                'preconditions': '',
                'test_data_set': 'sql_injection',
                'automation_ready': 'Yes'
            })

        # XSS Attack
        if fields:
            test_data = self.data_generator.generate_valid_data(fields)
            if test_data:
                first_field = list(test_data.keys())[0]
                test_data[first_field] = self.data_generator.generate_xss_attack()

            scenarios.append({
                'test_id': self._get_next_test_id(),
                'test_name': f'Create {entity} with XSS attempt',
                'test_category': 'Security',
                'priority': 'P2',
                'method': method,
                'base_url': req.get('base_url') or 'http://api.example.com',
                'endpoint': endpoint,
                'headers': 'Content-Type: application/json',
                'body': json.dumps(test_data) if test_data else '{}',
                'expected_status': '400',
                'expected_response': 'error',
                'description': 'Security - XSS attack',
                'preconditions': '',
                'test_data_set': 'xss_attack',
                'automation_ready': 'Yes'
            })

        return scenarios
