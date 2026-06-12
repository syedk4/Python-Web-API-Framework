"""
Schema Validator for API Response Validation
Supports JSON Schema validation for dynamic/unpredictable response data
Part of FA-739 Enhancement - Hybrid Validation Approach
"""

import json
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Any

try:
    import jsonschema
    from jsonschema import Draft7Validator, validators
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    Validates API responses against JSON Schema definitions
    
    Features:
    - Industry-standard JSON Schema validation
    - Detailed error reporting
    - Schema caching for performance
    - Fallback when jsonschema not installed
    """
    
    def __init__(self):
        self.schema_cache: Dict[str, dict] = {}
        
        if not JSONSCHEMA_AVAILABLE:
            logger.warning(
                "jsonschema library not installed. Schema validation disabled. "
                "Install with: pip install jsonschema"
            )
    
    def load_schema(self, schema_path: str) -> dict:
        """
        Load JSON schema from file
        
        Args:
            schema_path: Path to schema file (relative to project root)
            
        Returns:
            Schema dictionary
            
        Raises:
            FileNotFoundError: If schema file not found
            json.JSONDecodeError: If schema file is not valid JSON
        """
        # Use cache if available
        if schema_path in self.schema_cache:
            logger.debug(f"Using cached schema: {schema_path}")
            return self.schema_cache[schema_path]
        
        # Load from file
        schema_file = Path(schema_path)
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Cache the schema
            self.schema_cache[schema_path] = schema
            logger.debug(f"Loaded and cached schema: {schema_path}")
            
            return schema
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schema file {schema_path}: {e}")
            raise
    
    def validate(self, response_data: Any, schema: dict) -> Tuple[bool, List[str]]:
        """
        Validate response data against JSON schema
        
        Args:
            response_data: Parsed JSON response (dict, list, etc.)
            schema: JSON Schema dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
            - is_valid: True if validation passed
            - list_of_errors: List of validation error messages (empty if valid)
        """
        if not JSONSCHEMA_AVAILABLE:
            return True, ["Schema validation skipped: jsonschema not installed"]
        
        errors = []
        
        try:
            # Validate using Draft7Validator (most compatible)
            validator = Draft7Validator(schema)
            validation_errors = sorted(validator.iter_errors(response_data), key=str)
            
            if validation_errors:
                for error in validation_errors:
                    # Format error message with path
                    path = " -> ".join(str(p) for p in error.path) if error.path else "root"
                    errors.append(
                        f"Schema validation failed at '{path}': {error.message}"
                    )
                
                logger.debug(f"Schema validation failed with {len(errors)} error(s)")
                return False, errors
            
            logger.debug("Schema validation passed")
            return True, []
            
        except Exception as e:
            error_msg = f"Schema validation error: {str(e)}"
            logger.error(error_msg)
            return False, [error_msg]
    
    def validate_from_file(
        self, 
        response_data: Any, 
        schema_path: str
    ) -> Tuple[bool, List[str]]:
        """
        Load schema from file and validate response
        
        Args:
            response_data: Parsed JSON response
            schema_path: Path to schema file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            schema = self.load_schema(schema_path)
            return self.validate(response_data, schema)
            
        except FileNotFoundError as e:
            error_msg = f"Schema file not found: {schema_path}"
            logger.error(error_msg)
            return False, [error_msg]
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid schema file {schema_path}: {str(e)}"
            logger.error(error_msg)
            return False, [error_msg]
            
        except Exception as e:
            error_msg = f"Error loading schema: {str(e)}"
            logger.error(error_msg)
            return False, [error_msg]

