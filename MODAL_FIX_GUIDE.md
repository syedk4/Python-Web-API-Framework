# Configuration Modal Fix - Scenario Generator

## 🐛 **Issue: Modal Not Showing for Missing Configuration**

### **Problem:**
After pasting a user story in the Scenario Generator, the application was **not prompting** for Base URL, Endpoint, and API Key when they were missing from the requirements text.

### **Root Cause:**
When **LLM was enabled**, the AI was generating **default values** for `base_url` and `endpoint` even when they weren't mentioned in the user story. This caused the JavaScript modal check to be bypassed.

**Example:**
- User story: "Create a user registration API with email and password"
- LLM would return: `base_url: "https://jsonplaceholder.typicode.com"` (auto-generated)
- Modal check: `if (!hasBaseUrl || !hasEndpoint)` → **FALSE** (values exist)
- Result: Modal never shows ❌

---

## ✅ **Solution Applied**

### **1. Updated LLM Parsing Prompt**

**File:** `core/llm_service.py`

**Changed the prompt to explicitly instruct the LLM:**
```
IMPORTANT: 
- Only fill "base_url" if explicitly mentioned in the requirements
- Only fill "endpoint" if explicitly mentioned in the requirements
- If base_url or endpoint are NOT mentioned, leave them as empty strings ""
- Do NOT make up or assume base_url or endpoint values
```

---

### **2. Updated Backend to Accept LLM Toggle**

**File:** `app.py` → `/api/parse-requirements` endpoint

**Added `use_llm` parameter:**
```python
use_llm = data.get('use_llm', True)
parsed = requirement_parser.parse(requirements_text, use_llm=use_llm)
```

---

### **3. Updated Frontend to Pass LLM State**

**File:** `templates/scenario_generator.html` → `generateScenarios()` function

**Added LLM toggle to API call:**
```javascript
const useLLM = document.getElementById('useLLM').checked;

fetch('/api/parse-requirements', {
    body: JSON.stringify({
        requirements: requirements,
        use_llm: useLLM
    })
})
```

---

## 🧪 **Testing the Fix**

### **Test 1: Modal Should Appear**

1. **Go to:** http://localhost:5000
2. **Toggle LLM:** ON
3. **Enter:**
   ```
   Create a user registration API with email and password.
   Email must be valid. Password must be 8+ characters.
   Returns 201 on success, 400 for errors.
   ```
4. **Click:** Generate Scenarios
5. **Expected:** ✅ Modal appears asking for Base URL and Endpoint

---

### **Test 2: Modal Should NOT Appear**

1. **Go to:** http://localhost:5000
2. **Toggle LLM:** ON
3. **Enter:**
   ```
   Create a POST endpoint at https://jsonplaceholder.typicode.com/posts
   that accepts title and body.
   Returns 201 on success.
   ```
4. **Click:** Generate Scenarios
5. **Expected:** ✅ No modal - proceeds directly to generation

---

## 🔧 **Files Modified**

| File | Change | Purpose |
|------|--------|---------|
| `core/llm_service.py` | Updated `_build_parsing_prompt()` | Instruct LLM to return empty strings |
| `app.py` | Updated `/api/parse-requirements` | Accept `use_llm` parameter |
| `templates/scenario_generator.html` | Updated `generateScenarios()` | Pass `use_llm` toggle state |

---

## ✅ **Summary**

**Problem:** Modal not showing when base_url/endpoint missing  
**Cause:** LLM auto-generating default values  
**Solution:** Instruct LLM to return empty strings + pass LLM toggle state  
**Status:** ✅ **FIXED**

**The configuration modal now correctly appears when Base URL or Endpoint are not explicitly mentioned in the requirements!** 🎉

