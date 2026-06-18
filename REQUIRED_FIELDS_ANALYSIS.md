# Required Fields Analysis - API Validation Failures

## 🔍 **ROOT CAUSE: Missing Required Fields**

Based on the error screenshot and API responses, the `/ShortageValidation/validate` endpoint **REQUIRES** these fields:

### **Required Fields:**
1. ✅ `customerNumber` - Customer ID
2. ✅ `shipToNumber` - **REQUIRED** (must be between 1-4 characters)
3. ✅ `invoiceNumber` - **REQUIRED** (must be between 1-99999999)
4. ✅ `itemNumber` - Item/SKU number
5. ✅ `shortageQuantity` - Quantity to validate

### **API Error When Missing:**
```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "ShipToNumber": ["The ShipToNumber field is required."],
    "InvoiceNumber": ["The field InvoiceNumber must be between 1 and 99999999."]
  }
}
```

---

## ❌ **TESTS WITH INCORRECT EXPECTED STATUS CODES**

### **FA-1031_FIXED.csv Issues:**

| Test ID | Missing Fields | Current Expected | Should Be | Fix Needed |
|---------|----------------|------------------|-----------|------------|
| **TC_004** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_006** | `shipToNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_010** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_011** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_012** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_020** | `shipToNumber`, `invoiceNumber` | 400 | 400 | ✅ Already correct |
| **TC_021** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_022** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_023** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_025** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_026** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |
| **TC_028** | `shipToNumber`, `invoiceNumber` | 200 | **400** | ❌ Change to 400 |

---

## 🎯 **BETTER FIX: Add Missing Required Fields**

Instead of changing expected status codes, we should **ADD THE MISSING REQUIRED FIELDS** to the request bodies!

### **Why?**
- ✅ Tests will actually validate business logic (not just input validation)
- ✅ Higher test coverage of actual API functionality
- ✅ More valuable test results

### **How to Fix:**

#### **Option 1: Change Expected Status to 400** (Quick Fix)
- Tests become "negative tests" validating required field checks
- Less valuable - only tests input validation

#### **Option 2: Add Missing Fields** (Proper Fix) ⭐ **RECOMMENDED**
- Add `shipToNumber` and `invoiceNumber` to test bodies
- Tests will validate actual business logic
- Much more valuable

---

## 📝 **PROPOSED FIXES**

### **TC_004: Invalid customer/serial/item combination**
**Current Body:**
```json
{
  "customerNumber": "9999999",
  "itemNumber": "B1367-58",
  "serialNumber": "123456",
  "shortageQuantity": 1,
  "defectCode": "XP",
  "locationCode": "WU",
  "environment": "AFI"
}
```

**Fixed Body:**
```json
{
  "customerNumber": "9999999",
  "shipToNumber": "0001",          // ← ADD THIS
  "invoiceNumber": 99999999,        // ← ADD THIS (dummy invoice)
  "itemNumber": "B1367-58",
  "serialNumber": "123456",
  "shortageQuantity": 1,
  "defectCode": "XP",
  "locationCode": "WU",
  "environment": "AFI"
}
```

**Result:** Test will get past input validation and test the actual customer/serial/item validation logic!

---

### **TC_010, TC_011, TC_012: Defect/Location Code Tests**
These tests are trying to validate **business rules** (defect code validity, location code validity), but they fail at **input validation** first!

**Fix:** Add `shipToNumber` and `invoiceNumber` to all of them.

---

### **TC_021, TC_022, TC_023: API Contract Tests**
These are **Functional** tests trying to validate response structure, but they're failing because of missing required fields!

**Fix:** Add `shipToNumber` and `invoiceNumber` to all of them.

---

### **TC_025, TC_026, TC_028: Integration Tests**
These tests are checking environment-specific behavior and backward compatibility, but fail on required fields!

**Fix:** Add `shipToNumber` and `invoiceNumber` to all of them.

---

## ✅ **RECOMMENDED ACTION**

### **Step 1: Add Missing Fields to All Tests** (Best Practice)

Add these two fields to **EVERY** test that's missing them:
```json
"shipToNumber": "0001",
"invoiceNumber": 99999999
```

### **Step 2: Only Use 400 Status for Actual Input Validation Tests**

Keep these tests with expected 400 (they're testing input validation):
- TC_003: Invalid item number
- TC_007: Zero shortage quantity
- TC_008: Negative shortage quantity  
- TC_009: Invalid defect code
- TC_017: Missing customerNumber
- TC_018: Missing itemNumber
- TC_019: Missing shortageQuantity
- TC_020: SQL injection

---

## 🔧 **IMPLEMENTATION**

I'll create a script to add the missing required fields to all affected tests.

This is the PROPER fix that will make the tests actually validate the business logic they're intended to test!

