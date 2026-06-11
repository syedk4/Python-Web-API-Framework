# Schema Validation Quick Reference Card

## 🎯 Common Validation Patterns for FA-739

### Data Type Validations

```json
{
  "runId": {"type": "number"},                    // Must be numeric
  "customerNumber": {"type": "string"},           // Must be string
  "invoices": {"type": "array"},                  // Must be array
  "isActive": {"type": "boolean"},                // Must be true/false
  "metadata": {"type": "object"}                  // Must be JSON object
}
```

### Pattern Matching (Regex)

```json
{
  "poNumber": {
    "type": "string",
    "pattern": ".*--SH$"                          // Must end with --SH
  },
  "customerNumber": {
    "type": "string", 
    "pattern": "^[0-9]{7}$"                       // Exactly 7 digits
  },
  "correlationId": {
    "type": "string",
    "format": "uuid"                              // Must be GUID format
  },
  "invoiceDate": {
    "type": "string",
    "format": "date",                             // Must be YYYY-MM-DD
    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
  }
}
```

### Numeric Validations

```json
{
  "invoiceAmount": {
    "type": "number",
    "minimum": 0,                                 // Must be >= 0
    "multipleOf": 0.0001                          // 4 decimal places
  },
  "numDays": {
    "type": "integer",
    "minimum": 0,                                 // Non-negative integer
    "maximum": 365                                // <= 365
  }
}
```

### Required Fields

```json
{
  "type": "object",
  "required": [                                   // These fields MUST exist
    "runId",
    "customerNumber", 
    "fromDate",
    "toDate",
    "invoices"
  ],
  "properties": { ... }
}
```

### Array Validations

```json
{
  "invoices": {
    "type": "array",
    "minItems": 1,                                // At least 1 item
    "maxItems": 1000,                             // At most 1000 items
    "items": {
      "$ref": "#/definitions/invoice"             // Each item must match schema
    }
  }
}
```

### String Length

```json
{
  "orderNumber": {
    "type": "string",
    "minLength": 1,                               // At least 1 character
    "maxLength": 20                               // At most 20 characters
  }
}
```

### Allowed Values (Enum)

```json
{
  "division": {
    "type": "string",
    "enum": ["ALL", "EAST", "WEST", "CENTRAL"]    // Must be one of these
  },
  "creditNumber": {
    "type": "string",
    "pattern": "^(0|[1-9][0-9]*)$"                // "0" or positive number
  }
}
```

---

## 📋 FA-739 Test Case Mapping

| Test Case | Validation Need | Schema Solution |
|-----------|----------------|-----------------|
| TC_001 | PO ends with `--SH` | `"pattern": ".*--SH$"` |
| TC_003 | Required fields present | `"required": ["runId", ...]` |
| TC_042 | runId is number | `"type": "number"` |
| TC_043 | customerNumber is string | `"type": "string"` |
| TC_044 | fromDate is date format | `"format": "date"` |
| TC_046 | invoices is array | `"type": "array"` |
| TC_048 | 4 decimal precision | `"multipleOf": 0.0001` |
| TC_049 | GUID format | `"format": "uuid"` |
| TC_050 | All invoice fields required | `"required": [...]` in invoice definition |

---

## 🔧 CSV Configuration Examples

### Simple Schema Validation
```csv
test_id,expected_status,expected_response_schema
TC_001,200,schemas/fa739/invoice_list_response.json
TC_042,200,schemas/fa739/invoice_list_response.json
TC_046,200,schemas/fa739/invoice_list_response.json
```

### Error Response Validation
```csv
test_id,expected_status,expected_response_schema
TC_009,400,schemas/fa739/error_response.json
TC_010,400,schemas/fa739/error_response.json
TC_012,400,schemas/fa739/error_response.json
```

### Hybrid (Schema + Custom Rules)
```csv
test_id,expected_status,expected_response_schema,validation_rules
TC_054,200,schemas/fa739/invoice_list_response.json,custom:validate_amount_calculation
TC_055,200,schemas/fa739/invoice_list_response.json,custom:validate_invoice_age
```

### Legacy (Backward Compatible)
```csv
test_id,expected_status,expected_response
TC_OLD,200,"{""OUTSTATUS"":""S"",""OUTMESSAGE"":""Success""}"
```

---

## 📝 Complete Example: FA-739 Invoice Schema

### Minimal Schema (Quick Start)
```json
{
  "type": "object",
  "required": ["runId", "invoices"],
  "properties": {
    "runId": {"type": "number"},
    "invoices": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "poNumber": {"type": "string", "pattern": ".*--SH$"}
        }
      }
    }
  }
}
```

### Comprehensive Schema (Production Ready)
See `schemas/fa739/invoice_list_response.json`

---

## 🚀 Quick Setup Steps

1. **Install dependency:**
   ```bash
   pip install jsonschema
   ```

2. **Create schema file:**
   Save to `schemas/fa739/invoice_list_response.json`

3. **Update CSV:**
   Add column `expected_response_schema`

4. **Run test:**
   Framework automatically validates!

---

## 💡 Tips & Best Practices

### Start Simple
✅ Begin with basic type validation  
✅ Add patterns incrementally  
✅ Test with known good/bad responses

### Reuse Schemas
✅ One schema file → multiple test cases  
✅ Define common structures in `definitions`  
✅ Use `$ref` to avoid duplication

### Version Control
✅ Store schemas in version control  
✅ Document changes in schema comments  
✅ Use schema versioning if API versions differ

### Error Messages
✅ Schema validator provides detailed errors  
✅ Shows exactly which field failed  
✅ Shows expected vs actual values

---

## 🐛 Troubleshooting

### "Schema validation failed: 'invoices' is a required property"
**Problem:** Response missing required field  
**Solution:** Either fix API or update schema `required` list

### "Pattern '.*--SH$' does not match '16241296'"
**Problem:** poNumber doesn't end with --SH  
**Solution:** API bug - should add --SH suffix

### "Type number expected, got string"
**Problem:** runId is "1234" instead of 1234  
**Solution:** API returning wrong data type

---

## 📚 Resources

- **JSON Schema Docs:** https://json-schema.org/
- **Online Validator:** https://www.jsonschemavalidator.net/
- **Schema Generator:** https://www.jsonschema.net/
- **Python jsonschema:** https://python-jsonschema.readthedocs.io/

---

## ✅ Summary

**Before:**
```python
if response.status_code == 200:
    test_passed = True  # ❌ Only checks status
```

**After:**
```python
if response.status_code == 200:
    if schema_validates(response.json(), schema):
        test_passed = True  # ✅ Checks status AND structure
```

**Result:** More accurate, comprehensive test validation!

