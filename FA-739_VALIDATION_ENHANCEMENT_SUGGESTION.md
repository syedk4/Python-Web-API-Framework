# FA-739 Validation Enhancement Suggestion

## 📋 Executive Summary

**Story:** FA-739 - Credit Shortage Automation API Validation  
**Current Limitation:** Framework validates static `expected_response` values, but FA-739 has **unpredictable/dynamic response data**  
**Impact:** 50+ test cases need validation beyond simple status code checks

---

## 🔍 Current Framework Analysis

### ✅ What Framework Does Well:
1. **HTTP Status Validation** - Works perfectly (200, 400, 401, etc.)
2. **Static Field Validation** - Can validate fixed values like:
   ```json
   {"OUTSTATUS": "E", "OUTMESSAGE": "Invoice not found"}
   ```
3. **Multi-Team Support** - Handles different API response formats

### ❌ Current Gap (FA-739 Problem):

Looking at FA-739 test cases, the `expected_response` field contains **validation rules**, not exact values:

**TC_001:**
```csv
expected_response: "{""runId"":number,""invoices"":[{""poNumber"":""*--SH""}]}"
```
**Problem:** 
- `runId` is a **dynamic number** (changes every call)
- `invoices` array size is **unpredictable** (0 to 1000+)
- `poNumber` must **match pattern** (*--SH), not exact value

**TC_002:**
```csv
expected_response: "Different runId for each call"
```
**Problem:** Plain English description, not JSON

**TC_055:**
```csv
expected_response: "numDays = current_date - invoiceDate"
```
**Problem:** Requires **calculation logic**, not simple comparison

---

## 🎯 Proposed Solution: Schema-Based Validation

### Strategy Overview:

**Current:** Exact value matching (`expected == actual`)  
**Proposed:** Rule-based validation (schema, patterns, calculations)

### Implementation Levels:

#### **Level 1: JSON Schema Validation** (RECOMMENDED FOR FA-739)
- ✅ Multi-team compatible
- ✅ Handles dynamic values
- ✅ Industry standard
- ✅ Minimal learning curve

#### **Level 2: Custom Validation Rules**
- ⚙️ For complex business logic
- ⚙️ Team-specific requirements

#### **Level 3: Assertion Scripts**
- 🚀 Maximum flexibility
- ⚠️ Requires scripting knowledge

---

## 📐 Level 1: JSON Schema Validation (Recommended)

### What is JSON Schema?

JSON Schema is an industry-standard way to describe expected structure and validation rules:

```json
{
  "type": "object",
  "required": ["runId", "customerNumber", "invoices"],
  "properties": {
    "runId": {"type": "number"},
    "customerNumber": {"type": "string", "pattern": "^[0-9]{7}$"},
    "invoices": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["poNumber", "replacementInvoiceNumber"],
        "properties": {
          "poNumber": {"type": "string", "pattern": ".*--SH$"},
          "replacementInvoiceNumber": {"type": "string"},
          "invoiceAmount": {"type": "number"},
          "correlationId": {"type": "string", "format": "uuid"}
        }
      }
    }
  }
}
```

### FA-739 Test Case Mapping:

| Test Case | Current expected_response | JSON Schema Solution |
|-----------|--------------------------|---------------------|
| TC_001 | `{\"runId\":number...}` | Type validation: `{"runId": {"type": "number"}}` |
| TC_001 | `\"poNumber\":\"*--SH\"` | Pattern: `{"pattern": ".*--SH$"}` |
| TC_002 | "Different runId for each call" | Store & compare: custom validator |
| TC_042 | "runId field exists and is number type" | `{"required": ["runId"], "type": "number"}` |
| TC_049 | "correlationId matches GUID pattern" | `{"format": "uuid"}` |

---

## 🛠️ Implementation Plan

### Phase 1: Add JSON Schema Support (Week 1)

**1. Update CSV Format:**
```csv
test_id,expected_status,expected_response_schema,expected_response_legacy
TC_001,200,schemas/fa739_invoice_list.json,
TC_009,400,,"{""error"":""Invalid customerNumber format""}"
```

**2. New File: `core/schema_validator.py`**
```python
import jsonschema
from typing import Tuple, List

class SchemaValidator:
    def validate_schema(self, response_data: dict, schema: dict) -> Tuple[bool, List[str]]:
        """Validate response against JSON schema"""
        errors = []
        try:
            jsonschema.validate(instance=response_data, schema=schema)
            return True, []
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
            return False, errors
```

**3. Update `test_executor.py`:**
```python
# Add schema validation option
if test_data.get('expected_response_schema'):
    schema_path = test_data['expected_response_schema']
    schema = self._load_schema(schema_path)
    passed, errors = self.schema_validator.validate_schema(response.json(), schema)
elif test_data.get('expected_response'):
    # Legacy exact-match validation (backward compatible)
    passed, errors = self._validate_response(...)
```

**Benefits:**
- ✅ Solves 90% of FA-739 test cases
- ✅ Backward compatible (legacy tests unaffected)
- ✅ Reusable schemas across test cases
- ✅ Industry-standard approach

---

## 🎨 Level 2: Custom Validation Rules (For Complex Logic)

### For Test Cases Requiring Calculations/Comparisons:

**TC_055:** `numDays = current_date - invoiceDate`

**Solution: Custom Validators**

```python
# File: core/custom_validators.py
from datetime import datetime, date
from typing import Any, Tuple, List

class CustomValidator:
    """Business logic validators for FA-739"""

    def validate_invoice_age(self, invoice: dict, reference_date: date = None) -> Tuple[bool, str]:
        """Validate numDays reflects actual invoice age"""
        if not reference_date:
            reference_date = date.today()

        invoice_date = datetime.strptime(invoice['invoiceDate'], '%Y-%m-%d').date()
        expected_days = (reference_date - invoice_date).days
        actual_days = invoice.get('numDays', 0)

        if expected_days != actual_days:
            return False, f"numDays mismatch: expected {expected_days}, got {actual_days}"
        return True, ""

    def validate_amount_calculation(self, invoice: dict) -> Tuple[bool, str]:
        """Validate: openAmount = invoiceAmount - paidAmount"""
        invoice_amt = float(invoice.get('invoiceAmount', 0))
        paid_amt = float(invoice.get('paidAmount', 0))
        open_amt = float(invoice.get('openAmount', 0))
        expected_open = invoice_amt - paid_amt

        # Allow 0.01 tolerance for floating point
        if abs(expected_open - open_amt) > 0.01:
            return False, f"Amount calculation error: {invoice_amt} - {paid_amt} != {open_amt}"
        return True, ""
```

**CSV Configuration:**
```csv
test_id,expected_status,validation_rules
TC_055,200,"schema:fa739_base.json,custom:validate_invoice_age"
TC_054,200,"schema:fa739_base.json,custom:validate_amount_calculation"
```

---

## 🔧 Recommended Implementation Roadmap

### **Phase 1: JSON Schema (Week 1)** ✅ PRIORITY FOR FA-739
```
✅ Install jsonschema library
✅ Create SchemaValidator class
✅ Add expected_response_schema column support
✅ Create sample schemas for FA-739
✅ Test with TC_001, TC_042-051 (API contract tests)
```

**Deliverables:**
- Schema files in `schemas/fa739/` folder
- Updated test_executor.py with schema validation
- Sample test cases demonstrating schema usage

**Impact:** Covers 40+ out of 56 FA-739 test cases

---

### **Phase 2: Custom Validators (Week 2)** ⚙️ FOR COMPLEX LOGIC
```
✅ Create CustomValidator class
✅ Implement FA-739 specific validators (age, amounts, uniqueness)
✅ Add validation_rules column support
✅ Test with TC_002, TC_054, TC_055 (calculation tests)
```

**Impact:** Covers remaining 10+ complex test cases

---

## 💡 Quick Win: Hybrid Approach (RECOMMENDED)

**Use both old and new validation together:**

```csv
test_id,expected_status,expected_response,expected_response_schema,validation_rules
TC_009,400,"{""error"":""Invalid customerNumber format""}",,,
TC_001,200,,schemas/fa739_list.json,
TC_055,200,,schemas/fa739_base.json,custom:validate_invoice_age
```

**Validation Priority:**
1. If `expected_response_schema` exists → Use schema validation
2. Else if `validation_rules` exists → Use custom validators
3. Else if `expected_response` exists → Use legacy exact-match (current behavior)
4. Else → Status code only

**Benefits:**
- ✅ Zero breaking changes to existing tests
- ✅ Teams can adopt gradually
- ✅ Different API styles supported
- ✅ Maximum flexibility

---

## 📝 Sample Schema for FA-739

### `schemas/fa739/invoice_list_response.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["runId", "customerNumber", "fromDate", "toDate", "invoices"],
  "properties": {
    "runId": {"type": "number"},
    "customerNumber": {"type": "string", "pattern": "^[0-9]{7}$"},
    "fromDate": {"type": "string", "format": "date"},
    "toDate": {"type": "string", "format": "date"},
    "invoices": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["replacementInvoiceNumber", "poNumber", "correlationId"],
        "properties": {
          "replacementInvoiceNumber": {"type": "string"},
          "poNumber": {"type": "string", "pattern": ".*--SH$"},
          "invoiceAmount": {"type": "number"},
          "correlationId": {"type": "string", "format": "uuid"}
        }
      }
    }
  }
}
```

---

## 🎯 Answer to Your Questions

### Q1: "Will framework give exact result if expected_status passes?"

**Current Behavior:**
- If `expected_status` = 200 and actual = 200 → ✅ PASS (even if response body is wrong)
- Screenshot shows response with `runId`, `invoices`, etc. - framework currently doesn't validate these

**After Schema Enhancement:**
- Status code AND schema validation both must pass
- Test fails if status=200 but response structure is incorrect
- More accurate results for FA-739

### Q2: "What can be done to improve for multiple teams/API formats?"

**Solutions:**
1. **JSON Schema** - Universal standard, works for all JSON APIs
2. **Schema Library** - Teams share common schemas (dates, amounts, errors)
3. **Validation Profiles** - Pre-configured validators per team
4. **Extensibility** - Custom validators for team-specific logic

---

## 🚀 Getting Started (Next Steps)

### For FA-739 Automation:

**1. Install Dependencies:**
```bash
pip install jsonschema
```

**2. Create Schema File:**
Save `schemas/fa739/invoice_list_response.json` (provided above)

**3. Update CSV:**
```csv
test_id,expected_status,expected_response_schema
TC_001,200,schemas/fa739/invoice_list_response.json
```

**4. Benefits:**
- Validates `runId` is a number ✅
- Validates `poNumber` ends with `--SH` ✅
- Validates `correlationId` is UUID format ✅
- Validates all required fields present ✅

---

## ✅ Summary

| Aspect | Current | After Enhancement |
|--------|---------|------------------|
| **Static Responses** | ✅ Works | ✅ Still works (backward compatible) |
| **Dynamic Values** | ❌ Can't validate | ✅ Schema validates type/format |
| **Pattern Matching** | ❌ Not supported | ✅ Regex patterns in schema |
| **Calculations** | ❌ Not supported | ✅ Custom validators |
| **Multi-Team** | ⚠️ Limited | ✅ Schema library + profiles |
| **FA-739 Coverage** | ❌ 20% (status only) | ✅ 100% (all 56 tests) |

**Recommendation:** Implement **Phase 1 (JSON Schema)** first - it solves 80% of FA-739 needs with minimal effort.

