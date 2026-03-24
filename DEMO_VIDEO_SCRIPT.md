# Demo Video Script - Python Web API Testing Framework

## 🎬 **Video Structure (10-15 minutes)**

### **Part 1: Introduction (1-2 minutes)**
### **Part 2: Configuration (2 minutes)**
### **Part 3: AI-Powered Scenario Generation (3-4 minutes)**
### **Part 4: Test Execution (3-4 minutes)**
### **Part 5: Results & Reports (2-3 minutes)**
### **Part 6: Conclusion (1 minute)**

---

## 📝 **Detailed Script**

---

### **PART 1: INTRODUCTION (1-2 minutes)**

**[Screen: Desktop/IDE]**

**Script:**
> "Hello! Today I'm going to demonstrate the **Python Web API Testing Framework** - an intelligent, AI-powered testing solution that automatically generates and executes comprehensive API test scenarios.
>
> This framework combines the power of **Large Language Models** with traditional testing approaches to help QA teams and developers quickly create, execute, and validate API tests.
>
> **Key Features we'll cover today:**
> - ✅ AI-powered test scenario generation from natural language requirements
> - ✅ Automated test execution with real-time progress tracking
> - ✅ Comprehensive HTML reports with detailed results
> - ✅ Support for multiple authentication methods
> - ✅ CSV and JSON test data formats
>
> Let's get started!"

**[Action: Open browser, navigate to http://localhost:5000]**

---

### **PART 2: DASHBOARD & CONFIGURATION (2 minutes)**

**[Screen: Dashboard page]**

**Script:**
> "Here's the main dashboard. As you can see, we have a clean, intuitive interface with several key sections:
>
> **1. Test Runner** - Execute existing test scenarios
> **2. Scenario Generator** - AI-powered test creation (this is our star feature!)
> **3. Configuration** - Set up API endpoints and authentication
> **4. Results** - View historical test results
>
> Let me quickly show you the configuration page."

**[Action: Click on "Configure" in navigation]**

**[Screen: Configuration page]**

**Script:**
> "In the configuration page, you can set up:
> - **API Base URL** - Your API server endpoint
> - **Default endpoint** - The API path
> - **HTTP Method** - GET, POST, PUT, DELETE, etc.
> - **API Key** - For authentication
> - **Timeout settings** - Request timeout in seconds
> - **Language settings** - For multi-language support
>
> You can also configure **Azure OpenAI** or **OpenAI** credentials here for AI-powered features.
>
> For this demo, I've already configured the settings, so let's move to the exciting part - **AI-powered scenario generation**!"

**[Action: Click "Scenario Generator" in navigation]**

---

### **PART 3: AI-POWERED SCENARIO GENERATION (3-4 minutes)**

**[Screen: Scenario Generator page]**

**Script:**
> "This is where the magic happens! The **Scenario Generator** uses Large Language Models to automatically create comprehensive test scenarios from simple natural language requirements.
>
> Notice the **LLM toggle** at the top - when enabled, it uses AI to parse requirements and generate intelligent test cases. When disabled, it falls back to rule-based generation.
>
> Let me demonstrate with a real-world example. I'll paste a user story for an Invoice Extraction API."

**[Action: Paste this user story in the text area]**

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

**Script:**
> "As you can see, I've provided:
> - The **API URL** - our target endpoint
> - The **API Key** - for authentication
> - A simple description of the **required fields**
> - The **expected status codes**
>
> Now watch what happens when I click 'Generate Scenarios'..."

**[Action: Click "Generate Scenarios" button]**

**[Screen: Loading indicator appears]**

**Script:**
> "The AI is now analyzing the requirements, extracting structured information, and generating comprehensive test scenarios. This typically takes 5-10 seconds."

**[Screen: Scenarios appear in table]**

**Script:**
> "Excellent! The AI has generated **15 comprehensive test scenarios** covering:
>
> **1. Functional Tests** - Happy path scenarios with valid data
> **2. Validation Tests** - Testing field validations, required fields, format checks
> **3. Business Logic Tests** - Duplicate data, state transitions
> **4. Edge Cases** - Empty bodies, null values, boundary conditions
> **5. Security Tests** - SQL injection, XSS attacks
>
> Notice how each scenario has:
> - A unique **Test ID** (TC-001, TC-002, etc.)
> - A descriptive **Test Name**
> - A **Category** (Functional, Validation, Security, etc.)
> - **Priority** (P0, P1, P2)
> - The **HTTP Method** (POST)
> - The **Endpoint** (/PDFViewer)
> - **Expected Status Code** (200, 400, etc.)
>
> The AI automatically understood:
> - How to split the URL into base_url and endpoint
> - Which fields are required
> - What validations to test
> - What security tests to include
>
> This would take hours to create manually, but the AI did it in seconds!"

**[Action: Scroll through the scenarios table]**

**Script:**
> "Let me show you a few interesting scenarios:
> - **TC-001**: Create invoice with valid data - the happy path
> - **TC-003**: Missing required field 'environment' - validation test
> - **TC-009**: Duplicate invoice data - business logic test
> - **TC-014**: SQL injection attempt - security test
>
> Now let's download these scenarios as a CSV file for execution."

**[Action: Click "Download CSV" button]**

**Script:**
> "The scenarios are now saved as a CSV file in the Test_Data folder. Let's execute these tests!"

---

### **PART 4: TEST EXECUTION (3-4 minutes)**

**[Action: Click "Test Runner" in navigation]**

**[Screen: Test Runner page]**

**Script:**
> "Welcome to the **Test Runner**! This is where we execute our test scenarios and see real-time results.
>
> You can see:
> - A dropdown to **select test files** from the Test_Data folder
> - **Language selection** for multi-language testing
> - A **Start Tests** button to begin execution
> - Real-time **progress tracking**
> - A **Stop Tests** button to cancel execution if needed
>
> Let me select the CSV file we just generated."

**[Action: Select "generated-scenarios.csv" from dropdown]**

**Script:**
> "I've selected our generated scenarios. Now let's start the test execution!"

**[Action: Click "Start Tests" button]**

**[Screen: Progress bar and test log appear]**

**Script:**
> "The tests are now running! Notice:
>
> **1. Real-time Progress Bar** - Shows percentage completion
> **2. Test Log** - Live updates of each test execution
> **3. Test Counter** - Shows current test number and total
>
> The framework is:
> - Making actual HTTP requests to the API
> - Validating response status codes
> - Checking response data
> - Logging all results
>
> Let's watch a few tests execute..."

**[Screen: Tests executing, log scrolling]**

**Script:**
> "You can see each test in the log:
> - **Test ID and Name**
> - **Request details** (method, endpoint, body)
> - **Response status**
> - **Pass/Fail result**
>
> Some tests are passing (✅) and some are failing (❌) - this is expected because we're testing validation scenarios that should fail.
>
> For example:
> - TC-001 (valid data) - **PASSED** ✅
> - TC-003 (missing required field) - **FAILED** ❌ (expected behavior!)
>
> The framework correctly validates both positive and negative test cases."

**[Screen: Tests complete, summary appears]**

**Script:**
> "Great! All tests have completed. Let's look at the summary:
> - **Total Tests**: 15
> - **Passed**: 8
> - **Failed**: 7
> - **Pass Rate**: 53%
>
> The failed tests are actually validation and security tests that are supposed to fail - they're testing error handling.
>
> Now let's view the detailed HTML report!"

**[Action: Click "View Report" button]**

---

### **PART 5: RESULTS & REPORTS (2-3 minutes)**

**[Screen: HTML Report opens in new tab]**

**Script:**
> "Here's the comprehensive HTML test report! This is automatically generated after each test run.
>
> **Report Sections:**
>
> **1. Executive Summary**
> - Total tests executed
> - Pass/Fail counts
> - Pass rate percentage
> - Execution timestamp
>
> **2. Test Results Table**
> - All test cases with detailed information
> - Color-coded status (Green = Pass, Red = Fail)
> - Request and response details
> - Execution time for each test
>
> Let me scroll through the results..."

**[Action: Scroll through report]**

**Script:**
> "Notice how each test shows:
> - **Test ID and Name**
> - **Category and Priority**
> - **HTTP Method and Endpoint**
> - **Request Body** (the test data sent)
> - **Expected vs Actual Status**
> - **Response Data**
> - **Pass/Fail Status**
>
> This makes it easy to:
> - Identify which tests failed
> - Debug issues quickly
> - Share results with the team
> - Track test coverage
>
> You can save this report, email it, or integrate it into your CI/CD pipeline."

**[Action: Go back to Results page]**

**[Screen: Results history page]**

**Script:**
> "Back in the application, you can view all historical test results. Each report is saved with a timestamp, so you can track test execution over time and compare results."

---

### **PART 6: ADDITIONAL FEATURES (1-2 minutes)**

**[Action: Navigate back to Scenario Generator]**

**Script:**
> "Let me quickly show you a few more powerful features:
>
> **1. Multiple Authentication Methods**
> - API Key (Header or Query Parameter)
> - Bearer Token
> - Basic Authentication
> - No Authentication
>
> **2. Flexible Input Formats**
> - Natural language requirements (as we saw)
> - CSV files with test data
> - JSON test definitions
>
> **3. Customizable Test Data**
> - The AI generates realistic test data
> - You can customize any scenario before downloading
> - Support for template variables
>
> **4. Multi-language Support**
> - Test APIs in different languages
> - Automatic language parameter injection
>
> **5. Export Options**
> - Download as CSV
> - Download as JSON
> - Copy to clipboard"

---

### **PART 7: CONCLUSION (1 minute)**

**[Screen: Dashboard]**

**Script:**
> "To summarize, the **Python Web API Testing Framework** provides:
>
> ✅ **AI-Powered Test Generation** - Create comprehensive test scenarios from simple requirements in seconds
> ✅ **Automated Execution** - Run tests with real-time progress tracking
> ✅ **Detailed Reporting** - Professional HTML reports with all test details
> ✅ **Flexible Configuration** - Support for various authentication methods and API types
> ✅ **Easy Integration** - CSV/JSON formats work with any CI/CD pipeline
>
> **Benefits:**
> - **Save Time**: Generate 15+ test scenarios in 10 seconds vs hours manually
> - **Improve Coverage**: AI creates tests you might not think of (security, edge cases)
> - **Reduce Errors**: Automated execution eliminates manual testing mistakes
> - **Better Documentation**: Comprehensive reports for stakeholders
>
> **Perfect for:**
> - QA Engineers
> - API Developers
> - DevOps Teams
> - Anyone testing REST APIs
>
> Thank you for watching! If you have questions or want to learn more, please check the documentation or reach out to the team.
>
> Happy Testing! 🚀"

**[Screen: Fade to end screen with project info]**

---

## 🎯 **End Screen Text:**

```
Python Web API Testing Framework
AI-Powered API Testing Made Simple

GitHub: [Your Repository URL]
Documentation: [Your Docs URL]
Contact: [Your Email]

⭐ Star us on GitHub!
```

---

**Total Duration: ~12-15 minutes**

