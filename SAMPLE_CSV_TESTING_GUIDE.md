# Sample CSV Testing Guide

## 📁 **Sample CSV Files Created**

I've created two sample CSV files with LLM-generated test scenarios that you can use immediately:

### **1. User Registration API Tests**
**File:** `Test_Data/LLM_Generated_User_Registration_Tests.csv`

**API Endpoint:** `https://jsonplaceholder.typicode.com/users`

**Test Coverage:**
- ✅ **19 comprehensive test scenarios**
- ✅ Functional tests (valid user creation)
- ✅ Validation tests (email format, password complexity, username length)
- ✅ Business logic tests (duplicate username)
- ✅ Edge cases (empty body, null values, boundary conditions)
- ✅ Security tests (SQL injection, XSS attacks)

**Categories:**
- Functional: 3 scenarios
- Validation: 10 scenarios
- Business Logic: 1 scenario
- Edge Case: 3 scenarios
- Security: 2 scenarios

---

### **2. Posts API Tests**
**File:** `Test_Data/LLM_Generated_Posts_API_Tests.csv`

**API Endpoint:** `https://jsonplaceholder.typicode.com/posts`

**Test Coverage:**
- ✅ **15 comprehensive test scenarios**
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ GET, POST, PUT, PATCH, DELETE methods
- ✅ Validation tests (missing fields, invalid IDs)
- ✅ Edge cases (long titles, special characters)
- ✅ Security tests (HTML injection, XSS)

**Categories:**
- Functional: 6 scenarios
- Validation: 4 scenarios
- Edge Case: 2 scenarios
- Security: 2 scenarios
- Business Logic: 1 scenario

---

## 🧪 **How to Test These CSV Files**

### **Step 1: Start the Application**
```bash
py app.py
```

### **Step 2: Navigate to Test Runner**
Open your browser to: **http://localhost:5000/test-runner**

### **Step 3: Select Test File**
Choose one of the sample CSV files:
- `LLM_Generated_User_Registration_Tests.csv`
- `LLM_Generated_Posts_API_Tests.csv`

### **Step 4: Run Tests**
Click **"Start Tests"** button

### **Step 5: View Results**
- Watch real-time progress
- See pass/fail counts
- Download HTML report when complete

---

## 📊 **Expected Results**

### **For Posts API Tests (Recommended to try first):**

**JSONPlaceholder is a real, working API**, so you'll get actual responses:

| Test | Expected Result | Why |
|------|----------------|-----|
| TC-001: Create post | ✅ **PASS** | API accepts POST requests |
| TC-002: Get post by ID | ✅ **PASS** | Post ID 1 exists |
| TC-003: Get all posts | ✅ **PASS** | Returns 100 posts |
| TC-004: Update post | ✅ **PASS** | PUT request succeeds |
| TC-005: Patch post | ✅ **PASS** | PATCH request succeeds |
| TC-006: Delete post | ✅ **PASS** | DELETE returns 200 |
| TC-007: Get invalid post | ⚠️ **MAY FAIL** | API returns 404 (expected) but test expects 404 |
| TC-008-010: Validation | ⚠️ **MAY FAIL** | JSONPlaceholder doesn't validate (it's a mock API) |

**Note:** JSONPlaceholder is a **fake REST API** for testing. It accepts all requests but doesn't actually validate data or persist changes. This is perfect for testing your framework!

---

### **For User Registration Tests:**

**Expected Results:**
- Most tests will **PASS** because JSONPlaceholder accepts all requests
- Validation tests (TC-002 to TC-010) may **PASS** even with invalid data (JSONPlaceholder doesn't validate)
- This demonstrates that your **test framework works correctly**
- In a real API, validation tests would fail as expected

---

## 🎯 **What You'll Learn**

### **1. Test Execution Works**
- ✅ CSV files are parsed correctly
- ✅ HTTP requests are built properly
- ✅ API calls are executed
- ✅ Responses are captured

### **2. Format Compatibility**
- ✅ LLM-generated scenarios work with TestExecutor
- ✅ All required fields are present
- ✅ JSON body is properly formatted

### **3. Real-Time Progress**
- ✅ WebSocket updates work
- ✅ Progress bar updates
- ✅ Test log shows execution

### **4. Report Generation**
- ✅ HTML report is created
- ✅ Summary statistics are accurate
- ✅ Detailed results table is populated

---

## 🔧 **Customizing for Your API**

To test your own API, modify the CSV files:

### **Change Base URL:**
Replace:
```csv
https://jsonplaceholder.typicode.com
```

With your API:
```csv
https://your-api.com
```

### **Change Endpoint:**
Replace:
```csv
/posts
```

With your endpoint:
```csv
/api/v1/your-endpoint
```

### **Add Authentication:**
Update headers column:
```csv
Content-Type: application/json, Authorization: Bearer YOUR_TOKEN
```

Or configure in `config.env`:
```env
API_KEY=your-api-key-here
```

---

## 📈 **Success Metrics**

After running the tests, you should see:

### **Posts API Tests:**
- **Total Tests:** 15
- **Expected Pass Rate:** 60-80% (some validation tests may pass incorrectly)
- **Execution Time:** ~5-10 seconds
- **Report Generated:** ✅ Yes

### **User Registration Tests:**
- **Total Tests:** 19
- **Expected Pass Rate:** 50-70%
- **Execution Time:** ~8-15 seconds
- **Report Generated:** ✅ Yes

---

## 🎉 **What This Proves**

1. ✅ **Phase 3 is working** - LLM generates comprehensive scenarios
2. ✅ **Format fix is successful** - Scenarios are compatible with TestExecutor
3. ✅ **Test execution works** - Framework can run tests end-to-end
4. ✅ **Reporting works** - Results are captured and displayed
5. ✅ **Real API integration** - Can test against live APIs

---

## 🚀 **Next Steps**

1. **Run the sample tests** to verify everything works
2. **Review the HTML report** to see detailed results
3. **Create your own CSV** with your API endpoints
4. **Generate scenarios via UI** with LLM ON
5. **Export and test** your generated scenarios

---

**Ready to test!** 🎯

Try the **Posts API tests first** - they'll give you the most realistic results since JSONPlaceholder is a fully functional mock API.

