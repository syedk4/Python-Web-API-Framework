# FA-739 Quick Start Example

## 🚀 How Schema Validation Would Work

### Current Problem (Screenshot Analysis)

From your screenshot, the API returns:
```json
{
  "runId": 1781189466713,
  "customerNumber": "1256500",
  "invoices": [
    {
      "replacementInvoiceNumber": "72322043",
      "customerNumber": "1256500",
      "creditNumber": "0",
      "shipToNumber": "49",
      "orderNumber": "C951880",
      "tripNumber": null,
      "poNumber": "16241296--SH",
      "invoiceDate": "2026-04-03",
      "invoiceAmount": 277.0300,
      "paidAmount": 0.0000,
      "openAmount": 277.0300,
      "categoryCode": "1",
      "numDays": 69,
      "correlationId": "..."
    }
  ]
}
```

**Current Framework Validation:**
- ✅ Checks: `expected_status` = 200
- ❌ CANNOT validate: `runId` is a number
- ❌ CANNOT validate: `poNumber` ends with `--SH`
- ❌ CANNOT validate: `correlationId` is UUID format
- ❌ CANNOT validate: `invoiceAmount` has 4 decimal places

---

## ✅ After Schema Validation Enhancement

### Test Case CSV:
```csv
test_id,test_name,expected_status,expected_response_schema
TC_001,Verify PO suffix --SH,200,schemas/fa739/invoice_list_response.json
TC_042,Verify runId is number,200,schemas/fa739/invoice_list_response.json
TC_049,Verify correlationId is GUID,200,schemas/fa739/invoice_list_response.json
```

### What Framework Will Validate:

✅ **TC_001 - PO Suffix Validation:**
```
Schema Rule: "poNumber": {"pattern": ".*--SH$"}
Actual Value: "16241296--SH"
Result: ✅ PASS (ends with --SH)
```

✅ **TC_042 - runId Type Validation:**
```
Schema Rule: "runId": {"type": "number"}
Actual Value: 1781189466713
Result: ✅ PASS (is a number)
```

✅ **TC_049 - GUID Format Validation:**
```
Schema Rule: "correlationId": {"format": "uuid"}
Actual Value: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
Result: ✅ PASS (matches UUID pattern)
```

✅ **TC_048 - Decimal Precision Validation:**
```
Schema Rule: "invoiceAmount": {"multipleOf": 0.0001}
Actual Value: 277.0300
Result: ✅ PASS (has 4 decimal places)
```

✅ **TC_046 - Array Type Validation:**
```
Schema Rule: "invoices": {"type": "array"}
Actual Value: [...]
Result: ✅ PASS (is an array)
```

---

## 📊 Example Report Output

### Before (Current Framework):
```
Test ID: TC_001
Status: PASS ✅
Reason: Status code 200 == 200
```
❌ **Problem:** Test passes even if `poNumber` doesn't have `--SH` suffix!

### After (With Schema Validation):
```
Test ID: TC_001
Status: PASS ✅
Validations:
  ✅ HTTP Status: 200 == 200
  ✅ Schema: schemas/fa739/invoice_list_response.json
    ✅ runId is number
    ✅ customerNumber matches pattern ^[0-9]{7}$
    ✅ invoices is array
    ✅ invoices[0].poNumber ends with --SH
    ✅ invoices[0].correlationId is UUID format
    ✅ All required fields present
```

### Example Failure Scenario:
```
Test ID: TC_001
Status: FAIL ❌
Validations:
  ✅ HTTP Status: 200 == 200
  ❌ Schema: schemas/fa739/invoice_list_response.json
    ✅ runId is number
    ✅ customerNumber matches pattern
    ❌ invoices[0].poNumber: '16241296' does not match pattern '.*--SH$'
       Expected: PO number ending with --SH
       Actual: 16241296 (missing --SH suffix)
    ✅ invoices[0].correlationId is UUID
```

---

## 🔧 Implementation Preview

### New Column in CSV:
```csv
test_id,method,base_url,endpoint,body,expected_status,expected_response_schema
TC_001,POST,https://...,/api/OpenInvoices/runs,{...},200,schemas/fa739/invoice_list_response.json
```

### Framework Logic (Simplified):
```python
# In test_executor.py
def execute_single_test(self, test_data):
    # Execute request
    response = requests.post(url, json=body)
    
    # Step 1: Validate status code (existing)
    status_passed = (response.status_code == test_data['expected_status'])
    
    # Step 2: Validate schema (NEW!)
    schema_passed = True
    schema_errors = []
    
    if test_data.get('expected_response_schema'):
        schema = self._load_schema(test_data['expected_response_schema'])
        schema_passed, schema_errors = self.schema_validator.validate(
            response.json(), 
            schema
        )
    
    # Overall result: Both must pass
    overall_passed = status_passed and schema_passed
    
    return TestResult(
        passed=overall_passed,
        status_validation=status_passed,
        schema_validation=schema_passed,
        schema_errors=schema_errors
    )
```

---

## 💡 Real-World Example Mapping

### FA-739 Test Cases → Schema Validation:

| Test Case | Current Approach | Schema Solution |
|-----------|-----------------|----------------|
| **TC_001: PO suffix --SH** | ❌ Can't validate | ✅ Pattern: `.*--SH$` |
| **TC_002: Unique runId** | ❌ Can't validate | ⚙️ Custom validator (store previous) |
| **TC_003: Required fields** | ❌ Can't validate | ✅ `required: ["runId", "customerNumber", ...]` |
| **TC_042: runId is number** | ❌ Can't validate | ✅ `type: "number"` |
| **TC_046: invoices is array** | ❌ Can't validate | ✅ `type: "array"` |
| **TC_048: 4 decimal precision** | ❌ Can't validate | ✅ `multipleOf: 0.0001` |
| **TC_049: GUID format** | ❌ Can't validate | ✅ `format: "uuid"` |
| **TC_054: Amount calculation** | ❌ Can't validate | ⚙️ Custom validator |
| **TC_055: Date calculation** | ❌ Can't validate | ⚙️ Custom validator |

**Legend:**
- ✅ = Solved by JSON Schema alone
- ⚙️ = Requires custom validator (Phase 2)

**Result:** 40+ out of 56 test cases automated with Phase 1!

---

## 🎯 Why This Is Better

### Scenario: API Bug Introduced

**Bug:** Developer accidentally removes `--SH` suffix from PO numbers

**Current Framework:**
```
TC_001: PASS ✅ (200 status code)
```
❌ Bug goes undetected!

**With Schema Validation:**
```
TC_001: FAIL ❌
Schema Error: invoices[0].poNumber '16241296' does not match pattern '.*--SH$'
```
✅ Bug caught immediately!

---

## 📝 Next Steps

1. **Review** this document and the main suggestion (`FA-739_VALIDATION_ENHANCEMENT_SUGGESTION.md`)
2. **Decide** if schema validation approach fits your needs
3. **Pilot** with 5 test cases (TC_001, TC_042, TC_046, TC_048, TC_049)
4. **Expand** to all 56 FA-739 test cases
5. **Rollout** to other teams/APIs

---

## ❓ Questions to Consider

1. **Do you want backward compatibility?** (Yes → keep existing `expected_response` column)
2. **Who creates schemas?** (QA team, developers, or auto-generated?)
3. **Schema reusability?** (Share common schemas across test cases?)
4. **Custom validators needed?** (TC_002, TC_054, TC_055 require custom logic)

---

## 📞 Ready to Implement?

If you want to proceed, I can:
1. ✅ Create the `SchemaValidator` class
2. ✅ Update `test_executor.py` to support schema validation
3. ✅ Update CSV parser to read `expected_response_schema` column
4. ✅ Update report generator to show schema validation results
5. ✅ Create sample test cases for FA-739

Just let me know! 🚀

