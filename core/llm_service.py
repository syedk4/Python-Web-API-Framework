"""
LLM Service - Phase 2 AI-Powered Scenario Generation
Provides intelligent requirement parsing and scenario generation using LLMs
"""

import os
import json
from typing import Dict, Any, List, Optional
import logging

# LLM imports (will be optional)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class LLMService:
    """Service for LLM-powered requirement parsing and scenario generation"""

    def __init__(self, config: Dict[str, str] = None):
        """
        Initialize LLM Service

        Args:
            config: Configuration dictionary with LLM settings
        """
        self.config = config or {}
        self.enabled = self._parse_bool(
            self.config.get('LLM_ENABLED', 'false'))
        self.provider = self.config.get('LLM_PROVIDER', 'openai').lower()
        self.temperature = float(self.config.get('LLM_TEMPERATURE', '0.3'))
        self.max_tokens = int(self.config.get('OPENAI_MAX_TOKENS', '2000'))

        # Cost tracking
        self.total_cost = 0.0
        self.max_cost_per_request = float(
            self.config.get('LLM_MAX_COST_PER_REQUEST', '0.10'))

        # Initialize clients
        self.openai_client = None
        self.anthropic_client = None

        if self.enabled:
            self._initialize_clients()

    def _parse_bool(self, value: str) -> bool:
        """Parse boolean from string"""
        return value.lower() in ('true', '1', 'yes', 'on')

    def _initialize_clients(self):
        """Initialize LLM API clients"""
        if self.provider == 'openai' and OPENAI_AVAILABLE:
            api_key = self.config.get('OPENAI_API_KEY', '')
            azure_endpoint = self.config.get('AZURE_OPENAI_ENDPOINT', '')

            if api_key and api_key != 'your-openai-api-key-here':
                # Check if this is Azure OpenAI (longer key format or has azure endpoint)
                if azure_endpoint or len(api_key) > 60:
                    # Azure OpenAI
                    if not azure_endpoint:
                        logging.error(
                            "Azure OpenAI detected but AZURE_OPENAI_ENDPOINT not configured")
                        return

                    self.openai_client = openai.AzureOpenAI(
                        api_key=api_key,
                        api_version=self.config.get(
                            'AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                        azure_endpoint=azure_endpoint
                    )
                    logging.info("Azure OpenAI client initialized")
                else:
                    # Standard OpenAI
                    self.openai_client = openai.OpenAI(api_key=api_key)
                    logging.info("OpenAI client initialized")

        elif self.provider == 'anthropic' and ANTHROPIC_AVAILABLE:
            api_key = self.config.get('ANTHROPIC_API_KEY', '')
            if api_key and api_key != 'your-anthropic-api-key-here':
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                logging.info("Anthropic client initialized")

    def is_available(self) -> bool:
        """Check if LLM service is available and configured"""
        if not self.enabled:
            return False

        if self.provider == 'openai':
            return self.openai_client is not None
        elif self.provider == 'anthropic':
            return self.anthropic_client is not None

        return False

    def parse_requirements(self, requirements_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse requirements using LLM

        Args:
            requirements_text: Natural language requirements

        Returns:
            Parsed requirement dictionary or None if LLM unavailable
        """
        if not self.is_available():
            return None

        prompt = self._build_parsing_prompt(requirements_text)

        try:
            if self.provider == 'openai':
                response = self._call_openai(prompt)
            elif self.provider == 'anthropic':
                response = self._call_anthropic(prompt)
            else:
                return None

            # Parse JSON response
            parsed = json.loads(response)
            return parsed

        except Exception as e:
            logging.error(f"LLM parsing error: {e}")
            return None

    def generate_scenarios(self, requirements: str, parsed_data: Dict[str, Any]) -> Optional[List[Dict]]:
        """
        Generate test scenarios using LLM (Phase 3)

        Args:
            requirements: Original requirements text
            parsed_data: Parsed requirement data (entity, fields, etc.)

        Returns:
            List of generated test scenarios or None if LLM unavailable
        """
        if not self.is_available():
            return None

        prompt = self._build_scenario_generation_prompt(
            requirements, parsed_data)

        try:
            if self.provider == 'openai':
                response = self._call_openai(prompt)
            elif self.provider == 'anthropic':
                response = self._call_anthropic(prompt)
            else:
                return None

            # Parse JSON response with better error handling
            try:
                result = json.loads(response)
            except json.JSONDecodeError as je:
                # Try to extract JSON from markdown code blocks
                import re
                json_match = re.search(
                    r'```(?:json)?\s*(\{.*\})\s*```', response, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        # Try to find just the scenarios array
                        json_match = re.search(
                            r'\{.*"scenarios".*\}', response, re.DOTALL)
                        if json_match:
                            try:
                                result = json.loads(json_match.group(0))
                            except json.JSONDecodeError:
                                logging.error(
                                    f"Failed to parse JSON from LLM response: {je}")
                                logging.debug(
                                    f"Response was: {response[:1000]}")
                                return None
                        else:
                            logging.error(
                                f"Failed to parse JSON from LLM response: {je}")
                            logging.debug(f"Response was: {response[:1000]}")
                            return None
                else:
                    # Try to find JSON object in the response
                    json_match = re.search(
                        r'\{.*"scenarios".*\}', response, re.DOTALL)
                    if json_match:
                        try:
                            result = json.loads(json_match.group(0))
                        except json.JSONDecodeError:
                            logging.error(
                                f"Failed to parse JSON from LLM response: {je}")
                            logging.debug(f"Response was: {response[:1000]}")
                            return None
                    else:
                        logging.error(
                            f"Failed to parse JSON from LLM response: {je}")
                        logging.debug(f"Response was: {response[:1000]}")
                        return None

            scenarios = result.get('scenarios', [])

            # Validate and format scenarios
            # Pass base_url from parsed_data to ensure it's used in scenarios
            return self._format_scenarios(scenarios, parsed_data.get('base_url', ''))

        except Exception as e:
            logging.error(f"LLM scenario generation error: {e}")
            return None

    def enhance_scenarios(self, scenarios: List[Dict], requirements: str) -> List[Dict]:
        """
        Enhance generated scenarios with LLM suggestions

        Args:
            scenarios: List of generated scenarios
            requirements: Original requirements text

        Returns:
            Enhanced scenarios list
        """
        if not self.is_available():
            return scenarios

        # For now, return original scenarios
        # Future: Add LLM-based scenario enhancement
        return scenarios

    def _build_parsing_prompt(self, requirements: str) -> str:
        """Build prompt for requirement parsing"""
        return f"""Parse the following API testing requirements and extract structured information.
Return ONLY valid JSON with no additional text.

Requirements:
{requirements}

Extract and return JSON with this structure:
{{
    "entity": "main entity being tested (e.g., user, product)",
    "operations": ["list of CRUD operations: create, read, update, delete"],
    "fields": [
        {{"name": "field_name", "type": "field_type", "required": true/false}}
    ],
    "validations": [
        {{"field": "field_name", "rule": "validation_rule", "value": "constraint_value"}}
    ],
    "endpoint": "/api/endpoint/path",
    "method": "HTTP_METHOD",
    "base_url": "",
    "status_codes": {{
        "success": [200, 201],
        "error": [400, 404, 500]
    }},
    "business_rules": ["list of business rules"]
}}

IMPORTANT URL EXTRACTION RULES:
1. If requirements explicitly label "API URL:" and "Endpoint:" separately:
   - Extract the labeled "API URL" as base_url
   - Extract the labeled "Endpoint" as endpoint

2. If a full URL is provided without labels, use intelligent splitting:
   - Look for common API path patterns (/api/, /v1/, /WebAPI/, etc.)
   - Split at the last major API boundary
   - Example: "https://api.example.com/api/users" → base_url: "https://api.example.com", endpoint: "/api/users"

3. Special case - if the URL contains a service path before the endpoint:
   - Example: "http://server.com/WebAPI/InvoiceExtraction/PDFViewer"
   - Split as: base_url: "http://server.com/WebAPI/InvoiceExtraction", endpoint: "/PDFViewer"
   - The base_url includes the service path, endpoint is the final resource

4. If only base_url is mentioned, fill "base_url" and leave "endpoint" as ""
5. If only endpoint is mentioned, fill "endpoint" and leave "base_url" as ""
6. If neither is mentioned, leave both as empty strings ""
7. Do NOT make up or assume base_url or endpoint values
8. Do NOT use placeholder URLs like "jsonplaceholder.typicode.com" unless explicitly in the requirements

Examples:
- "API URL: http://server.com/WebAPI/InvoiceExtraction/PDFViewer" →
  base_url: "http://server.com/WebAPI/InvoiceExtraction", endpoint: "/PDFViewer"
- "https://payroll-api.azurewebsites.net/WebAPI/InvoiceExtraction/PDFViewer" →
  base_url: "https://payroll-api.azurewebsites.net/WebAPI/InvoiceExtraction", endpoint: "/PDFViewer"
- "POST to https://api.myapp.com/v1/users" →
  base_url: "https://api.myapp.com", endpoint: "/v1/users"
- "endpoint /api/users" →
  base_url: "", endpoint: "/api/users"

Return ONLY the JSON object, no markdown, no explanations."""

    def _build_scenario_generation_prompt(self, requirements: str, parsed_data: Dict) -> str:
        """Build prompt for scenario generation (Phase 3)"""
        entity = parsed_data.get('entity', 'resource')
        operations = parsed_data.get('operations', [])
        fields = parsed_data.get('fields', [])
        validations = parsed_data.get('validations', [])
        base_url = parsed_data.get('base_url', '')
        endpoint = parsed_data.get('endpoint', '/api/endpoint')
        method = parsed_data.get('method', 'POST')

        return f"""Generate comprehensive API test scenarios based on the following requirements.

Requirements:
{requirements}

Parsed Information:
- Entity: {entity}
- Operations: {', '.join(operations)}
- Base URL: {base_url if base_url else '(not specified)'}
- Endpoint: {endpoint}
- HTTP Method: {method}
- Fields: {json.dumps(fields, indent=2)}
- Validations: {json.dumps(validations, indent=2)}

Generate a comprehensive set of test scenarios covering:
1. **Positive Tests**: Valid data scenarios that should succeed
2. **Validation Tests**: Invalid data for each field (format, length, required fields)
3. **Business Logic Tests**: Duplicate data, state transitions, business rules
4. **Edge Cases**: Empty body, null values, boundary conditions
5. **Security Tests**: SQL injection, XSS, authentication bypass attempts

Return ONLY valid JSON with no additional text in this exact structure:
{{
    "scenarios": [
        {{
            "test_id": "TC-001",
            "test_name": "Descriptive test name",
            "category": "Functional|Validation|Business Logic|Edge Case|Security",
            "priority": "P0|P1|P2",
            "method": "{method}",
            "endpoint": "{endpoint}",
            "expected_status": 200,
            "description": "What this test validates",
            "test_data": {{
                "field1": "value1",
                "field2": "value2"
            }},
            "assertions": [
                "Response status should be 200",
                "Response should contain user ID"
            ]
        }}
    ]
}}

Generate at least 10-15 comprehensive test scenarios. Be creative and thorough.
Return ONLY the JSON object, no markdown, no explanations."""

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        model = self.config.get('OPENAI_MODEL', 'gpt-4-turbo-preview')

        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert API testing assistant. Extract structured information from requirements and return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"}
        )

        # Track cost (approximate)
        self._track_cost(response.usage.total_tokens, model)

        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        model = self.config.get('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')

        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system="You are an expert API testing assistant. Extract structured information from requirements and return valid JSON only.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Track cost (approximate)
        self._track_cost(response.usage.input_tokens +
                         response.usage.output_tokens, model)

        return response.content[0].text

    def _track_cost(self, tokens: int, model: str):
        """Track API usage cost"""
        # Approximate pricing (as of 2024)
        pricing = {
            'gpt-4-turbo-preview': 0.01 / 1000,  # $0.01 per 1K tokens
            'gpt-3.5-turbo': 0.0015 / 1000,
            'claude-3-sonnet-20240229': 0.003 / 1000,
            'claude-3-opus-20240229': 0.015 / 1000,
        }

        cost_per_token = pricing.get(model, 0.01 / 1000)
        request_cost = tokens * cost_per_token
        self.total_cost += request_cost

        logging.info(
            f"LLM Request: {tokens} tokens, ${request_cost:.4f} (Total: ${self.total_cost:.4f})")

    def _format_scenarios(self, scenarios: List[Dict], parsed_base_url: str = '') -> List[Dict]:
        """
        Format and validate LLM-generated scenarios to match TestExecutor format

        Args:
            scenarios: Raw scenarios from LLM
            parsed_base_url: Base URL extracted from requirements during parsing

        Returns:
            Formatted and validated scenarios compatible with TestExecutor
        """
        formatted = []

        for idx, scenario in enumerate(scenarios):
            # Convert test_data object to JSON string for body
            test_data = scenario.get('test_data', {})
            body = json.dumps(test_data) if test_data else '{}'

            # Get base_url with priority:
            # 1. From scenario (if LLM included it)
            # 2. From parsed requirements (extracted during parsing phase)
            # 3. Default to JSONPlaceholder (only if nothing else available)
            base_url = scenario.get(
                'base_url') or parsed_base_url or 'https://jsonplaceholder.typicode.com'

            # Format scenario to match TestExecutor expected structure
            formatted_scenario = {
                'test_id': scenario.get('test_id', f'TC-{idx+1:03d}'),
                'test_name': scenario.get('test_name', f'Test {idx+1}'),
                # Map 'category' to 'test_category'
                'test_category': scenario.get('category', 'Functional'),
                'priority': scenario.get('priority', 'P1'),
                'method': scenario.get('method', 'POST'),
                'base_url': base_url,
                'endpoint': scenario.get('endpoint', '/api/endpoint'),
                'headers': 'Content-Type: application/json',  # Default headers
                'body': body,  # Convert test_data to JSON string
                # Convert to string
                'expected_status': str(scenario.get('expected_status', 200)),
                'expected_response': '',  # TestExecutor expects this field
                'description': scenario.get('description', ''),
                'preconditions': '',  # TestExecutor expects this field
                'test_data_set': scenario.get('test_id', f'llm_generated_{idx+1}'),
                'automation_ready': 'Yes',
                # Keep LLM-specific fields for display
                'test_data': test_data,
                'assertions': scenario.get('assertions', [])
            }
            formatted.append(formatted_scenario)

        return formatted

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get LLM usage statistics"""
        return {
            'enabled': self.enabled,
            'provider': self.provider,
            'available': self.is_available(),
            'total_cost': round(self.total_cost, 4),
            'max_cost_per_request': self.max_cost_per_request
        }
