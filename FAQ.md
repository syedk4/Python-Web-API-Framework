# Frequently Asked Questions (FAQ)
## Python-API-Testing-Framework

**Last Updated:** March 2, 2026  
**Version:** 1.0.0

---

## 📚 Table of Contents

1. [General Questions](#general-questions)
2. [Getting Started](#getting-started)
3. [Test Data & Formats](#test-data--formats)
4. [Running Tests](#running-tests)
5. [Results & Reports](#results--reports)
6. [Technical Questions](#technical-questions)
7. [Comparison with Other Tools](#comparison-with-other-tools)
8. [Troubleshooting](#troubleshooting)
9. [Security & Privacy](#security--privacy)
10. [Advanced Usage](#advanced-usage)

---

## 🎯 General Questions

### **Q1: What is Python-API-Testing-Framework?**

**A:** Python-API-Testing-Framework is a web-based tool for automated, data-driven API testing. It allows QA teams to run batch API tests using simple CSV or JSON files, with real-time progress tracking and automatic HTML report generation.

**Key Features:**
- CSV-based test data (edit in Excel)
- Real-time progress tracking via WebSocket
- Automatic HTML report generation
- Web-based interface (no installation for end users)
- Self-hosted (data stays on your infrastructure)

---

### **Q2: Who should use this tool?**

**A:** This tool is designed for:
- **QA Engineers** - Running regression test suites
- **Business Analysts** - Creating test scenarios without coding
- **Developers** - Quick API validation during development
- **Team Leads** - Generating test reports for stakeholders

**Skill Level:** No programming knowledge required for basic usage (CSV editing in Excel)

---

### **Q3: What problem does this solve?**

**A:** 
- **Manual Testing is Slow:** Testing 500 API scenarios manually takes 16-25 hours
- **Automated Testing is Complex:** Tools like Postman require JSON knowledge and scripting
- **Non-Technical Barrier:** QA team can't easily create/edit tests without developer help
- **No Real-Time Feedback:** Can't see progress during long test runs
- **Report Generation:** Manual effort to compile test results

**Solution:** Run 500 tests in ~15 minutes using CSV files that anyone can edit in Excel, with real-time progress and automatic reports.

---

### **Q4: Does this use HTTPie CLI?**

**A:** **No!** Despite the original project name, this tool does NOT use HTTPie CLI.

**What it uses:**
- Python `requests` library (version 2.31.0)
- No HTTPie installation required
- No HTTPie dependencies

**Why the confusion?**
- Originally named "HTTPie-Python-Web" (inspired by HTTPie's user-friendly philosophy)
- Renamed to "Python-API-Testing-Framework" to avoid confusion
- Uses standard Python HTTP library, not HTTPie

---

### **Q5: How is this different from Postman?**

**A:** 

| Feature | Python-API-Testing-Framework | Postman |
|---------|------------------------------|---------|
| **Test Data** | CSV files (Excel-friendly) | JSON collections |
| **Batch Testing** | Built-in, one-click | Requires Collection Runner |
| **Real-Time Progress** | WebSocket updates | Limited feedback |
| **Reports** | Automatic HTML generation | Manual or Newman CLI |
| **Installation** | Web-based (no install) | Desktop app required |
| **Learning Curve** | 15-30 minutes | Several hours |
| **Best For** | Batch regression testing | API exploration |

**Use Both:** Postman for API exploration, this tool for automated batch testing.

---

### **Q6: How is this different from Bruno?**

**A:**

| Feature | Python-API-Testing-Framework | Bruno |
|---------|------------------------------|-------|
| **Interface** | Web-based | Desktop app |
| **Batch Testing** | Built for it | Limited support |
| **Test Data** | CSV/JSON files | .bru files |
| **Reports** | Automatic HTML | No built-in reporting |
| **Installation** | Server-side only | App installation required |
| **Best For** | Automated testing | Manual testing, Git-friendly |

---

## 🚀 Getting Started

### **Q7: How do I install this?**

**A:** 

**Prerequisites:**
- Python 3.12 or higher
- pip (Python package manager)

**Installation Steps:**
```powershell
# 1. Clone the repository
git clone https://github.com/syedk4/Python-API-Testing-Framework.git
cd Python-API-Testing-Framework

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
py app.py

# 4. Open browser
# Navigate to: http://localhost:5000
```

**Time Required:** 5-10 minutes

---

### **Q8: What are the system requirements?**

**A:**

**Minimum:**
- Python 3.12+
- 512MB RAM
- 100MB disk space
- Modern web browser (Chrome, Firefox, Edge, Safari)

**Recommended:**
- Python 3.12+
- 2GB RAM
- 1GB disk space (for test results)
- Chrome or Firefox browser
- Network access to API endpoints

**Operating Systems:**
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, CentOS 8+, etc.)

---

### **Q9: How do I create my first test?**

**A:**

**Step-by-Step:**

1. **Download Sample File**
   - Go to Configure page
   - Click "Download Sample" under CSV - Legacy Format
   - Save `test-data-sample.csv`

2. **Edit in Excel**
   - Open file in Excel
   - Edit the test data:
     ```csv
     testDescription,customerNumber,invoiceNumber,orderNumber,shipTo
     My First Test,1234567,40000001,C000001,A01
     ```

3. **Configure API Settings**
   - Go to Configure page
   - Enter API Base URL
   - Enter API Endpoint
   - Enter API Key
   - Click "Save Configuration"

4. **Upload Test File**
   - Go to Run Tests page
   - Click "Choose File" under "Upload Test Data File"
   - Select your edited CSV file
   - Click "Upload"

5. **Run Tests**
   - Select your file from dropdown
   - Select language
   - Click "Start Tests"
   - Watch real-time progress!

**Time Required:** 10-15 minutes for first test

---

### **Q10: Do I need programming knowledge?**

**A:**

**For Basic Usage:** No!
- Edit CSV files in Excel (like a spreadsheet)
- Upload files via web interface
- Click "Start Tests" button
- View HTML reports

**For Advanced Usage:** Helpful but not required
- Understanding JSON format
- Customizing test logic (Python knowledge)
- Deploying to production server

**Bottom Line:** QA team members with Excel skills can use this without any coding.

---

## 📊 Test Data & Formats

### **Q11: What test data formats are supported?**

**A:** Four formats are supported:

**1. CSV - Legacy Format** (Simplest)
```csv
testDescription,customerNumber,invoiceNumber,orderNumber,shipTo
Test 1,1234567,40000001,C000001,A01
Test 2,8888000,40000002,D000002,262
```
- **Use when:** All tests use the same API endpoint
- **Columns:** 5 fixed columns
- **Best for:** Quick testing, simple scenarios

**2. CSV - Dynamic Format** (Advanced)
```csv
test_id,method,base_url,endpoint,headers,body,expected_status
TC-001,POST,http://api.example.com,/users,"Content-Type: application/json","{""name"":""John""}",201
```
- **Use when:** Different endpoints, methods, or headers per test
- **Columns:** 20+ columns (full control)
- **Best for:** Complex test suites, multiple APIs

**3. JSON - Legacy Format**
```json
[
  {
    "testDescription": "Test 1",
    "customerNumber": "1234567",
    "invoiceNumber": "40000001"
  }
]
```
- **Use when:** Prefer JSON over CSV
- **Best for:** Developers comfortable with JSON

**4. JSON - Dynamic Format**
```json
[
  {
    "test_name": "Create User",
    "method": "POST",
    "endpoint": "/users",
    "body": {"name": "John"}
  }
]
```
- **Use when:** Complex request bodies, nested data
- **Best for:** Advanced API testing

---

### **Q12: How do I choose between CSV and JSON?**

**A:**

**Choose CSV when:**
- ✅ QA team prefers Excel
- ✅ Simple, tabular data
- ✅ Non-technical users creating tests
- ✅ Easy to review/edit in spreadsheet

**Choose JSON when:**
- ✅ Complex nested data structures
- ✅ Developers creating tests
- ✅ Need to version control test data
- ✅ Programmatic test generation

**Recommendation:** Start with CSV Legacy format, upgrade to CSV Dynamic or JSON as needed.

---

### **Q13: What are template variables?**

**A:** Template variables are placeholders that get replaced at runtime.

**Available Variables:**
- `{{environment}}` - Replaced with configured environment (e.g., "AFI")
- `{{languageCheck}}` - Replaced with selected language (e.g., "EN-US")

**Example:**
```json
{
  "environment": "{{environment}}",
  "language": "{{languageCheck}}",
  "customerNumber": "1234567"
}
```

**At Runtime (if environment=AFI, language=EN-US):**
```json
{
  "environment": "AFI",
  "language": "EN-US",
  "customerNumber": "1234567"
}
```

**Use Cases:**
- Multi-environment testing (DEV, QA, PROD)
- Multi-language testing (EN-US, FR-CA, ES-MX)
- Reusable test data across environments

**Configuration:** Set values on Configure page

---

### **Q14: How many tests can I include in one file?**

**A:**

**Tested Limits:**
- ✅ Up to 1,000 tests in one file
- ✅ File size up to 5MB

**Practical Recommendations:**
- **Small batches:** 10-50 tests (quick feedback, ~1-2 minutes)
- **Medium batches:** 100-500 tests (regression suites, ~5-15 minutes)
- **Large batches:** 500-1,000 tests (full regression, ~15-30 minutes)

**Performance:**
- ~1-2 seconds per test (depends on API response time)
- Sequential execution (one test at a time)

**Tip:** Split very large test suites into multiple files for better organization.

---

### **Q15: Can I reuse test data across different environments?**

**A:** Yes! Use template variables.

**Example:**
```csv
test_id,method,base_url,endpoint,body
TC-001,POST,http://{{environment}}.api.com,/users,"{""lang"":""{{languageCheck}}""}"
```

**Configure page settings:**
- Environment: `dev` or `qa` or `prod`
- Language: `EN-US` or `FR-CA`

**Result:** Same test file works across all environments!

---

## ▶️ Running Tests

### **Q16: How do I run tests?**

**A:**

**Quick Steps:**
1. Go to **Run Tests** page
2. Select test file from dropdown
3. Select language (EN-US, FR-CA, ES-MX)
4. Click **"Start Tests"** button
5. Watch real-time progress
6. Download report when complete

**During Execution:**
- Progress bar shows % complete
- Live log shows each test result
- Pass/fail counts update in real-time
- Can stop tests anytime with "Stop Tests" button

---

### **Q17: Can I stop tests mid-execution?**

**A:** Yes!

**How to Stop:**
- Click **"Stop Tests"** button during execution
- Tests will stop gracefully
- Partial results are saved
- Can review completed tests

**What Happens:**
- Currently running test completes
- Remaining tests are skipped
- Log shows "Tests stopped by user"
- Partial report may be available

**Use Cases:**
- Discovered error in test data
- API is down
- Need to make urgent changes
- Testing the stop functionality

---

### **Q18: What happens if a test fails?**

**A:**

**Behavior:**
- ❌ Test marked as FAILED
- ✅ Execution continues to next test (doesn't stop)
- 📝 Error details logged
- 📊 Failure counted in statistics

**Error Information Captured:**
- HTTP status code received
- Expected vs actual status
- Response body (if available)
- Error message
- Timestamp

**After Completion:**
- HTML report shows all failures
- Can filter/review failed tests
- Can re-run failed tests by creating new file with only failures

---

### **Q19: How long does it take to run tests?**

**A:**

**Calculation:**
- **Time per test:** 1-2 seconds (depends on API response time)
- **Total time:** Number of tests × time per test

**Examples:**
- 10 tests: ~10-20 seconds
- 50 tests: ~1-2 minutes
- 100 tests: ~2-4 minutes
- 500 tests: ~10-15 minutes
- 1,000 tests: ~20-30 minutes

**Factors Affecting Speed:**
- API response time
- Network latency
- Server performance
- Timeout settings

**Future Enhancement:** Parallel execution for faster runs

---

### **Q20: Can I run multiple test files at once?**

**A:**

**Currently:** No - one file at a time

**Workaround:**
- Combine test data into one file
- Run sequentially (one after another)

**Future Enhancement:** Multi-file selection and batch execution

---

### **Q21: Can I schedule tests to run automatically?**

**A:**

**Currently:** No built-in scheduling

**Workarounds:**

**Option 1: Windows Task Scheduler**
```powershell
# Create a script: run_tests.ps1
cd C:\path\to\project
py app.py
# Then trigger via API or WebSocket
```

**Option 2: Cron Job (Linux/Mac)**
```bash
# Add to crontab
0 2 * * * cd /path/to/project && python3 app.py
```

**Option 3: CI/CD Integration**
- Jenkins scheduled job
- GitHub Actions cron
- GitLab CI schedules

**Future Enhancement:** Built-in scheduler with cron-like syntax

---

## 📈 Results & Reports

### **Q22: What kind of reports are generated?**

**A:**

**HTML Reports Include:**
- **Summary Section:**
  - Total tests run
  - Passed/failed counts
  - Pass rate percentage
  - Execution time
  - Timestamp

- **Detailed Results:**
  - Each test name/description
  - HTTP method and endpoint
  - Expected vs actual status
  - Response time
  - Pass/fail indicator
  - Error details (for failures)

- **Visual Elements:**
  - Color-coded results (green=pass, red=fail)
  - Summary charts
  - Sortable tables
  - Professional formatting

**Report Location:** `test-results/` folder
**Naming:** `test_report_YYYYMMDD_HHMMSS.html`

---

### **Q23: Can I export results to Excel/CSV?**

**A:**

**Currently:** HTML reports only

**Workarounds:**
- Open HTML report in browser
- Copy table data
- Paste into Excel
- Or parse HTML file programmatically

**Future Enhancement:**
- CSV export option
- Excel export with formatting
- JSON export for programmatic access

---

### **Q24: How long are reports kept?**

**A:**

**Current Behavior:**
- Reports saved indefinitely
- Stored in `test-results/` folder
- No automatic cleanup

**Recommendations:**
- Archive old reports monthly
- Keep last 30 days on server
- Move older reports to network drive
- Implement retention policy (e.g., 90 days)

**Manual Cleanup:**
```powershell
# Delete reports older than 30 days (Windows)
Get-ChildItem test-results\*.html | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

**Future Enhancement:** Configurable auto-cleanup

---

### **Q25: Can I share reports with my team?**

**A:** Yes! Multiple ways:

**Option 1: Direct File Sharing**
- Navigate to `test-results/` folder
- Copy HTML file
- Email or share via network drive
- Recipients open in any browser

**Option 2: Web Server**
- Reports accessible via application
- Share URL: `http://your-server:5000/download/test_report_xxx.html`
- Requires server to be running

**Option 3: Screenshot/PDF**
- Open HTML report
- Print to PDF (Ctrl+P → Save as PDF)
- Share PDF file

**Best Practice:** Include report in test summary emails to stakeholders

---

### **Q26: Can I see test results in real-time?**

**A:** Yes! Real-time updates via WebSocket.

**What You See During Execution:**
- ✅ Progress bar (% complete)
- ✅ Current test name
- ✅ Test X of Y
- ✅ Pass/fail status immediately
- ✅ Running totals (passed/failed)
- ✅ Live test log (scrolling)
- ✅ Estimated time remaining

**Technology:** WebSocket connection provides instant updates

**Benefits:**
- No need to wait for completion
- Can spot issues immediately
- Can stop if errors detected
- Engaging to watch!

---

## 🔧 Technical Questions

### **Q27: What technology stack is used?**

**A:**

**Backend:**
- Python 3.12
- Flask 3.0.0 (web framework)
- Flask-SocketIO 5.3.5 (WebSocket support)
- Python Requests 2.31.0 (HTTP client)

**Frontend:**
- HTML5
- Bootstrap 5 (UI framework)
- JavaScript (ES6+)
- Socket.IO (WebSocket client)

**Data Storage:**
- File system (CSV/JSON files)
- JSON configuration file
- No database required

**Deployment:**
- Development: Flask built-in server
- Production: Gunicorn/uWSGI recommended

---

### **Q28: Can I customize the code?**

**A:** Yes! The code is open and modifiable.

**Key Files to Customize:**

**1. Test Execution Logic** (`core/test_executor.py`)
- Modify HTTP request handling
- Add custom validation rules
- Change timeout behavior
- Add retry logic

**2. Data Parsing** (`core/data_parser.py`)
- Support new file formats
- Add custom data transformations
- Implement data validation

**3. Report Generation** (`core/report_generator.py`)
- Customize report format
- Add charts/graphs
- Change styling
- Add custom metrics

**4. Web Interface** (`templates/*.html`)
- Modify UI layout
- Add new pages
- Change branding
- Add custom features

**Language:** Python (easy to learn and modify)

---

### **Q29: Can I integrate this with CI/CD?**

**A:** Yes! Multiple integration options:

**Option 1: API Integration**
```python
# Call via HTTP API
import requests
response = requests.post('http://localhost:5000/api/run-tests',
    json={'test_file': 'my-tests.csv', 'language': 'EN-US'})
```

**Option 2: WebSocket Integration**
```javascript
// Connect via WebSocket
const socket = io('http://localhost:5000');
socket.emit('start_tests', {test_file: 'my-tests.csv'});
```

**Option 3: Command Line** (Future Enhancement)
```bash
# Planned CLI mode
python run_tests.py --file my-tests.csv --language EN-US
```

**CI/CD Examples:**
- Jenkins: Scheduled job calling API
- GitHub Actions: Workflow triggering tests
- GitLab CI: Pipeline step running tests

---

### **Q30: Does this support parallel test execution?**

**A:**

**Currently:** No - sequential execution only (one test at a time)

**Why Sequential:**
- Simpler implementation
- Easier debugging
- Predictable resource usage
- Sufficient for most use cases

**Future Enhancement:** Parallel execution
- Configure number of parallel threads
- Faster execution for large test suites
- Example: 500 tests in 2 minutes instead of 15

**Workaround:** Run multiple instances with different test files

---

### **Q31: What HTTP methods are supported?**

**A:**

**Supported Methods:**
- GET
- POST
- PUT
- DELETE
- PATCH

**Configuration:**
- **Legacy CSV:** POST only (configured in settings)
- **Dynamic CSV/JSON:** Any method per test

**Example (Dynamic CSV):**
```csv
test_id,method,endpoint
TC-001,GET,/users/123
TC-002,POST,/users
TC-003,PUT,/users/123
TC-004,DELETE,/users/123
TC-005,PATCH,/users/123
```

**Future Enhancement:** Support for HEAD, OPTIONS, TRACE

---

### **Q32: How does authentication work?**

**A:**

**Current Support:**

**1. API Key (Header)**
```
API_KEY: your-api-key-here
```
- Configured on Configure page
- Added to all requests automatically

**2. Custom Headers**
```csv
headers
"Authorization: Bearer token123, Content-Type: application/json"
```
- Specify in dynamic CSV/JSON
- Per-test customization

**3. Basic Auth** (Manual)
```csv
headers
"Authorization: Basic base64encodedcredentials"
```

**Not Currently Supported:**
- OAuth 2.0 flows
- JWT token refresh
- Session-based auth

**Future Enhancement:** Built-in OAuth support

---

### **Q33: Can I test APIs with SSL/HTTPS?**

**A:** Yes!

**HTTPS Support:**
- ✅ Fully supported
- ✅ SSL certificate verification disabled by default (for testing)
- ✅ Can enable verification if needed

**Configuration:**
```python
# In core/test_executor.py
response = requests.request(
    method, url,
    verify=False  # Change to True to enable SSL verification
)
```

**Self-Signed Certificates:**
- Works with `verify=False`
- Can provide custom CA bundle if needed

**Best Practice:** Use HTTPS for production APIs

---

### **Q34: What's the maximum file size for uploads?**

**A:**

**Current Limits:**
- **File size:** No hard limit (Flask default: 16MB)
- **Practical limit:** 5MB recommended
- **Test count:** Up to 1,000 tests per file

**Recommendations:**
- Keep files under 5MB for best performance
- Split large test suites into multiple files
- Use CSV for better compression vs JSON

**To Increase Limit:**
```python
# In app.py
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

---

## 🆚 Comparison with Other Tools

### **Q35: Should I use this instead of Postman?**

**A:** Use both! They serve different purposes.

**Use Python-API-Testing-Framework for:**
- ✅ Automated regression testing
- ✅ Batch testing (100+ tests)
- ✅ Data-driven testing from CSV
- ✅ Non-technical QA team
- ✅ Automated reporting

**Use Postman for:**
- ✅ API exploration and discovery
- ✅ Manual testing and debugging
- ✅ API documentation
- ✅ Mock servers
- ✅ Complex pre-request scripts

**Ideal Workflow:**
1. Use Postman to explore and understand API
2. Create test scenarios in CSV
3. Run batch tests with Python-API-Testing-Framework
4. Generate reports for stakeholders

---

### **Q36: Should I use this instead of JMeter?**

**A:** Different use cases.

**Python-API-Testing-Framework:**
- **Purpose:** Functional testing
- **Focus:** Correctness of API responses
- **Strength:** Data-driven, easy to use
- **Weakness:** Not for load testing

**JMeter:**
- **Purpose:** Performance/load testing
- **Focus:** Throughput, response times, scalability
- **Strength:** Simulate thousands of concurrent users
- **Weakness:** Complex setup, steep learning curve

**Use Both:**
- This tool for functional regression tests
- JMeter for performance/load testing

---

### **Q37: Can this replace manual testing?**

**A:** Partially - it's complementary.

**Can Replace:**
- ✅ Repetitive regression tests
- ✅ Data validation tests
- ✅ Smoke tests
- ✅ Sanity tests

**Cannot Replace:**
- ❌ Exploratory testing
- ❌ Usability testing
- ❌ Edge case discovery
- ❌ Complex business logic validation

**Best Approach:**
- Automate repetitive tests with this tool
- Focus manual testing on new features and edge cases
- Use both for comprehensive coverage

---

## 🔍 Troubleshooting

### **Q38: Application won't start - what should I check?**

**A:**

**Common Issues:**

**1. Python Version**
```powershell
py --version  # Should be 3.12 or higher
```
**Fix:** Install Python 3.12+

**2. Missing Dependencies**
```powershell
pip install -r requirements.txt
```
**Fix:** Install all required packages

**3. Port Already in Use**
```
Error: Address already in use (port 5000)
```
**Fix:**
- Stop other application using port 5000
- Or change port in `app.py`: `socketio.run(app, port=5001)`

**4. Permission Issues**
```
Error: Permission denied
```
**Fix:** Run as administrator or check folder permissions

**5. Module Not Found**
```
ModuleNotFoundError: No module named 'flask'
```
**Fix:** Activate virtual environment or reinstall dependencies

---

### **Q39: Tests are failing but API works in Postman - why?**

**A:**

**Common Causes:**

**1. Headers Missing**
- Check if API requires specific headers
- Add to Configure page or test data
- Example: `Content-Type: application/json`

**2. Authentication**
- Verify API key is correct
- Check if token has expired
- Ensure headers are properly formatted

**3. Request Body Format**
- Check JSON formatting (quotes, commas)
- Verify data types (string vs number)
- Escape special characters in CSV

**4. Endpoint URL**
- Verify base URL is correct
- Check endpoint path (leading slash?)
- Ensure no extra spaces

**5. Timeout**
- API might be slow
- Increase timeout in Configure page
- Default is 30 seconds

**Debug Steps:**
1. Copy exact request from Postman
2. Create test with same parameters
3. Compare request details
4. Check error message in report

---

### **Q40: File upload fails - what's wrong?**

**A:**

**Common Issues:**

**1. Invalid File Type**
- Only .csv and .json allowed
- Check file extension
- Rename if needed

**2. File Format Errors**
- CSV: Check for proper comma separation
- JSON: Validate JSON syntax (use jsonlint.com)
- Check for special characters

**3. File Too Large**
- Keep under 5MB
- Split into smaller files if needed

**4. File Name Issues**
- Avoid special characters in filename
- Use alphanumeric and hyphens/underscores only
- Example: `my-test-data.csv` ✅
- Example: `my test data (v2).csv` ❌

**5. Browser Issues**
- Try different browser
- Clear browser cache
- Disable browser extensions

---

### **Q41: Real-time updates not working - what to do?**

**A:**

**Troubleshooting Steps:**

**1. Check Browser Console**
- Press F12 to open developer tools
- Look for WebSocket errors
- Check for connection issues

**2. Refresh Page**
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear cache and reload

**3. Check Server**
- Ensure application is running
- Check terminal for errors
- Restart application if needed

**4. Firewall/Proxy**
- WebSocket might be blocked
- Check corporate firewall settings
- Try from different network

**5. Browser Compatibility**
- Use modern browser (Chrome, Firefox, Edge)
- Update browser to latest version
- Disable extensions that might interfere

**Workaround:** Refresh page after tests complete to see results

---

### **Q42: API returns 401 Unauthorized - how to fix?**

**A:**

**Causes & Solutions:**

**1. Invalid API Key**
- Verify API key on Configure page
- Check for extra spaces
- Regenerate API key if needed

**2. Expired Token**
- If using Bearer token, check expiration
- Refresh token before running tests
- Update test data with new token

**3. Missing Authorization Header**
- Ensure API_KEY is configured
- For custom auth, add to headers in test data
- Example: `Authorization: Bearer your-token`

**4. Incorrect Header Format**
- Check header syntax
- Example: `API_KEY: value` not `API_KEY=value`

**5. IP Whitelisting**
- API might restrict by IP address
- Contact API administrator
- Add server IP to whitelist

---

### **Q43: Tests run but no report generated - why?**

**A:**

**Possible Causes:**

**1. Tests Still Running**
- Wait for "All tests completed" message
- Check progress bar is at 100%

**2. Permission Issues**
- Check `test-results/` folder exists
- Verify write permissions
- Create folder manually if needed

**3. Disk Space**
- Check available disk space
- Clean up old reports if needed

**4. Application Error**
- Check terminal for error messages
- Look for Python exceptions
- Restart application

**5. Browser Download Settings**
- Check browser download folder
- Look for blocked downloads
- Allow downloads from localhost

**Manual Check:**
```powershell
# Navigate to test-results folder
cd test-results
dir  # Windows
ls   # Linux/Mac
```

---

## 🔒 Security & Privacy

### **Q44: Is my data secure?**

**A:**

**Data Storage:**
- ✅ All data stored locally on your server
- ✅ No cloud storage or external services
- ✅ No data sent to third parties
- ✅ Complete control over your data

**Security Considerations:**

**1. API Keys**
- ⚠️ Currently stored in plain text (`config.json`)
- **Recommendation:** Use environment variables in production
- **Future:** Encrypted storage

**2. Test Data**
- Stored in `Test_Data/` folder
- Accessible to anyone with server access
- **Recommendation:** Restrict folder permissions

**3. Reports**
- Stored in `test-results/` folder
- May contain sensitive response data
- **Recommendation:** Implement access controls

**4. Network**
- Development: HTTP only
- **Recommendation:** Use HTTPS in production
- Deploy behind reverse proxy (nginx) with SSL

---

### **Q45: Can multiple users use this simultaneously?**

**A:**

**Current Behavior:**
- ✅ Multiple users can access web interface
- ⚠️ Only one test run at a time (shared execution)
- ⚠️ No user authentication
- ⚠️ No user sessions

**Limitations:**
- If User A starts tests, User B must wait
- All users see same test execution
- No user-specific test history

**Workarounds:**
- Deploy multiple instances (different ports)
- Coordinate test runs among team
- Use scheduling/queue system

**Future Enhancement:**
- User authentication
- User sessions
- Test queue system
- Concurrent test runs

---

### **Q46: How do I secure this in production?**

**A:**

**Security Checklist:**

**1. Use HTTPS**
```nginx
# nginx reverse proxy with SSL
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

**2. Add Authentication**
- Implement login system
- Use Flask-Login extension
- Integrate with corporate SSO

**3. Restrict Access**
- Firewall rules (allow only internal network)
- VPN requirement
- IP whitelisting

**4. Secure API Keys**
```python
# Use environment variables
import os
api_key = os.getenv('API_KEY')
```

**5. File Permissions**
```bash
# Restrict folder access (Linux)
chmod 700 Test_Data/
chmod 700 test-results/
```

**6. Regular Updates**
```powershell
# Keep dependencies updated
pip install --upgrade -r requirements.txt
```

---

## 🚀 Advanced Usage

### **Q47: Can I add custom validation rules?**

**A:** Yes! Modify `core/test_executor.py`

**Example: Validate Response Body**
```python
# In test_executor.py, after getting response
if response.status_code == expected_status:
    # Add custom validation
    response_data = response.json()
    if 'error' in response_data:
        test_result['status'] = 'failed'
        test_result['error'] = 'Response contains error field'
    else:
        test_result['status'] = 'passed'
```

**Example: Validate Response Time**
```python
# Check if response time is acceptable
if response.elapsed.total_seconds() > 5:
    test_result['status'] = 'failed'
    test_result['error'] = f'Response too slow: {response.elapsed.total_seconds()}s'
```

**Example: Validate JSON Schema**
```python
import jsonschema

expected_schema = {...}
try:
    jsonschema.validate(response.json(), expected_schema)
    test_result['status'] = 'passed'
except jsonschema.ValidationError as e:
    test_result['status'] = 'failed'
    test_result['error'] = f'Schema validation failed: {e.message}'
```

---

### **Q48: Can I add more template variables?**

**A:** Yes! Modify `core/test_executor.py`

**Step 1: Add to Configuration** (`templates/configure.html`)
```html
<div class="mb-3">
    <label for="customVar" class="form-label">Custom Variable</label>
    <input type="text" class="form-control" id="customVar" name="customVar">
</div>
```

**Step 2: Update Replacement Logic** (`core/test_executor.py`)
```python
def replace_template_variables(text, config, language):
    text = text.replace('{{environment}}', config.get('ENVIRONMENT', ''))
    text = text.replace('{{languageCheck}}', language)
    text = text.replace('{{customVar}}', config.get('customVar', ''))  # Add this
    return text
```

**Step 3: Use in Test Data**
```csv
body
"{""customField"": ""{{customVar}}""}"
```

---

### **Q49: Can I test GraphQL APIs?**

**A:** Yes, with dynamic CSV/JSON format!

**Example (CSV):**
```csv
test_id,method,endpoint,headers,body,expected_status
GQL-001,POST,/graphql,"Content-Type: application/json","{""query"": ""{ users { id name } }""}",200
```

**Example (JSON):**
```json
{
  "test_name": "Get Users GraphQL",
  "method": "POST",
  "endpoint": "/graphql",
  "headers": "Content-Type: application/json",
  "body": {
    "query": "{ users { id name email } }"
  },
  "expected_status": "200"
}
```

**With Variables:**
```json
{
  "body": {
    "query": "mutation CreateUser($name: String!) { createUser(name: $name) { id } }",
    "variables": {
      "name": "John Doe"
    }
  }
}
```

---

### **Q50: How do I contribute to this project?**

**A:**

**Ways to Contribute:**

**1. Report Issues**
- Found a bug? Create GitHub issue
- Include steps to reproduce
- Provide error messages/screenshots

**2. Suggest Features**
- Have an idea? Open feature request
- Explain use case and benefits
- Discuss with maintainers

**3. Submit Code**
- Fork repository
- Create feature branch
- Write code + tests
- Submit pull request

**4. Improve Documentation**
- Fix typos
- Add examples
- Clarify confusing sections
- Translate to other languages

**5. Share Feedback**
- How are you using it?
- What works well?
- What could be better?

**Contact:**
- GitHub: https://github.com/syedk4/Python-API-Testing-Framework
- Issues: https://github.com/syedk4/Python-API-Testing-Framework/issues

---

## 📞 Getting Help

### **Still have questions?**

**Resources:**
- 📖 Read `PROJECT_OVERVIEW_DEMO.md` for detailed overview
- 📖 Read `README.md` for quick start guide
- 📖 Check `DEMO_PREPARATION_CHECKLIST.md` for demo tips
- 🐛 Report issues on GitHub
- 💬 Ask your team lead or project maintainer

**Common Next Steps:**
1. Try the quick start guide (Q9)
2. Download and edit a sample file
3. Run your first test
4. Review the HTML report
5. Customize for your needs

---

**Last Updated:** March 2, 2026
**Version:** 1.0.0
**Maintained by:** API Testing Team

**Feedback Welcome!** Help us improve this FAQ by suggesting additions or corrections.


