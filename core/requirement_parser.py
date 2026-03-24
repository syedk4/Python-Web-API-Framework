"""
Requirement Parser Module
Parses natural language requirements and extracts structured information
Phase 1: Rule-based parsing (regex, NLP patterns, keyword matching)
Phase 2: LLM-enhanced parsing with fallback to rule-based
"""

import re
from typing import Dict, List, Any, Optional


class RequirementParser:
    """
    Intelligent parser that extracts structured data from natural language requirements
    Supports both rule-based (Phase 1) and LLM-enhanced (Phase 2) parsing
    """

    # Keyword dictionaries for pattern matching
    OPERATIONS = {
        'create': ['create', 'add', 'register', 'sign up', 'signup', 'new', 'insert', 'post'],
        'read': ['get', 'retrieve', 'fetch', 'view', 'show', 'list', 'search', 'find', 'read'],
        'update': ['update', 'modify', 'edit', 'change', 'patch', 'put'],
        'delete': ['delete', 'remove', 'cancel', 'deactivate', 'destroy']
    }

    ENTITIES = {
        'user': ['user', 'account', 'customer', 'member', 'profile'],
        'product': ['product', 'item', 'goods', 'merchandise'],
        'order': ['order', 'purchase', 'transaction', 'sale'],
        'payment': ['payment', 'billing', 'charge', 'invoice'],
        'authentication': ['login', 'logout', 'auth', 'authentication', 'session'],
        'cart': ['cart', 'basket', 'shopping cart'],
        'review': ['review', 'rating', 'comment', 'feedback']
    }

    VALIDATIONS = {
        'email': r'email.*(?:valid|format)|valid.*email',
        'password': r'password.*?(\d+)\s*character|character.*?(\d+)',
        'required': r'(?:must|required|mandatory|should have)',
        'unique': r'unique|duplicate|already exists',
        'format': r'format|pattern|valid',
        'length': r'(?:at least|minimum|min)\s*(\d+)',
        'max_length': r'(?:at most|maximum|max)\s*(\d+)'
    }

    HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def __init__(self, llm_service=None):
        """
        Initialize parser with optional LLM service

        Args:
            llm_service: Optional LLMService instance for AI-powered parsing
        """
        self.llm_service = llm_service

    def parse(self, requirements_text: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Parse requirements and extract structured information

        Phase 2: Try LLM first, fallback to rule-based if unavailable

        Args:
            requirements_text: Natural language requirements
            use_llm: Whether to attempt LLM parsing (default: True)

        Returns:
            Dictionary with extracted information
        """

        # Phase 2: Try LLM parsing first if available
        if use_llm and self.llm_service and self.llm_service.is_available():
            try:
                llm_result = self.llm_service.parse_requirements(
                    requirements_text)
                if llm_result:
                    # Merge LLM results with rule-based extraction for missing fields
                    rule_based_result = self._parse_rule_based(
                        requirements_text)
                    return self._merge_results(llm_result, rule_based_result)
            except Exception as e:
                # Fallback to rule-based on error
                print(f"LLM parsing failed, using rule-based: {e}")

        # Phase 1: Rule-based parsing (fallback or default)
        return self._parse_rule_based(requirements_text)

    def _parse_rule_based(self, requirements_text: str) -> Dict[str, Any]:
        """
        Rule-based parsing using regex and keyword matching

        Args:
            requirements_text: Natural language requirements

        Returns:
            Dictionary with extracted information
        """
        result = {
            'entity': self._extract_entity(requirements_text),
            'operations': self._extract_operations(requirements_text),
            'fields': self._extract_fields(requirements_text),
            'validations': self._extract_validations(requirements_text),
            'status_codes': self._extract_status_codes(requirements_text),
            'endpoint': self._extract_endpoint(requirements_text),
            'method': self._extract_http_method(requirements_text),
            'business_rules': self._extract_business_rules(requirements_text),
            'base_url': self._extract_base_url(requirements_text)
        }

        return result

    def _merge_results(self, llm_result: Dict, rule_result: Dict) -> Dict[str, Any]:
        """
        Merge LLM and rule-based results, preferring LLM but filling gaps with rules

        Args:
            llm_result: Results from LLM parsing
            rule_result: Results from rule-based parsing

        Returns:
            Merged results dictionary
        """
        merged = rule_result.copy()

        # Override with LLM results where available and non-empty
        for key, value in llm_result.items():
            if value:  # Only use LLM value if it's not empty/None
                if isinstance(value, list) and len(value) == 0:
                    continue  # Skip empty lists
                merged[key] = value

        return merged

    def _extract_entity(self, text: str) -> str:
        """Extract main entity (user, product, order, etc.)"""
        text_lower = text.lower()

        # Check predefined entities
        for entity, keywords in self.ENTITIES.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return entity

        # Fallback: extract from common patterns
        patterns = [
            r'create\s+(?:a|an)\s+(\w+)',
            r'manage\s+(\w+)',
            r'(\w+)\s+management',
            r'(\w+)\s+api'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1)

        return 'resource'  # default

    def _extract_operations(self, text: str) -> List[str]:
        """Extract CRUD operations mentioned"""
        text_lower = text.lower()
        operations = []

        for operation, keywords in self.OPERATIONS.items():
            for keyword in keywords:
                if re.search(r'\b' + keyword + r'\b', text_lower):
                    if operation not in operations:
                        operations.append(operation)
                    break

        # Check for CRUD keyword
        if 'crud' in text_lower:
            operations = ['create', 'read', 'update', 'delete']

        return operations or ['create']  # default to create

    def _extract_fields(self, text: str) -> List[Dict[str, str]]:
        """Extract field names and types"""
        fields = []
        text_lower = text.lower()

        # Pattern: "with email and password" or "email, password, username"
        patterns = [
            r'with\s+([\w\s,and]+?)(?:\.|,|\n|so that)',
            r'fields?:\s*([\w\s,and]+?)(?:\.|,|\n)',
            r'include[s]?\s+([\w\s,and]+?)(?:\.|,|\n)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                field_text = match.group(1)
                # Split by comma or 'and'
                field_names = re.split(r',|\s+and\s+', field_text)

                for field in field_names:
                    field = field.strip()
                    if field and len(field) < 30:  # Reasonable field name length
                        fields.append({
                            'name': field,
                            'type': self._guess_field_type(field)
                        })
                break

        return fields

    def _guess_field_type(self, field_name: str) -> str:
        """Guess field type from name"""
        field_lower = field_name.lower()

        if 'email' in field_lower:
            return 'email'
        elif 'password' in field_lower or 'pwd' in field_lower:
            return 'password'
        elif 'phone' in field_lower or 'mobile' in field_lower:
            return 'phone'
        elif 'date' in field_lower or 'time' in field_lower:
            return 'datetime'
        elif 'price' in field_lower or 'amount' in field_lower or 'cost' in field_lower:
            return 'number'
        elif 'id' in field_lower or 'number' in field_lower:
            return 'integer'
        elif 'url' in field_lower or 'link' in field_lower:
            return 'url'
        elif 'address' in field_lower:
            return 'address'
        elif 'name' in field_lower:
            return 'name'
        else:
            return 'string'

    def _extract_validations(self, text: str) -> List[Dict[str, Any]]:
        """Extract validation rules"""
        validations = []

        # Email validation
        if re.search(self.VALIDATIONS['email'], text, re.IGNORECASE):
            validations.append({
                'field': 'email',
                'rule': 'format',
                'pattern': 'email'
            })

        # Password length
        match = re.search(r'password.*?(\d+)\s*character', text, re.IGNORECASE)
        if match:
            min_length = int(match.group(1))
            validations.append({
                'field': 'password',
                'rule': 'min_length',
                'value': min_length
            })

        # Unique constraint
        if re.search(self.VALIDATIONS['unique'], text, re.IGNORECASE):
            validations.append({
                'rule': 'unique',
                'type': 'business_rule'
            })

        # Required fields
        if re.search(self.VALIDATIONS['required'], text, re.IGNORECASE):
            validations.append({
                'rule': 'required',
                'type': 'validation'
            })

        return validations

    def _extract_status_codes(self, text: str) -> Dict[str, List[int]]:
        """Extract expected status codes"""
        codes = {'success': [], 'error': []}

        # Pattern: "return 201" or "returns 400" or "status 200"
        matches = re.findall(r'(?:return[s]?|status|code)\s+(\d{3})', text)
        for code in matches:
            code_int = int(code)
            if 200 <= code_int < 300:
                if code_int not in codes['success']:
                    codes['success'].append(code_int)
            else:
                if code_int not in codes['error']:
                    codes['error'].append(code_int)

        # Defaults based on operation
        if not codes['success']:
            if 'create' in text.lower() or 'post' in text.lower():
                codes['success'] = [201]
            else:
                codes['success'] = [200]

        if not codes['error']:
            codes['error'] = [400, 404, 500]

        return codes

    def _extract_endpoint(self, text: str) -> str:
        """Extract API endpoint if mentioned"""
        # Pattern: "endpoint: /api/users" or "API: /users" or "URL: /api/resource"
        patterns = [
            r'(?:endpoint|api|url|path):\s*(/[\w/\-{}]+)',
            r'(?:endpoint|api|url|path)\s+(?:is|=)\s*(/[\w/\-{}]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None  # Will be generated later based on entity

    def _extract_http_method(self, text: str) -> str:
        """Extract HTTP method"""
        text_upper = text.upper()

        # Check if method is explicitly mentioned
        for method in self.HTTP_METHODS:
            if re.search(r'\b' + method + r'\b', text_upper):
                return method

        # Infer from operation keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['create', 'add', 'register', 'signup', 'insert']):
            return 'POST'
        elif any(word in text_lower for word in ['update', 'modify', 'edit']):
            return 'PUT'
        elif any(word in text_lower for word in ['delete', 'remove']):
            return 'DELETE'
        elif any(word in text_lower for word in ['get', 'retrieve', 'fetch', 'list', 'search']):
            return 'GET'
        else:
            return 'POST'  # default

    def _extract_business_rules(self, text: str) -> List[str]:
        """Extract business rules and constraints"""
        rules = []

        # Timeout
        match = re.search(r'(\d+)\s*second[s]?', text, re.IGNORECASE)
        if match:
            rules.append(f'timeout_{match.group(1)}s')

        # Retry logic
        match = re.search(r'retry.*?(\d+)\s*time[s]?', text, re.IGNORECASE)
        if match:
            rules.append(f'retry_{match.group(1)}_times')

        # Fraud detection
        if 'fraud' in text.lower():
            rules.append('fraud_detection')

        # Authentication
        if any(word in text.lower() for word in ['authenticate', 'authorization', 'token', 'jwt']):
            rules.append('authentication_required')

        # Pagination
        if any(word in text.lower() for word in ['pagination', 'page', 'limit', 'offset']):
            rules.append('pagination')

        return rules

    def _extract_base_url(self, text: str) -> str:
        """Extract base URL if mentioned"""
        # Pattern: "http://..." or "https://..."
        match = re.search(
            r'(https?://[\w\.\-:]+(?:/[\w\-]*)?)', text, re.IGNORECASE)
        if match:
            return match.group(1)

        return None
