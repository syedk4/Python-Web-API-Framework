# Troubleshooting Test Failures

## 🐛 **Common Issue: "Failed to resolve 'api.example.com'"**

### **Problem:**
All tests fail with error: `Failed to resolve 'api.example.com' (Errno 11001) getaddrinfo failed`

### **Root Cause:**
The test scenarios are using `https://api.example.com` as the base URL, which is **not a real API endpoint**. This is a placeholder domain that doesn't exist.

---

## ✅ **Solution 1: Use Sample CSV Files with Real API**

### **Quick Fix (Recommended):**

1. **Navigate to Test Runner:** http://localhost:5000/test-runner

2. **Select one of these files:**
   - ✅ `LLM_Generated_Posts_API_Tests.csv` (15 tests)
   - ✅ `LLM_Generated_User_Registration_Tests.csv` (19 tests)

3. **Run tests** - These files use `https://jsonplaceholder.typicode.com` (a real, working API)

4. **Expected Result:**
   - ✅ Tests will execute successfully
   - ✅ Most tests will PASS
   - ✅ You'll see actual API responses

---

## ✅ **Solution 2: Update Generated Scenarios**

If you generated scenarios through the UI and got `generated-scenarios.csv`:

### **Option A: Regenerate with Real API**

1. **Go to Scenario Generator:** http://localhost:5000

2. **Enter requirements with a real API:**
   ```
   Create a POST endpoint at https://jsonplaceholder.typicode.com/posts
   that accepts title and body fields.
   Returns 201 on success, 400 for validation errors.
   ```

3. **Generate scenarios** with LLM ON

4. **Download CSV** and test

### **Option B: Manually Edit the CSV**

Open `Test_Data/generated-scenarios.csv` and replace:

**Before:**
```csv
base_url
https://api.example.com
```

**After:**
```csv
base_url
https://jsonplaceholder.typicode.com
```

**Also update the endpoint** to match JSONPlaceholder API:
```csv
endpoint
/posts
```

---

## ✅ **Solution 3: Use Your Own API**

If you have a real API to test:

### **Update the CSV file:**

1. **Change `base_url`** to your API:
   ```csv
   https://your-api.com
   ```

2. **Change `endpoint`** to your endpoint:
   ```csv
   /api/v1/your-endpoint
   ```

3. **Add authentication** if needed:
   ```csv
   headers
   Content-Type: application/json, Authorization: Bearer YOUR_TOKEN
   ```

---

## 📊 **Understanding the Error**

### **Error Message Breakdown:**

```
Failed to resolve 'api.example.com' (Errno 11001) getaddrinfo failed
```

**What it means:**
- ❌ DNS lookup failed
- ❌ Domain doesn't exist
- ❌ Cannot establish connection
- ❌ Test cannot proceed

**Why it happens:**
- `api.example.com` is a **placeholder domain**
- It's used in documentation/examples
- It's **not a real API**

---

## 🎯 **Recommended Test APIs**

### **1. JSONPlaceholder (Best for Testing)**
- **URL:** `https://jsonplaceholder.typicode.com`
- **Endpoints:** `/posts`, `/users`, `/comments`, `/todos`
- **Methods:** GET, POST, PUT, PATCH, DELETE
- **Auth:** None required
- **Perfect for:** Testing your framework

### **2. ReqRes**
- **URL:** `https://reqres.in/api`
- **Endpoints:** `/users`, `/register`, `/login`
- **Methods:** GET, POST, PUT, DELETE
- **Auth:** None required
- **Perfect for:** User management tests

### **3. HTTPBin**
- **URL:** `https://httpbin.org`
- **Endpoints:** `/get`, `/post`, `/put`, `/delete`
- **Methods:** All HTTP methods
- **Auth:** Various auth methods supported
- **Perfect for:** HTTP testing

---

## 🔧 **Fix Applied**

I've updated the LLM service to use `https://jsonplaceholder.typicode.com` as the default base URL instead of `api.example.com`.

**Files Modified:**
- ✅ `core/llm_service.py` - Changed default base_url

**What this means:**
- ✅ Future scenario generation will use a working API by default
- ✅ Tests will execute successfully out of the box
- ✅ No more DNS resolution errors

---

## 📝 **Testing Checklist**

Before running tests, verify:

- [ ] **Base URL is valid** - Check the CSV file
- [ ] **Endpoint exists** - Verify the API endpoint
- [ ] **Authentication configured** - If API requires auth
- [ ] **Network connectivity** - Can reach the API
- [ ] **Firewall/Proxy** - Not blocking requests

---

## 🧪 **Quick Test**

To verify the fix works:

1. **Generate new scenarios:**
   ```
   Go to: http://localhost:5000
   Enter: "Create a post with title and body"
   Toggle: LLM ON
   Click: Generate Scenarios
   ```

2. **Check the base_url:**
   - Should be: `https://jsonplaceholder.typicode.com`
   - NOT: `https://api.example.com`

3. **Download and test:**
   - Download CSV
   - Go to Test Runner
   - Run tests
   - Should PASS ✅

---

## 📞 **Still Having Issues?**

### **Check these:**

1. **Internet connection:**
   ```bash
   ping jsonplaceholder.typicode.com
   ```

2. **API is accessible:**
   ```bash
   curl https://jsonplaceholder.typicode.com/posts/1
   ```

3. **Firewall/Proxy:**
   - Check if corporate firewall blocks external APIs
   - Configure proxy if needed

4. **CSV file format:**
   - Ensure base_url column has valid URL
   - No typos in domain name
   - Includes `https://` or `http://`

---

## ✅ **Summary**

**Problem:** Tests failing with DNS resolution error  
**Cause:** Using fake domain `api.example.com`  
**Solution:** Use real API like `jsonplaceholder.typicode.com`  
**Status:** ✅ Fixed in LLM service  

**Next Steps:**
1. Use sample CSV files provided
2. Or regenerate scenarios (will use real API now)
3. Or manually update existing CSV files

---

**Your tests should now work!** 🎉

