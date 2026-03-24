# Quick Verification Guide - Base URL Fix

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Generate Scenarios**

1. Go to: http://localhost:5000/scenario-generator
2. Paste this user story:
   ```
   API URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction/PDFViewer
   API Key: 0c4b24cf-0211-4dcb-8f2f-280ab556ca78
   
   Create a POST endpoint that accepts environment, customerNumber, shipTo, invoiceNumber, orderNumber, and languageCheck fields.
   Returns 200 on success, 400 for validation errors.
   ```
3. Click "Generate Scenarios"

---

### **Step 2: Check Terminal Output**

**Look for this in your terminal:**

```
================================================================================
PARSING METHOD: LLM (AI-Powered)
================================================================================
Parsed Data:
{
  ...
  "base_url": "http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction",
  "endpoint": "/PDFViewer",
  ...
}
================================================================================
```

**✅ GOOD:** base_url and endpoint are correct  
**❌ BAD:** base_url is empty or shows "jsonplaceholder.typicode.com"

---

### **Step 3: Run Verification Script**

```powershell
python verify_csv.py
```

**Expected Output:**

```
================================================================================
CSV VERIFICATION RESULTS
================================================================================
File: Test_Data/generated-scenarios.csv
Total scenarios: 15
================================================================================

First Scenario Details:
Test ID: TC-001
Test Name: Create invoice with valid data
Method: POST
Base URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction
Endpoint: /PDFViewer

Verification:
--------------------------------------------------------------------------------
✅ Base URL is CORRECT!
   http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction
✅ Endpoint is CORRECT!
   /PDFViewer

Checking All Scenarios:
--------------------------------------------------------------------------------
✅ All scenarios use the same base_url
✅ All scenarios use the same endpoint

Checking for Hardcoded Defaults:
--------------------------------------------------------------------------------
✅ No jsonplaceholder.typicode.com found
✅ No api.example.com found

================================================================================
🎉 VERIFICATION PASSED! All checks successful!
================================================================================
```

---

## 📊 **What to Look For**

### **✅ CORRECT (After Fix):**

**In CSV file:**
```csv
base_url,endpoint
http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction,/PDFViewer
http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction,/PDFViewer
http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction,/PDFViewer
```

**Key Points:**
- ✅ base_url includes the service path `/WebAPI/InvoiceExtraction`
- ✅ endpoint is just the final resource `/PDFViewer`
- ✅ All rows have the same values
- ✅ No `jsonplaceholder.typicode.com`

---

### **❌ WRONG (Before Fix):**

**In CSV file:**
```csv
base_url,endpoint
https://jsonplaceholder.typicode.com,/WebAPI/InvoiceExtraction/PDFViewer
https://jsonplaceholder.typicode.com,/WebAPI/InvoiceExtraction/PDFViewer
https://jsonplaceholder.typicode.com,/WebAPI/InvoiceExtraction/PDFViewer
```

**Problems:**
- ❌ base_url is hardcoded default
- ❌ endpoint has the full path (wrong split)
- ❌ Using jsonplaceholder instead of your API

---

## 🔍 **Manual CSV Check (Without Script)**

### **Option 1: Open in Excel**

1. Open `Test_Data/generated-scenarios.csv` in Excel
2. Find the `base_url` column (usually column C)
3. Check the first row value
4. **Should be:** `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
5. Find the `endpoint` column (usually column F)
6. Check the first row value
7. **Should be:** `/PDFViewer`

---

### **Option 2: Open in Notepad/VS Code**

1. Open `Test_Data/generated-scenarios.csv` in Notepad or VS Code
2. Look at the first data row (line 2)
3. Find the base_url value (3rd column)
4. Find the endpoint value (6th column)

**Example line:**
```csv
TC-001,Create invoice with valid data,Functional,P0,POST,http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction,/PDFViewer,Content-Type: application/json,...
```

---

## 🐛 **Common Issues & Solutions**

### **Issue 1: Verification script shows "CSV file not found"**

**Solution:**
```powershell
# Check if file exists
dir Test_Data\generated-scenarios.csv

# If not found, generate scenarios first in the web UI
```

---

### **Issue 2: Base URL still shows jsonplaceholder**

**Solution:**
1. Restart the application to reload the updated code:
   ```powershell
   # Press Ctrl+C to stop
   python app.py
   ```
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try generating scenarios again

---

### **Issue 3: Endpoint shows full path instead of /PDFViewer**

**Solution:**
- The LLM might not be splitting correctly
- Check if the user story clearly labels "API URL:"
- Try adding more explicit labels:
  ```
  Base URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction
  Endpoint: /PDFViewer
  ```

---

## 📝 **Verification Checklist**

Use this checklist to verify the fix:

- [ ] Application is running (http://localhost:5000)
- [ ] Navigated to Scenario Generator
- [ ] LLM toggle is ON (green)
- [ ] Pasted user story with API URL
- [ ] Clicked "Generate Scenarios"
- [ ] Terminal shows correct parsed base_url
- [ ] Terminal shows correct parsed endpoint
- [ ] Scenarios generated successfully
- [ ] Downloaded CSV file
- [ ] Ran `python verify_csv.py`
- [ ] Verification script shows ✅ PASSED
- [ ] Manually checked CSV in Excel/Notepad
- [ ] base_url column has correct value
- [ ] endpoint column has correct value
- [ ] No jsonplaceholder.typicode.com found

---

## 🎯 **Success Criteria**

**The fix is working correctly if ALL of these are true:**

1. ✅ Terminal shows correct base_url in parsed data
2. ✅ Terminal shows correct endpoint in parsed data
3. ✅ CSV base_url = `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
4. ✅ CSV endpoint = `/PDFViewer`
5. ✅ All scenarios use the same base_url
6. ✅ All scenarios use the same endpoint
7. ✅ No hardcoded defaults (jsonplaceholder, api.example.com)
8. ✅ Verification script shows "VERIFICATION PASSED"

---

## 🎉 **Next Steps After Verification**

Once verification passes:

1. **Test with real API:**
   - Go to Test Runner
   - Select the generated CSV
   - Run tests against your actual API

2. **Create more scenarios:**
   - Try different user stories
   - Test various API endpoints
   - Verify each one has correct base_url

3. **Document your API patterns:**
   - Note how your URLs are structured
   - Share examples with the team
   - Update user story templates

---

**Need help? Check `VERIFY_BASE_URL_FIX.md` for detailed instructions!**

