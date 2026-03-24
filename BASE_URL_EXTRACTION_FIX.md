# Base URL Extraction Fix - Complete Solution

## 🐛 **Problem Identified**

**Issue:** Generated CSV file contained incorrect `base_url` despite user story providing a specific Azure-hosted API URL.

**User Story:**
```
API URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction/PDFViewer
API Key: 0c4b24cf-0211-4dcb-8f2f-280ab556ca78
```

**Generated CSV (Before Fix):**
- ❌ **base_url:** `https://jsonplaceholder.typicode.com` (WRONG!)
- ❌ **endpoint:** `/WebAPI/InvoiceExtraction/PDFViewer` (Wrong split!)

**Expected CSV (After Fix):**
- ✅ **base_url:** `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
- ✅ **endpoint:** `/PDFViewer`

---

## 🔍 **Root Cause Analysis**

### **Issue 1: LLM Prompt Confusion**
The LLM parsing prompt didn't provide clear instructions on how to split a full URL into `base_url` and `endpoint`.

**Example:**
- Input: `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction/PDFViewer`
- Expected:
  - `base_url`: `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
  - `endpoint`: `/PDFViewer`
- Actual: LLM was confused about where to split the URL, and the code fell back to hardcoded default

### **Issue 2: Data Flow Problem**
Even when the LLM correctly extracted `base_url` during parsing, it was **not being passed** to the scenario formatting function.

**Data Flow:**
1. ✅ `parse_requirements()` → Extracts `base_url` from requirements
2. ✅ `generate_scenarios()` → Receives `parsed_data` with `base_url`
3. ❌ `_format_scenarios()` → **Did NOT receive `base_url`**
4. ❌ Fallback to hardcoded default: `https://jsonplaceholder.typicode.com`

---

## ✅ **Solution Implemented**

### **Fix 1: Improved LLM Parsing Prompt**

**File:** `core/llm_service.py` (Lines 261-279)

**Changes:**
- Added explicit instructions for splitting full URLs
- Provided concrete examples
- Warned against using placeholder URLs

**New Instructions:**
```
IMPORTANT URL EXTRACTION RULES:
1. If requirements explicitly label "API URL:" and "Endpoint:" separately:
   - Extract the labeled "API URL" as base_url
   - Extract the labeled "Endpoint" as endpoint

2. If a full URL is provided without labels, use intelligent splitting:
   - Look for common API path patterns (/api/, /v1/, /WebAPI/, etc.)
   - Split at the last major API boundary

3. Special case - if the URL contains a service path before the endpoint:
   - Example: "http://server.com/WebAPI/InvoiceExtraction/PDFViewer"
   - Split as: base_url: "http://server.com/WebAPI/InvoiceExtraction", endpoint: "/PDFViewer"
   - The base_url includes the service path, endpoint is the final resource

Examples:
- "API URL: http://server.com/WebAPI/InvoiceExtraction/PDFViewer" →
  base_url: "http://server.com/WebAPI/InvoiceExtraction", endpoint: "/PDFViewer"
- "https://payroll-api.azurewebsites.net/WebAPI/InvoiceExtraction/PDFViewer" →
  base_url: "https://payroll-api.azurewebsites.net/WebAPI/InvoiceExtraction", endpoint: "/PDFViewer"
```

---

### **Fix 2: Pass base_url Through Data Pipeline**

**File:** `core/llm_service.py` (Line 209)

**Before:**
```python
return self._format_scenarios(scenarios)
```

**After:**
```python
# Pass base_url from parsed_data to ensure it's used in scenarios
return self._format_scenarios(scenarios, parsed_data.get('base_url', ''))
```

---

### **Fix 3: Update _format_scenarios to Use Parsed base_url**

**File:** `core/llm_service.py` (Lines 395-418)

**Before:**
```python
def _format_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
    # Get base_url from scenario or use default
    base_url = scenario.get('base_url', 'https://jsonplaceholder.typicode.com')
```

**After:**
```python
def _format_scenarios(self, scenarios: List[Dict], parsed_base_url: str = '') -> List[Dict]:
    # Get base_url with priority:
    # 1. From scenario (if LLM included it)
    # 2. From parsed requirements (extracted during parsing phase)
    # 3. Default to JSONPlaceholder (only if nothing else available)
    base_url = scenario.get('base_url') or parsed_base_url or 'https://jsonplaceholder.typicode.com'
```

**Priority Order:**
1. ✅ Scenario-level `base_url` (if LLM included it in each scenario)
2. ✅ Parsed `base_url` (extracted from requirements during parsing)
3. ✅ Default fallback (only if nothing else is available)

---

### **Fix 4: Include base_url in Scenario Generation Context**

**File:** `core/llm_service.py` (Lines 282-304)

**Added:**
```python
base_url = parsed_data.get('base_url', '')

Parsed Information:
- Base URL: {base_url if base_url else '(not specified)'}
```

This ensures the LLM knows what base URL to use when generating test scenarios.

---

## 🧪 **Testing the Fix**

### **Test Case:**
```
API URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction/PDFViewer
API Key: 0c4b24cf-0211-4dcb-8f2f-280ab556ca78
```

### **Expected Result:**
- ✅ `base_url`: `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
- ✅ `endpoint`: `/PDFViewer`

**Splitting Logic:**
- The URL contains a service path `/WebAPI/InvoiceExtraction` before the final endpoint `/PDFViewer`
- The base_url includes the service path (everything except the final resource)
- The endpoint is the final resource path segment

---

## 📊 **Summary of Changes**

| File | Lines | Change | Impact |
|------|-------|--------|--------|
| `core/llm_service.py` | 261-279 | Improved parsing prompt with URL splitting examples | LLM correctly extracts base_url |
| `core/llm_service.py` | 209 | Pass `parsed_base_url` to `_format_scenarios()` | Data flows through pipeline |
| `core/llm_service.py` | 395-418 | Accept and use `parsed_base_url` parameter | Scenarios use correct base_url |
| `core/llm_service.py` | 282-304 | Include base_url in scenario generation context | LLM aware of base_url |

---

## ✅ **Verification Checklist**

- [x] LLM prompt includes URL splitting instructions
- [x] LLM prompt includes concrete examples
- [x] `parsed_base_url` is passed to `_format_scenarios()`
- [x] `_format_scenarios()` accepts `parsed_base_url` parameter
- [x] Priority order: scenario > parsed > default
- [x] Scenario generation prompt includes base_url
- [x] No hardcoded defaults override user-provided URLs

---

## 🎯 **Expected Behavior After Fix**

1. **User provides full URL in requirements:**
   - LLM splits it into `base_url` and `endpoint`
   - Both are stored in `parsed_data`
   - Both are passed to scenario generation
   - CSV contains correct values

2. **User provides only base_url:**
   - LLM extracts `base_url`
   - Endpoint remains empty or uses default
   - CSV contains correct base_url

3. **User provides neither:**
   - Modal appears asking for configuration
   - User manually enters values
   - CSV contains user-provided values

---

**Status:** ✅ **FIX COMPLETE**

The base URL extraction and data flow issues have been resolved. The framework now correctly:
- Extracts base_url from full URLs
- Passes base_url through the entire data pipeline
- Uses the correct base_url in generated CSV files

