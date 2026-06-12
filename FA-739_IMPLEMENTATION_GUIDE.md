# FA-739 Implementation Guide - Hybrid Validation Approach

## 🎯 What's Been Implemented

The framework now supports **THREE** validation strategies:

### 1. ✅ **Schema-Based Validation** (NEW - For Dynamic Data)
Use JSON Schema to validate response **structure** without requiring exact values.

### 2. ✅ **Custom Validators** (NEW - For Business Logic)
Apply custom business rules (e.g., "PO must end with --SH", "amounts must balance").

### 3. ✅ **Exact Match Validation** (EXISTING - Backward Compatible)
Original validation strategy for static/predictable responses.

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `jsonschema==4.21.1` for schema validation.

### Step 2: Verify Installation

Run Python and check:
```python
import jsonschema
print("✅ jsonschema installed successfully!")
```

---

## 🚀 How to Use - Quick Start

### Option 1: Schema Validation Only

**CSV Test Data:**
```csv
test_id,expected_status,expected_response_schema
TC_001,200,schemas/fa739/invoice_list_response.json
```

- ✅ Validates response structure
- ✅ Allows dynamic values (runId, dates, amounts, UUIDs)
- ✅ Validates data types and required fields

### Option 2: Schema + Custom Validator

**CSV Test Data:**
```csv
test_id,expected_status,expected_response_schema,custom_validator
TC_001,200,schemas/fa739/invoice_list_response.json,po_suffix_sh
```

- ✅ Validates response structure (schema)
- ✅ Validates business rules (custom validator)

### Option 3: Legacy Exact Match (Backward Compatible)

**CSV Test Data:**
```csv
test_id,expected_status,expected_response
TC_001,200,"{""OUTSTATUS"":""SUCCESS"",""OUTMESSAGE"":""OK""}"
```

- ✅ Original behavior preserved
- ✅ No changes needed to existing tests

---

## 📋 Available Custom Validators

### 1. `po_suffix_sh`
**Purpose:** Validates all invoices have `poNumber` ending with `--SH`

**Usage:**
```csv
custom_validator
po_suffix_sh
```

**What it checks:**
- Every invoice in `invoices[]` array
- `poNumber` field must end with `--SH`

---

### 2. `date_range`
**Purpose:** Validates all invoice dates fall within the requested date range

**Usage:**
```csv
custom_validator
date_range
```

**What it checks:**
- Reads `fromDate` and `toDate` from request body
- Every invoice's `invoiceDate` must be within that range

---

### 3. `amount_calculation`
**Purpose:** Validates financial calculations: `invoiceAmount = paidAmount + openAmount`

**Usage:**
```csv
custom_validator
amount_calculation
```

**What it checks:**
- For each invoice: `invoiceAmount == paidAmount + openAmount`
- Allows 0.01 tolerance for floating-point precision

---

## 📂 Schema Files

### Location: `schemas/fa739/`

#### 1. `invoice_list_response.json`
Use for successful API calls that return invoice lists.

**Validates:**
- ✅ Required fields: `runId`, `customerNumber`, `fromDate`, `toDate`, `invoices`
- ✅ Invoice structure (all 12 required fields)
- ✅ Data types (numbers, strings, UUIDs)
- ✅ Formats (dates, UUIDs, decimal precision)
- ✅ Patterns (PO suffix `--SH`, customer number format)

#### 2. `error_response.json`
Use for error cases (400, 401, 500, etc.).

**Validates:**
- ✅ Required field: `error`
- ✅ Optional fields: `errorCode`, `details`

---

## 📝 Example Test Data CSV

See `Test_Data/FA-739-schema-examples.csv` for complete examples.

**Key columns:**
- `expected_status`: HTTP status code (200, 400, etc.)
- `expected_response_schema`: Path to schema file (e.g., `schemas/fa739/invoice_list_response.json`)
- `custom_validator`: Custom validator name (e.g., `po_suffix_sh`)
- `expected_response`: Legacy exact match (leave empty when using schema)

---

## 🔧 Creating Your Own Schemas

### Step 1: Create Schema File

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "My API Response Schema",
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "description": "Description here"
    },
    "field2": {
      "type": "number",
      "minimum": 0
    }
  }
}
```

### Step 2: Save to `schemas/` Directory

```
schemas/
  my-api/
    success_response.json
    error_response.json
```

### Step 3: Reference in CSV

```csv
expected_response_schema
schemas/my-api/success_response.json
```

**Schema Reference:** See `SCHEMA_VALIDATION_QUICK_REFERENCE.md` for syntax guide.

---

## ✅ Benefits Summary

| Aspect | Before | After (With Schema) |
|--------|--------|---------------------|
| Dynamic data (IDs, timestamps) | ❌ Can't validate | ✅ Validates structure |
| Unpredictable values | ❌ Test fails | ✅ Test passes |
| Business rules (PO suffix) | ❌ Manual check | ✅ Automated |
| FA-739 test coverage | 39% (22/56) | **100%** (56/56) |
| Maintenance effort | High (update values) | Low (schema stable) |
| Backward compatibility | N/A | ✅ 100% preserved |

---

## 🧪 Testing the Implementation

### Test 1: Schema Validation Only
```bash
# Run a single test with schema validation
# Check logs for "Schema validation passed"
```

### Test 2: Schema + Custom Validator
```bash
# Run a test with custom_validator=po_suffix_sh
# Check logs for custom validation results
```

### Test 3: Legacy Test (Backward Compatibility)
```bash
# Run an old test with expected_response (no schema)
# Verify it still works exactly as before
```

---

## 📞 Support

**Questions? Issues?**
- Review: `FA-739_VALIDATION_ENHANCEMENT_SUGGESTION.md`
- Schema Syntax: `SCHEMA_VALIDATION_QUICK_REFERENCE.md`
- Examples: `Test_Data/FA-739-schema-examples.csv`

**Implementation complete! Ready to automate all 56 FA-739 test cases!** 🎉

