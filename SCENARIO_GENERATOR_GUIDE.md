# 🤖 Scenario Generator - User Guide

## Overview

The **Scenario Generator** is a powerful new feature that automatically generates comprehensive test scenarios from natural language requirements. No more tedious manual CSV creation!

## ✨ Features

- **Natural Language Input**: Write requirements in plain English
- **Intelligent Parsing**: Automatically extracts entities, operations, and validations
- **Comprehensive Coverage**: Generates positive, negative, edge case, and security tests
- **Multiple Formats**: Save as CSV or JSON
- **No LLM Required**: Works entirely with rule-based parsing (Phase 1)

## 🚀 How to Use

### Step 1: Access the Scenario Generator

1. Start your application: `python app.py`
2. Open browser: `http://localhost:5000`
3. Click on **"Scenario Generator"** in the navigation menu

### Step 2: Enter Your Requirements

Write your requirements or user story in the text area. Include:

- **User story** (As a... I want... So that...)
- **Acceptance criteria**
- **Validation rules**
- **Expected status codes**
- **API details** (optional: base URL, endpoint, method)

**Example:**
```
As a user, I want to create a new account with email and password,
so that I can access the system.

Acceptance Criteria:
- Email must be valid format
- Password must be at least 8 characters
- Username must be unique
- API should return 201 on success
- API should return 400 for invalid data

API Details:
- Base URL: http://api.example.com
- Endpoint: /api/users
- Method: POST
```

### Step 3: Generate Scenarios

1. Click **"Generate Test Scenarios"** button
2. Wait for processing (usually 1-2 seconds)
3. Review the generated scenarios in the table

### Step 4: Save Scenarios

1. Enter a filename (e.g., `user-registration-tests`)
2. Select format (CSV or JSON)
3. Click **"Save Scenarios"**
4. Scenarios are saved to `Test_Data/` folder

### Step 5: Run Tests

1. Click **"Go to Test Runner"** button
2. Select your generated file
3. Click **"Start Tests"**
4. View results in real-time

## 📊 What Gets Generated

For a typical user registration requirement, the generator creates:

### Positive Tests (Happy Path)
- Create user with valid data
- Get user by ID
- Update user with valid data
- Delete user

### Validation Tests
- Invalid email format
- Short password
- Missing required fields
- Duplicate username

### Edge Cases
- Empty request body
- Null values in fields
- Very long input strings

### Security Tests
- SQL injection attempts
- XSS attack attempts

## 💡 Tips for Best Results

### 1. Be Specific
❌ Bad: "Test user API"
✅ Good: "Create user with email, password, and username. Email must be valid."

### 2. Include Validations
```
- Email must be valid format
- Password must be at least 8 characters
- Username must be unique
```

### 3. Specify Status Codes
```
- Return 201 on success
- Return 400 for invalid data
- Return 404 if not found
```

### 4. Mention Business Rules
```
- Transaction must complete within 30 seconds
- Retry failed payments up to 3 times
- Fraud detection should flag suspicious transactions
```

### 5. Add API Details (Optional)
```
Base URL: http://api.example.com
Endpoint: /api/users
Method: POST
```

## 📝 Example Requirements

### Example 1: User Management
```
Create, read, update, and delete users.

Fields: email, password, username, firstName, lastName

Validations:
- Email must be valid format
- Password minimum 8 characters
- Username must be unique

API: POST /api/users
Success: 201
Error: 400, 404
```

### Example 2: Product Catalog
```
Manage product catalog with CRUD operations.

Fields: name, description, price, category, stock

Business Rules:
- Price must be greater than 0
- Stock cannot be negative
- Category must be from predefined list

Endpoint: /api/products
```

### Example 3: Payment Processing
```
Process payments using credit card or PayPal.

Validations:
- Amount must be greater than $0.01
- Credit card must pass Luhn check
- Transaction timeout: 30 seconds

Security:
- Fraud detection required
- PCI compliance checks

API: POST /api/payments
```

## 🎯 Generated Scenario Format

Each scenario includes:

| Field | Description |
|-------|-------------|
| `test_id` | Unique identifier (TC-001, TC-002, etc.) |
| `test_name` | Descriptive name |
| `test_category` | Functional, Validation, Edge Case, Security |
| `priority` | P0 (critical), P1 (high), P2 (medium) |
| `method` | HTTP method (GET, POST, PUT, DELETE) |
| `base_url` | API base URL |
| `endpoint` | API endpoint path |
| `headers` | Request headers |
| `body` | Request body (JSON) |
| `expected_status` | Expected HTTP status code |
| `description` | Test description |

## 🔧 Troubleshooting

### No scenarios generated
- Check that you've entered requirements
- Make sure requirements include at least one operation (create, read, update, delete)

### Wrong entity detected
- Be more specific in your requirements
- Explicitly mention the entity name multiple times

### Missing validations
- List validations explicitly in acceptance criteria
- Use keywords like "must", "required", "should"

### Incorrect endpoint
- Specify the endpoint explicitly in requirements
- Format: `Endpoint: /api/resource` or `API: /api/resource`

## 🚀 Next Steps

After generating scenarios:

1. **Review** - Check generated scenarios for accuracy
2. **Customize** - Edit the CSV/JSON file if needed
3. **Configure** - Set up API base URL and authentication
4. **Execute** - Run tests from Test Runner
5. **Analyze** - Review results and fix failures

## 📚 Additional Resources

- [Main README](README.md) - Application overview
- [FAQ](FAQ.md) - Frequently asked questions
- [Project Overview](PROJECT_OVERVIEW_DEMO.md) - Detailed documentation

## 🎉 Benefits

- **Time Savings**: 95%+ reduction in scenario creation time
- **Consistency**: Standardized test format
- **Coverage**: Comprehensive test scenarios
- **Quality**: Reduced manual errors
- **Productivity**: Focus on testing, not file creation

---

**Happy Testing! 🚀**

