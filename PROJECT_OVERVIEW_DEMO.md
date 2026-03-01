# HTTPie-Python-Web - Project Overview & Demo Guide

**Version:** 1.0.0  
**Demo Date:** March 2, 2026  
**Prepared for:** Team Presentation

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture & How It Works](#2-architecture--how-it-works)
3. [HTTPie Dependency Clarification](#3-httpie-dependency-clarification)
4. [Test Data Formats](#4-test-data-formats)
5. [Key Features for Demo](#5-key-features-for-demo)
6. [Live Demo Preparation](#6-live-demo-preparation)

---

## 1. Project Overview

### 1.1 What is HTTPie-Python-Web?

**HTTPie-Python-Web** is a web-based API testing and automation framework built with Flask. It provides an intuitive, user-friendly interface for managing, executing, and analyzing API tests without requiring command-line expertise.

Think of it as a **Postman alternative** with built-in test automation, batch execution, and comprehensive reporting capabilities.

### 1.2 Main Purpose & Use Cases

**Primary Purpose:**
- Automate API testing workflows for REST APIs
- Execute batch API tests from CSV/JSON files
- Generate comprehensive HTML reports with test results
- Monitor API performance and reliability over time

**Key Use Cases:**
1. **Regression Testing** - Run automated test suites after API changes
2. **Load Testing** - Execute multiple API calls in batch
3. **Multi-Language Testing** - Test APIs with different language parameters (EN-US, FR-CA, ES-MX)
4. **PDF Generation Testing** - Specifically designed for APIs that return PDF files
5. **CI/CD Integration** - Can be integrated into automated deployment pipelines

### 1.3 Target Audience

**Primary Users:**
- QA Engineers and Testers
- Backend Developers
- DevOps Engineers
- API Integration Teams

**Skill Level:**
- No programming knowledge required for basic usage
- Technical users can leverage advanced features (custom test data formats, scripting)

**Current Implementation:**
- Built for testing Invoice Extraction APIs
- Easily adaptable for any REST API testing needs

---

## 2. Architecture & How It Works

### 2.1 Technology Stack

**Backend:**
- **Flask 3.0.0** - Python web framework
- **Flask-SocketIO 5.3.5** - Real-time WebSocket communication
- **Python Requests 2.31.0** - HTTP client library for API calls

**Frontend:**
- **Bootstrap 5** - Responsive UI framework
- **JavaScript** - Client-side interactivity
- **Socket.IO** - Real-time updates

**Data Processing:**
- **CSV/JSON Parsers** - Multi-format test data support
- **HTML Report Generator** - Beautiful test reports

### 2.2 Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Configure │  │Run Tests │  │ Results  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP / WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Application (app.py)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Routes & WebSocket Handlers              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ConfigManager │  │ DataParser   │  │TestExecutor  │
│              │  │              │  │              │
│ - Load/Save  │  │ - Parse CSV  │  │ - Execute    │
│   config.env │  │ - Parse JSON │  │   HTTP calls │
│              │  │ - Validate   │  │ - Track      │
│              │  │   data       │  │   results    │
└──────────────┘  └──────────────┘  └──────┬───────┘
                                            │
                                            ▼
                                    ┌──────────────┐
                                    │   External   │
                                    │   REST API   │
                                    └──────────────┘
                                            │
                                            ▼
                                    ┌──────────────┐
                                    │ReportGen     │
                                    │              │
                                    │ - Generate   │
                                    │   HTML       │
                                    │ - Save PDFs  │
                                    └──────────────┘
```

### 2.3 Complete Workflow

**Step-by-Step Process:**

1. **Configuration Setup**
   - User configures API settings via web interface
   - Settings saved to `config.env` file
   - Includes: API URL, endpoint, method, API key, timeout

2. **Test Data Preparation**
   - User uploads or selects test data file (CSV/JSON)
   - DataParser reads and validates the file
   - Supports multiple formats (legacy and dynamic)

3. **Test Execution**
   - User clicks "Start Tests" on web interface
   - WebSocket connection established for real-time updates
   - TestExecutor processes each test case:
     - Builds HTTP request (URL, headers, body)
     - Executes API call using Python `requests` library
     - Captures response (status, time, size, body)
     - Compares actual vs expected results
     - Saves PDF files if applicable

4. **Real-Time Progress**
   - Progress updates sent via WebSocket
   - UI displays: current test, pass/fail count, progress bar
   - Live log of test execution

5. **Report Generation**
   - ReportGenerator creates HTML report
   - Includes: summary statistics, detailed results table
   - Saves to `test-results/YYYY-MM-DD/` directory
   - User can view/download report

### 2.4 Core Modules Explained

#### ConfigManager (`core/config_manager.py`)
**Role:** Manages application configuration
- Loads settings from `config.env` file
- Saves user-configured settings
- Provides default values if config missing
- **Key Settings:** API_BASE_URL, API_ENDPOINT, METHOD, API_KEY, TIMEOUT

#### DataParser (`core/data_parser.py`)
**Role:** Parses and validates test data files
- Supports CSV and JSON formats
- Handles multiple CSV formats (legacy vs dynamic)
- Replaces template variables ({{environment}}, {{languageCheck}})
- Validates data structure
- **Output:** List of test case dictionaries

#### TestExecutor (`core/test_executor.py`)
**Role:** Executes API tests and tracks results
- Builds HTTP requests from test data
- Executes requests using Python `requests` library
- Supports all HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Tracks pass/fail status
- Saves PDF responses
- Provides progress callbacks for real-time updates
- **Output:** List of TestResult objects

#### ReportGenerator (`core/report_generator.py`)
**Role:** Creates HTML test reports
- Generates beautiful, responsive HTML reports
- Includes summary statistics (total, passed, failed, pass rate)
- Detailed results table with all test data
- Saves reports with timestamps
- **Output:** HTML file and file path

---

## 3. HTTPie Dependency Clarification

### 3.1 Does This Use HTTPie CLI?

**No.** Despite the name "HTTPie-Python-Web", this application **does NOT use the HTTPie CLI tool** or HTTPie service.

### 3.2 What Does It Actually Use?

The application uses **Python's `requests` library** directly for making HTTP calls.

**Evidence from `requirements.txt`:**
```
requests==2.31.0  ← This is what we use for HTTP calls
```

**Evidence from `core/test_executor.py`:**
```python
import requests  # Line 6

# Line 123-131: Direct use of requests library
response = requests.request(
    method,
    url,
    headers=headers,
    data=request_body,
    timeout=timeout,
    verify=False
)
```

### 3.3 Why the Name "HTTPie-Python-Web"?

The naming is **inspired by HTTPie's philosophy** of making HTTP requests simple and user-friendly:

**HTTPie CLI Philosophy:**
- Simple, intuitive command-line HTTP client
- Human-friendly syntax
- Beautiful output formatting

**HTTPie-Python-Web Philosophy:**
- Simple, intuitive **web-based** HTTP testing
- User-friendly interface (no command line needed)
- Beautiful HTML reports

**In Summary:**
- ❌ Does NOT depend on HTTPie CLI
- ✅ Uses Python `requests` library
- ✅ Inspired by HTTPie's user-friendly approach
- ✅ Provides web interface instead of command line

---

## 4. Test Data Formats

### 4.1 Supported Formats Overview

The application supports **two main file formats** with **multiple variations**:

1. **CSV Format**
   - Legacy CSV (simple format)
   - Dynamic CSV (full-featured format)

2. **JSON Format**
   - Legacy JSON
   - Dynamic JSON

### 4.2 CSV Format - Legacy (Simple)

**When to Use:**
- Quick testing with minimal configuration
- All tests use the same API endpoint
- Testing invoice extraction or similar APIs
- Don't need to specify HTTP method or headers per test

**Structure:**
```csv
testDescription,customerNumber,invoiceNumber,orderNumber,shipTo
```

**Required Fields:**
- `testDescription` - Name/description of the test
- `customerNumber` - Customer identifier
- `invoiceNumber` - Invoice number
- `orderNumber` - Order number
- `shipTo` - Shipping location

**Sample Data:**
```csv
testDescription,customerNumber,invoiceNumber,orderNumber,shipTo
Standard numeric customer,9946600,40756307,C746966,D63
High-volume customer,8888000,40761163,D477664,262
Invalid Test Data,9999999,9999999,ABCD001,12344
```

**How It Works:**
- Parser automatically wraps data in API-compatible format
- Uses configured API_BASE_URL and API_ENDPOINT from config.env
- Uses configured METHOD (default: POST)
- Automatically adds environment='AFI' and languageCheck='EN-US'
- Expected status code: 200

**Generated Request Body:**
```json
[
  {
    "environment": "AFI",
    "customerNumber": "9946600",
    "shipTo": "D63",
    "invoiceNumber": "40756307",
    "orderNumber": "C746966",
    "languageCheck": "EN-US"
  }
]
```

### 4.3 CSV Format - Dynamic (Full-Featured)

**When to Use:**
- Need full control over each test
- Different tests use different endpoints or methods
- Need custom headers per test
- Testing multiple APIs in one file

**Structure:**
```csv
test_id,test_category,test_name,priority,method,base_url,endpoint,headers,body,expected_status
```

**Required Fields:**
- `test_name` - Name of the test
- `method` - HTTP method (GET, POST, PUT, DELETE, PATCH)
- `base_url` - Full base URL of the API
- `endpoint` - API endpoint path
- `body` - Request body (JSON string)
- `expected_status` - Expected HTTP status code (e.g., 200)

**Optional Fields:**
- `test_id`, `test_category`, `priority`, `headers`, `expected_response`, etc.

**Sample Data:**
```csv
test_name,method,base_url,endpoint,headers,body,expected_status
Test User Login,POST,http://api.example.com,/auth/login,"Content-Type: application/json","[{""username"":""test""}]",200
Get User Profile,GET,http://api.example.com,/users/123,"Content-Type: application/json","",200
```

**Template Variables:**
The body can include template variables that are replaced at runtime:
- `{{environment}}` → Replaced with 'AFI'
- `{{languageCheck}}` → Replaced with selected language (EN-US, FR-CA, ES-MX)

### 4.4 JSON Format - Legacy

**Structure:**
```json
[
  {
    "testDescription": "Test name",
    "customerNumber": "9946600",
    "invoiceNumber": "40756307",
    "orderNumber": "C746966",
    "shipTo": "D63"
  }
]
```

### 4.5 JSON Format - Dynamic (Full-Featured)

**Structure:**
```json
[
  {
    "test_name": "Create User",
    "method": "POST",
    "base_url": "http://api.example.com",
    "endpoint": "/users",
    "headers": "Content-Type: application/json",
    "body": {"username": "testuser"},
    "expected_status": "201"
  }
]
```

### 4.6 HTTP Methods Support

**All HTTP methods are supported:**
- ✅ GET, POST, PUT, DELETE, PATCH

**How Method Selection Works:**
1. **Dynamic Format:** Specify `method` field in each test case
2. **Legacy Format:** Uses configured default METHOD from config.env
3. **Method Override:** Test data method always overrides configured default

**Request Body Handling:**
- **POST, PUT, PATCH:** Body is sent in request
- **GET, DELETE:** Body is ignored (per HTTP standards)

### 4.7 Format Detection

The application **automatically detects** which format you're using based on field names. You don't need to specify the format!

### 4.8 Quick Reference Table

| Feature | Legacy CSV | Dynamic CSV | Legacy JSON | Dynamic JSON |
|---------|-----------|-------------|-------------|--------------|
| **Complexity** | Simple | Advanced | Simple | Advanced |
| **HTTP Method** | From config | Per test | From config | Per test |
| **Custom Headers** | ❌ | ✅ | ❌ | ✅ |
| **Custom URL** | ❌ | ✅ | ❌ | ✅ |
| **Template Variables** | ❌ | ✅ | ❌ | ✅ |
| **Best For** | Quick tests | Full control | Quick tests | Full control |

---

## 5. Key Features for Demo

### 5.1 Main Features to Highlight

#### 1. **Web-Based Configuration Management**
- No need to edit config files manually
- User-friendly form interface
- Real-time validation
- Persistent storage

#### 2. **Multi-Format Test Data Support**
- CSV and JSON formats
- Legacy and dynamic formats
- Automatic format detection
- Template variable replacement

#### 3. **Real-Time Test Execution**
- Live progress updates via WebSocket
- See tests running in real-time
- Current test name, pass/fail count
- Progress bar and percentage

#### 4. **Comprehensive HTML Reports**
- Beautiful, responsive design
- Summary statistics (pass rate, total, passed, failed)
- Detailed results table
- Downloadable reports
- Timestamped for tracking

#### 5. **Multi-Language Support**
- Test APIs in different languages
- EN-US (English)
- FR-CA (French Canadian)
- ES-MX (Spanish Mexican)

#### 6. **PDF File Handling**
- Automatically saves PDF responses
- Organized by date and test run
- Easy access to generated PDFs

#### 7. **Flexible HTTP Method Support**
- Configurable default method
- Per-test method override
- Supports GET, POST, PUT, DELETE, PATCH

#### 8. **Error Handling & Debugging**
- Detailed error messages
- Response preview for failed tests
- Timeout handling
- Connection error handling

### 5.2 Step-by-Step Demo Flow

**Recommended Demo Sequence:**

#### **Part 1: Dashboard Overview (2 minutes)**
1. Open application at http://localhost:5000
2. Show dashboard features:
   - Available test files count
   - Configuration status
   - Recent test runs
   - Quick navigation

**What to Say:**
> "This is the main dashboard. It gives us an overview of our testing environment. We can see we have X test files ready to run, our API is configured, and here are our recent test runs."

#### **Part 2: Configuration Setup (3 minutes)**
1. Navigate to Configure page
2. Show configuration form:
   - API Base URL
   - API Endpoint
   - HTTP Method dropdown (highlight this new feature!)
   - API Key (show it's password-protected)
   - Timeout settings
3. Explain each field
4. Click "Save Configuration"
5. Show success message

**What to Say:**
> "Configuration is simple. We enter our API details here. Notice the HTTP Method dropdown - this is a new feature that lets us set the default method for all tests. The API key is masked for security. Once we save, these settings are used for all test runs."

#### **Part 3: Test Data Files (2 minutes)**
1. Navigate to Test Runner page
2. Show test file dropdown
3. Explain different test files:
   - `test-data.csv` - Legacy format (8 tests)
   - `InvoiceExtraction-TestCases.csv` - Dynamic format (8 tests)
4. Show language selector

**What to Say:**
> "We support multiple test data formats. The legacy format is simple - just customer and invoice data. The dynamic format gives us full control - we can specify different HTTP methods, endpoints, and headers for each test."

#### **Part 4: Live Test Execution (5 minutes)**
1. Select a test file (use `test-data.csv` for simplicity)
2. Select language (EN-US)
3. Click "Start Tests"
4. **Highlight real-time features:**
   - Progress bar moving
   - Current test name updating
   - Pass/fail counters incrementing
   - Live log showing each test
5. Wait for completion
6. Show summary:
   - Pass rate percentage
   - Total/Passed/Failed counts
7. Click "View Report"

**What to Say:**
> "Watch this - as soon as I click Start Tests, we get real-time updates. See the progress bar? The current test name? The pass/fail counters? This is all happening live via WebSocket. No page refresh needed. And here's our summary - 87.5% pass rate, 7 out of 8 tests passed."

#### **Part 5: Test Report (3 minutes)**
1. Show HTML report in new tab
2. Highlight report features:
   - Summary statistics at top
   - Color-coded pass/fail status
   - Detailed results table
   - Response times
   - Status codes (actual vs expected)
   - Timestamps
   - Error details for failed tests
3. Scroll through the report
4. Show it's downloadable/shareable

**What to Say:**
> "Here's our comprehensive test report. At the top, we have our summary. Below, every test is listed with full details - response time, file size, status codes. Notice the failed test shows error details. This report is saved automatically and can be shared with the team."

#### **Part 6: Results History (2 minutes)**
1. Navigate to Results page
2. Show list of past test runs
3. Show date/time organization
4. Click on a previous report
5. Show it opens the saved HTML report

**What to Say:**
> "All test runs are saved and organized by date. We can go back and review any previous test run. This is great for tracking API stability over time and comparing results."

#### **Part 7: Advanced Features (3 minutes)**
1. Go back to Test Runner
2. Select `InvoiceExtraction-TestCases.csv` (dynamic format)
3. Show how it has different structure
4. Run tests to show it works the same way
5. Highlight template variable replacement

**What to Say:**
> "Now let me show you the advanced format. This CSV has full control - each test can specify its own HTTP method, endpoint, and headers. Notice the template variables in the body - these are automatically replaced with actual values at runtime."

### 5.3 Page-by-Page Description

#### **Dashboard Page**
- **Purpose:** Overview and quick access
- **Key Elements:**
  - Test files summary card
  - Configuration status card
  - Recent test runs table
  - Navigation buttons
- **User Actions:** Navigate to other pages

#### **Configure Page**
- **Purpose:** Set up API connection details
- **Key Elements:**
  - API Base URL input
  - API Endpoint input
  - HTTP Method dropdown (GET, POST, PUT, DELETE, PATCH)
  - API Key input (password field)
  - Correlation ID input
  - Timeout settings
  - Max Response Time setting
  - Save button
- **User Actions:** Enter/update configuration, save settings

#### **Run Tests Page**
- **Purpose:** Execute test suites
- **Key Elements:**
  - **Left Panel:**
    - Test file selector dropdown
    - Language selector
    - Start/Stop buttons
    - Current configuration display
  - **Right Panel:**
    - Progress section (hidden until tests start)
    - Progress bar with percentage
    - Statistics cards (Total, Current, Passed, Failed)
    - Test log (live updates)
    - Results section (shown after completion)
    - Summary message
    - View Report button
- **User Actions:** Select file, select language, start tests, view report

#### **Results Page**
- **Purpose:** Browse historical test runs
- **Key Elements:**
  - List of all test runs
  - Date/time stamps
  - Test file names
  - View Report buttons
  - Search/filter functionality
- **User Actions:** Browse history, open previous reports

---

## 6. Live Demo Preparation

### 6.1 Pre-Demo Checklist

**24 Hours Before Demo:**
- [ ] Verify API endpoint is accessible
- [ ] Test API key is valid
- [ ] Run a test execution to ensure everything works
- [ ] Clear old test results (optional, for clean demo)
- [ ] Prepare test data files
- [ ] Review this documentation

**1 Hour Before Demo:**
- [ ] Start the Flask application: `python app.py`
- [ ] Verify application is running at http://localhost:5000
- [ ] Open application in browser
- [ ] Configure API settings
- [ ] Run one quick test to verify everything works
- [ ] Keep browser tab open and ready

**5 Minutes Before Demo:**
- [ ] Close unnecessary browser tabs
- [ ] Zoom browser to comfortable viewing size (Ctrl + +)
- [ ] Have this documentation open in another window
- [ ] Test screen sharing if presenting remotely

### 6.2 Configuration Setup

**Before the demo, configure these settings:**

```
API Base URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction
API Endpoint: /PDFViewer
HTTP Method: POST
API Key: 0b4b24cf-0211-4deb-8f2f-280ab556ca78
Correlation ID: test
Timeout: 30
Max Response Time: 5000
```

**How to Configure:**
1. Navigate to Configure page
2. Enter the values above
3. Click "Save Configuration"
4. Verify success message appears

### 6.3 Sample Test Scenarios

**Scenario 1: Simple Legacy Format Test**
- **File:** `test-data.csv`
- **Tests:** 8 tests
- **Expected Result:** 7 pass, 1 fail (87.5% pass rate)
- **Duration:** ~30 seconds
- **Purpose:** Show basic functionality and real-time updates

**Scenario 2: Advanced Dynamic Format Test**
- **File:** `InvoiceExtraction-TestCases.csv`
- **Tests:** 8 tests
- **Expected Result:** 7 pass, 1 fail (87.5% pass rate)
- **Duration:** ~30 seconds
- **Purpose:** Show template variable replacement and dynamic format

**Scenario 3: Multi-Language Test**
- **File:** `test-data.csv`
- **Language:** FR-CA (French Canadian)
- **Tests:** 8 tests
- **Expected Result:** 7 pass, 1 fail
- **Duration:** ~30 seconds
- **Purpose:** Show multi-language support

### 6.4 Expected Outcomes

**For test-data.csv:**
```
Total Tests: 8
Passed: 7
Failed: 1
Pass Rate: 87.5%

Failed Test: "Invalid Test Data"
Reason: HTTP 500 - Invalid customer/invoice data
```

**Test Execution Timeline:**
- Test 1-7: Should pass (green checkmarks in log)
- Test 8: Should fail (red X in log)
- Total time: ~30 seconds

**Report Contents:**
- Summary section with 87.5% pass rate
- 8 rows in results table
- 7 rows with green "PASS" status
- 1 row with red "FAIL" status
- Error details for failed test

### 6.5 Demo Script

**Opening (30 seconds):**
> "Today I'm going to show you HTTPie-Python-Web, a web-based API testing framework we've built. It allows us to automate API testing without writing code, execute batch tests, and generate comprehensive reports. Let me walk you through it."

**Dashboard (1 minute):**
> "This is our dashboard. We can see we have 6 test files ready to use, our API is configured and ready, and here are our recent test runs. Everything is accessible from this clean interface."

**Configuration (2 minutes):**
> "Let's look at configuration. Here we set up our API connection - the base URL, endpoint, and importantly, we can now select the default HTTP method. This is a new feature that gives us flexibility. The API key is masked for security. Once saved, these settings apply to all tests."

**Test Execution (5 minutes):**
> "Now the exciting part - running tests. I'll select our test data file - this one has 8 test cases. I'll choose English as the language. Watch what happens when I click Start Tests..."

> [Click Start Tests]

> "See the real-time updates? The progress bar is moving, we can see which test is currently running, and the pass/fail counters are updating live. This is all happening via WebSocket - no page refresh needed."

> [Wait for completion]

> "And we're done! 87.5% pass rate - 7 out of 8 tests passed. The one failure is expected - it's testing invalid data. Now let's look at the report."

**Report Review (3 minutes):**
> "Here's our comprehensive HTML report. At the top, we have our summary statistics. Below, every single test is documented - the test name, pass/fail status, response time, file size, status codes. Notice the failed test shows detailed error information. This report is automatically saved and can be shared with the team or attached to tickets."

**Advanced Features (2 minutes):**
> "Let me quickly show you the advanced format. This test file uses our dynamic format where each test can specify its own HTTP method, endpoint, and headers. It also uses template variables that are automatically replaced at runtime. Watch - it works exactly the same way."

> [Run InvoiceExtraction-TestCases.csv]

**Closing (1 minute):**
> "So in summary, HTTPie-Python-Web gives us: easy configuration, multiple test data formats, real-time execution monitoring, comprehensive reports, and multi-language support. It's perfect for regression testing, API validation, and continuous integration. Questions?"

### 6.6 Potential Questions & Answers

**Q: Can we test APIs other than invoice extraction?**
> A: Absolutely! While it's currently configured for invoice extraction, you can test any REST API. Just update the configuration with your API details and create test data files with your endpoints.

**Q: How do we create test data files?**
> A: You can create CSV or JSON files. For simple tests, use the legacy format with just the data fields. For advanced tests, use the dynamic format where you specify the full HTTP request details. The application auto-detects which format you're using.

**Q: Can we integrate this into our CI/CD pipeline?**
> A: Yes! The application can be run headlessly, and test results are saved as HTML files. You can trigger tests via API calls and parse the results programmatically.

**Q: What happens if the API is down?**
> A: The application handles timeouts gracefully. Failed tests are marked as failed, error details are captured, and the test suite continues running. You'll see timeout errors in the report.

**Q: Can we test different HTTP methods?**
> A: Yes! You can set a default method in the configuration (GET, POST, PUT, DELETE, PATCH), and override it per test in the dynamic format.

**Q: How are API keys secured?**
> A: API keys are stored in config.env which is excluded from version control via .gitignore. In the UI, the API key field is a password field. For production, you'd want to use environment variables or a secrets manager.

**Q: Can we run tests in parallel?**
> A: Currently, tests run sequentially to avoid overwhelming the API. Parallel execution could be added as a future enhancement.

**Q: How long are test results kept?**
> A: Test results are saved indefinitely in the test-results folder, organized by date. You can manually clean up old results or implement automatic cleanup.

### 6.7 Troubleshooting During Demo

**If application won't start:**
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart application
python app.py
```

**If tests fail unexpectedly:**
- Check API endpoint is accessible
- Verify API key is correct
- Check network connection
- Look at error details in the log

**If WebSocket doesn't connect:**
- Refresh the browser page
- Check browser console for errors
- Restart the Flask application

**If report doesn't generate:**
- Check test-results folder exists
- Verify write permissions
- Check browser console for errors

### 6.8 Post-Demo Follow-Up

**Materials to Share:**
- [ ] Link to GitHub repository
- [ ] This documentation file
- [ ] Sample test data files
- [ ] Installation guide (README.md)
- [ ] Configuration template (config.env.example)

**Next Steps to Discuss:**
- Deployment to shared server
- Integration with CI/CD pipeline
- Additional test data creation
- Training sessions for team members
- Feature requests and enhancements

---

## 📊 Quick Reference

### Application URLs
- **Dashboard:** http://localhost:5000/
- **Configure:** http://localhost:5000/configure
- **Run Tests:** http://localhost:5000/test-runner
- **Results:** http://localhost:5000/results

### Key Commands
```powershell
# Start application
python app.py

# Stop application
Ctrl + C

# Check if running
netstat -ano | findstr :5000
```

### Test Files Location
```
Test_Data/
├── test-data.csv                      # Legacy format (8 tests)
├── InvoiceExtraction-TestCases.csv    # Dynamic format (8 tests)
├── TestCasesDocID.csv                 # Alternative test set
├── TestFailData.csv                   # Failure scenarios
├── 5min_batch_invoices.json           # JSON format (224 tests)
└── max_batch_invoice.json             # Large batch test
```

### Report Location
```
test-results/
└── YYYY-MM-DD/
    └── Test_Report_YYYY-MM-DD_HH-MM-SS.html
```

---

## 🎯 Demo Success Criteria

✅ **Successful Demo Includes:**
- [ ] Clear explanation of what the application does
- [ ] Live demonstration of test execution
- [ ] Real-time updates visible
- [ ] Report generation shown
- [ ] At least one advanced feature highlighted
- [ ] Questions answered confidently
- [ ] Team understands value proposition

✅ **Key Messages to Convey:**
- Easy to use - no coding required
- Real-time feedback during test execution
- Comprehensive reporting
- Flexible test data formats
- Ready for team adoption

---

**Good luck with your demo! 🚀**

*For questions or issues, refer to the README.md or contact the development team.*

