# FA-1031.csv vs exported_table_76.csv - Failure Analysis

## 🎯 **ROOT CAUSE IDENTIFIED**

All 30 tests in FA-1031.csv are failing because the **request body structure doesn't match the API endpoint requirements**.

---

## **THE CRITICAL DIFFERENCE**

### **exported_table_76.csv** ✅ WORKING
- **Endpoint:** `/ShortageValidation/validate`
- **Request Body:** Flat structure (simple single-item validation)
- **Use Case:** Validate ONE item at a time

```json
{
  "customerNumber": "4444400",
  "shipToNumber": "0001",
  "invoiceNumber": 72682582,
  "itemNumber": "R600006611",
  "serialNumber": "999999",
  "shortageQuantity": 1,
  "defectCode": "XP",
  "locationCode": "WU"
}
```

### **FA-1031.csv** ❌ FAILING
- **Endpoint:** `/ShortageValidation/validate-credit-shortage`
- **Request Body:** **WRONG** - Using flat structure instead of expected nested structure
- **Use Case:** Validate BATCH of items (credit shortage scenario)

**What FA-1031.csv is sending:**
```json
{
  "customerNumber": "4444400",
  "itemNumber": "R600006611",    // ← WRONG! Should be in items[] array
  "serialNumber": "999999",
  "shortageQuantity": 1
}
```

**What the API REQUIRES:**
```json
{
  "replacementInvoiceNumber": "72682582",  // ← REQUIRED!
  "customerNumber": "4444400",
  "shipToNumber": "0001",
  "creditValidation": "Y",                 // ← REQUIRED!
  "raValidation": "Y",                     // ← REQUIRED!
  "correlationId": "STAGE-CORR-001",
  "items": [                               // ← REQUIRED array!
    {
      "itemNumber": "R600006611",
      "quantity": 1,
      "amount": 150.00,
      "defectCode": "XP",
      "locationCode": "WU",
      "serialNumber": "999999"
    }
  ]
}
```

---

## **API ERROR MESSAGES (From Test Report)**

The API is rejecting ALL FA-1031.csv requests with:

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "Items": ["At least one item is required"],
    "ReplacementInvoiceNumber": ["The ReplacementInvoiceNumber field is required."]
  }
}
```

**Translation:**
- ❌ Missing `replacementInvoiceNumber` field
- ❌ Missing `items[]` array
- ❌ Using flat structure for batch endpoint

---

## **DETAILED COMPARISON**

### **TC_001 in FA-1031.csv (FAILING)**

**Current Request Body (Line 2):**
```json
{
  "customerNumber": "4444400",
  "shipToNumber": "0001",
  "invoiceNumber": 72682582,
  "itemNumber": "R600006611",      // ← Should be in items[] array
  "serialNumber": "999999",
  "shortageQuantity": 1,
  "orderNumber": "D299323",
  "amount": 150.00,
  "defectCode": "XP",
  "locationCode": "WU",
  "environment": "AFI"
}
```

**Should Be:**
```json
{
  "replacementInvoiceNumber": "72682582",
  "customerNumber": "4444400",
  "shipToNumber": "0001",
  "creditValidation": "Y",
  "raValidation": "Y",
  "correlationId": "STAGE-TC001-001",
  "environment": "AFI",
  "orderNumber": "D299323",
  "poNumber": "NEED_PO_NUMBER--SH",
  "invoiceAmount": 150.00,
  "items": [
    {
      "itemNumber": "R600006611",
      "quantity": 1,
      "amount": 150.00,
      "defectCode": "XP",
      "locationCode": "WU",
      "serialNumber": "999999"
    }
  ]
}
```

---

## **WHY THIS HAPPENS**

FA-1031.csv appears to have been created by:
1. **Copying** test data from exported_table_76.csv
2. **Changing** only the endpoint from `/validate` to `/validate-credit-shortage`
3. **NOT updating** the request body structure

The two endpoints have **completely different contracts**:

| Feature | `/validate` | `/validate-credit-shortage` |
|---------|-------------|----------------------------|
| **Purpose** | Single item validation | Batch credit shortage validation |
| **Structure** | Flat JSON object | Nested (with items array) |
| **Required** | `customerNumber`, `itemNumber` | `replacementInvoiceNumber`, `items[]`, `creditValidation`, `raValidation` |
| **Use Case** | Quick validation | Full automation workflow |

---

## ✅ **SOLUTION**

You have **TWO OPTIONS**:

### **Option 1: Fix the Endpoint (Quick Fix)**

Change FA-1031.csv to use the correct endpoint:
```
FROM: /ShortageValidation/validate-credit-shortage
TO:   /ShortageValidation/validate
```

**Impact:** Tests will use single-item validation (same as exported_table_76.csv)

---

### **Option 2: Fix the Request Bodies (Correct Fix)**

Update all 30 request bodies in FA-1031.csv to match the batch endpoint requirements:

**For each test:**
1. Add `replacementInvoiceNumber` field
2. Add `creditValidation` field (Y/N)
3. Add `raValidation` field (Y/N)
4. Add `correlationId` field
5. Wrap item data in `items[]` array
6. Add `poNumber` with `--SH` suffix
7. Add `invoiceAmount` field

**Impact:** Tests will properly validate the credit shortage batch endpoint

---

## **RECOMMENDED ACTION**

**Use Option 1** (quick fix) because:
- ✅ Tests can run immediately
- ✅ Validates the same business logic
- ✅ No complex JSON restructuring needed
- ✅ Matches the working exported_table_76.csv pattern

**Later:** Create a NEW test file specifically for batch endpoint with proper structure.

---

## **ADDITIONAL ISSUES IN FA-1031.csv**

1. **Wrong Schema Files:**
   - TC_001-TC_012 use `schemas/fa739/invoice_list_response.json`
   - Should use `schemas/fa739/validation_response.json`

2. **Custom Validators:**
   - Contains unsupported free-text validators
   - Should be cleared (same issue as exported_table_76.csv had)

3. **TC_013-TC_016:**
   - These ARE correctly structured for `/validate-credit-shortage`
   - They already have `items[]` array and required fields
   - Keep these tests but fix schema to `schemas/fa739/credit_shortage_response.json`

---

## **SUMMARY**

| Issue | Impact | Fix |
|-------|--------|-----|
| **Wrong endpoint used** | All 30 tests fail with 400 | Change to `/validate` OR restructure bodies |
| **Wrong request structure** | API rejects: missing `items[]` and `replacementInvoiceNumber` | Add required fields |
| **Wrong schema** | Validation would fail even if API worked | Change to `validation_response.json` |
| **Unsupported validators** | "Unknown custom validator" errors | Clear custom_validator column |

