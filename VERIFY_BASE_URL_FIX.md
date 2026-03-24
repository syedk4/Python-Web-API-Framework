# How to Verify Base URL Extraction Fix

## 🎯 **Verification Goal**

Verify that the generated CSV file contains the correct `base_url` and `endpoint` values after the fix.

---

## 📋 **Step-by-Step Verification Process**

### **Step 1: Start the Application**

1. **Open Terminal/PowerShell** in the project directory
2. **Run the application:**
   ```powershell
   python app.py
   ```
3. **Wait for the message:**
   ```
   Server running at: http://localhost:5000
   ```

---

### **Step 2: Navigate to Scenario Generator**

1. **Open your browser** and go to: http://localhost:5000/scenario-generator
2. **Ensure LLM toggle is ON** (should show "LLM Parsing: Enabled")

---

### **Step 3: Enter Your User Story**

**Copy and paste this exact user story:**

```
API URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction/PDFViewer
API Key: 0c4b24cf-0211-4dcb-8f2f-280ab556ca78

Create a POST endpoint that accepts the following fields:
- environment (string, required)
- customerNumber (string, required)
- shipTo (string, required)
- invoiceNumber (string, required)
- orderNumber (string, required)
- languageCheck (string, required)

Returns 200 on success, 400 for validation errors, 500 for server errors.
```

**Click:** "Generate Scenarios"

---

### **Step 4: Check the Parsing Results**

**In the terminal/console, you should see:**

```
================================================================================
PARSING METHOD: LLM (AI-Powered)
================================================================================
Parsed Data:
{
  "entity": "invoice",
  "operations": ["create"],
  "fields": [...],
  "validations": [...],
  "endpoint": "/PDFViewer",
  "method": "POST",
  "base_url": "http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction",
  "status_codes": {
    "success": [200],
    "error": [400, 500]
  },
  "business_rules": []
}
================================================================================
```

**✅ VERIFY:**
- `"base_url"`: Should be `"http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction"`
- `"endpoint"`: Should be `"/PDFViewer"`

---

### **Step 5: Check Generated Scenarios**

**In the browser, you should see:**
- A table with 10-15 test scenarios
- Each scenario should show:
  - **Endpoint:** `/PDFViewer`
  - **Method:** `POST`
  - **Status:** Various (200, 400, etc.)

---

### **Step 6: Download and Inspect CSV**

1. **Click:** "Download CSV" button
2. **Save as:** `test-scenarios.csv`
3. **Open the CSV file** in Excel, Notepad, or VS Code

**✅ VERIFY the CSV contains these columns:**

```csv
test_id,test_name,test_category,priority,method,base_url,endpoint,headers,body,expected_status,...
TC-001,Create invoice with valid data,Functional,P0,POST,http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction,/PDFViewer,Content-Type: application/json,...
```

**Key checks:**
- ✅ `base_url` column = `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
- ✅ `endpoint` column = `/PDFViewer`
- ✅ NOT `https://jsonplaceholder.typicode.com` (old default)

---

## 🔍 **Quick CSV Verification Commands**

### **Option 1: PowerShell (Windows)**

```powershell
# Navigate to Test_Data folder
cd Test_Data

# Check base_url values in CSV
Select-String -Path "generated-scenarios.csv" -Pattern "base_url" | Select-Object -First 3

# Check endpoint values in CSV
Select-String -Path "generated-scenarios.csv" -Pattern "endpoint" | Select-Object -First 3
```

### **Option 2: Python Script**

Create a quick verification script:

```python
import csv

# Read the generated CSV
with open('Test_Data/generated-scenarios.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    scenarios = list(reader)

# Check first scenario
first = scenarios[0]
print("=" * 80)
print("CSV VERIFICATION")
print("=" * 80)
print(f"Test ID: {first['test_id']}")
print(f"Test Name: {first['test_name']}")
print(f"Method: {first['method']}")
print(f"Base URL: {first['base_url']}")
print(f"Endpoint: {first['endpoint']}")
print("=" * 80)

# Verify values
expected_base_url = "http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction"
expected_endpoint = "/PDFViewer"

if first['base_url'] == expected_base_url:
    print("✅ Base URL is CORRECT!")
else:
    print(f"❌ Base URL is WRONG!")
    print(f"   Expected: {expected_base_url}")
    print(f"   Actual: {first['base_url']}")

if first['endpoint'] == expected_endpoint:
    print("✅ Endpoint is CORRECT!")
else:
    print(f"❌ Endpoint is WRONG!")
    print(f"   Expected: {expected_endpoint}")
    print(f"   Actual: {first['endpoint']}")

print("=" * 80)
print(f"Total scenarios generated: {len(scenarios)}")
```

**Save as:** `verify_csv.py`

**Run:**
```powershell
python verify_csv.py
```

---

## ✅ **Expected Results**

### **Correct Output:**
```
================================================================================
CSV VERIFICATION
================================================================================
Test ID: TC-001
Test Name: Create invoice with valid data
Method: POST
Base URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction
Endpoint: /PDFViewer
================================================================================
✅ Base URL is CORRECT!
✅ Endpoint is CORRECT!
================================================================================
Total scenarios generated: 15
```

### **Incorrect Output (Before Fix):**
```
❌ Base URL is WRONG!
   Expected: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction
   Actual: https://jsonplaceholder.typicode.com
```

---

## 🐛 **Troubleshooting**

### **Issue 1: Base URL still shows jsonplaceholder.typicode.com**

**Cause:** LLM didn't extract the base_url correctly

**Solution:**
1. Check the terminal output for "Parsed Data"
2. If `base_url` is empty in parsed data, the LLM parsing failed
3. Try restarting the application to reload the updated prompt
4. Verify `core/llm_service.py` has the updated prompt (lines 262-291)

---

### **Issue 2: Endpoint shows full path instead of /PDFViewer**

**Cause:** LLM split the URL incorrectly

**Solution:**
1. Check if the user story clearly labels "API URL:"
2. The LLM should recognize the pattern and split at the last segment
3. If it still fails, you can manually enter the values in the modal

---

### **Issue 3: Modal appears asking for base_url**

**Cause:** LLM returned empty base_url

**This is actually GOOD!** It means:
- The fix is working (no hardcoded default)
- You can manually enter the correct values
- Enter:
  - **Base URL:** `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
  - **Endpoint:** `/PDFViewer`
  - **API Key:** `0c4b24cf-0211-4dcb-8f2f-280ab556ca78`

---

## 📊 **Verification Checklist**

- [ ] Application started successfully
- [ ] Navigated to Scenario Generator
- [ ] LLM toggle is ON
- [ ] Pasted user story with API URL
- [ ] Clicked "Generate Scenarios"
- [ ] Terminal shows correct parsed base_url and endpoint
- [ ] Browser shows generated scenarios
- [ ] Downloaded CSV file
- [ ] Opened CSV and verified base_url column
- [ ] Verified endpoint column
- [ ] Both values match expected values
- [ ] No hardcoded jsonplaceholder.typicode.com

---

## 🎉 **Success Criteria**

**The fix is working if:**
1. ✅ CSV `base_url` = `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
2. ✅ CSV `endpoint` = `/PDFViewer`
3. ✅ All scenarios use the same base_url and endpoint
4. ✅ No scenarios use `jsonplaceholder.typicode.com`

---

**Ready to test? Let me know if you need help with any step!**

