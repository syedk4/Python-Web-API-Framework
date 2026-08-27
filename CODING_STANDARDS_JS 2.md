# Coding Standards - JavaScript Test Automation

This document defines the coding standards and conventions for **JavaScript** test automation frameworks using Playwright.

> **Note:** For **TypeScript** coding standards, refer to [CODING_STANDARDS_TS.md](./CODING_STANDARDS_TS.md)

---

## **Table of Contents**

1. [Naming Conventions](#naming-conventions)
2. [Documentation Standards](#documentation-standards)
3. [Code Structure](#code-structure)
4. [Import Standards](#import-standards)
5. [Playwright Test Standards](#playwright-test-standards)
6. [Locator Standards](#locator-standards)
7. [Async/Await Standards](#asyncawait-standards)
8. [Error Handling](#error-handling)
9. [Logging and Output Standards](#logging-and-output-standards)
10. [Constants and Configuration](#constants-and-configuration)

---

## **1. Naming Conventions**

### **1.1 Files and Folders**

| Type | Convention | Example |
|------|-----------|---------|
| **Folder names** | `PascalCase` | `Configuration/`, `MaintenancePage/`, `Routing/` |
| **Test spec files** | `camelCase.spec.js` | `regionRoutingMaster.spec.js`, `routeRegionPage.spec.js` |
| **Page object files** | `camelCase.js` | `manualRequestPage.js`, `cancelPage.js` |
| **Utility files** | `camelCase.js` | `emailService.js`, `reportGenerator.js` |
| **Setup files** | `*.setup.js` | `auth.setup.js` |

### **1.2 Classes**

- **Convention:** `PascalCase`
- **Examples:**
  - `ManualRequestPage`
  - `RegionRoutingMasterPage`
  - `ReportGenerator`

### **1.3 Functions and Methods**

- **Convention:** `camelCase`
- **Examples:**
  - ✅ `async navigateToPage()` (regular method)
  - ✅ `async clickSubmitButton()` (action method)
  - ✅ `async validatePageLoad()` (validation method)
  - ❌ `async navigate_to_page()` (wrong - don't use snake_case)

### **1.4 Variables**

| Type | Convention | Example |
|------|-----------|---------|
| **Local variables** | `camelCase` | `userName`, `productPrice`, `rowIndex` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT`, `BASE_URL` |
| **Test data objects** | `camelCase` | `dataSet`, `testData`, `configData` |

### **1.5 Locators (Page Objects)**

- **Convention:** Private properties with `#` prefix (ES2022) or underscore prefix, `camelCase`
- **Pattern:** `this._<elementPurpose>` or `this.#<elementPurpose>`
- **Examples:**
  - `this._submitButton`
  - `this._userNameInput`
  - `this._confirmationMessage`
  - `this._tableRow`

### **1.6 Test Method Names**

- **Convention:** Descriptive test names that convey purpose
- **Format (Option 1):** `[Module]_[Feature]_[Scenario]_[Expected Result]`
- **Format (Option 2):** `[TestID]_[Module]_[Feature]_[Scenario]_[Expected Result]` (when linking to test management system)

**Examples:**

**Without TestID:**
- `test('Routing_ManualRequest_WithValidData_Success', async ({ page }) => { ... })`
- `test('Configuration_RegionRouting_CreateNewRoute_SavedSuccessfully', async ({ page }) => { ... })`
- `test('Maintenance_CancelRequest_WithConfirmation_StatusUpdated', async ({ page }) => { ... })`
- `test('Checkout_PaymentProcessing_ValidCreditCard_Success', async ({ page }) => { ... })`

**With TestID (when linked to ADO, Jira, TestRail, etc.):**
- `test('12345_Routing_ManualRequest_WithValidData_Success', async ({ page }) => { ... })`
- `test('67890_Configuration_RegionRouting_CreateNewRoute_SavedSuccessfully', async ({ page }) => { ... })`
- `test('TC001_Checkout_PaymentProcessing_ValidCreditCard_Success', async ({ page }) => { ... })`

**Notes:**
- Use PascalCase for each component to maintain readability
- Each component should be descriptive but concise
- Avoid abbreviations unless universally understood in the domain
- TestID is optional but recommended when tracking tests in test management systems
- Order without TestID: Module → Feature → Scenario → Expected Result
- Order with TestID: TestID → Module → Feature → Scenario → Expected Result

---

## **2. Documentation Standards**

### **2.1 Module/File JSDoc Comments**

**Format:**
```javascript
/**
 * @file <Module Name>
 * @description <Brief 1-2 line description of module purpose>
 * @author <Your Name>
 * @created YYYY-MM-DD
 * @version X.Y.Z
 */
```

**Example:**
```javascript
/**
 * @file Email Service Module
 * @description Provides utility methods for sending test execution reports via email
 * @author John Leonard
 * @created 2025-08-11
 * @version 1.0.0
 */
```

### **2.2 Class JSDoc Comments**

**Requirements:**
- 1-3 lines describing the class purpose
- Generic description (should not change when adding/removing methods)
- Include author and date metadata

**Format:**
```javascript
/**
 * <1-3 line description of class purpose>
 * 
 * @author <Your Name>
 * @created YYYY-MM-DD
 * @modified_by <Modifier Name>
 * @modified YYYY-MM-DD
 */
class ClassName {
    // Class implementation
}
```

**Example:**
```javascript
/**
 * Page object for creating and managing manual routing requests in the TPS application.
 * Contains locators and methods for manual request form interactions.
 * 
 * @author John Leonard
 * @created 2025-01-15
 * @modified_by John Leonard
 * @modified 2025-02-20
 */
class ManualRequestPage {
    constructor(page) {
        this.page = page;
    }
}
```

### **2.3 Test Method JSDoc Comments**

**Requirements:**
- 1-2 line concise description only
- No detailed Args, Returns, or Examples sections
- Focus on WHAT the test validates, not HOW

**Format:**
```javascript
// Without TestID
test('Module_Feature_Scenario_ExpectedResult', async ({ page }) => {
    // Test validates <what the test checks>
});

// With TestID (optional)
test('TestID_Module_Feature_Scenario_ExpectedResult', async ({ page }) => {
    // Test validates <what the test checks>
});
```

**Examples:**
```javascript
// Without TestID
test('Configuration_RegionRoutingMaster_CreateNewRecord_Success', async ({ page }) => {
    // Validates successful creation of new region routing master record
});

test('Routing_CancelRequest_WithConfirmation_StatusUpdated', async ({ page }) => {
    // Verifies routing request status changes to 'Cancelled' after cancellation
});

// With TestID
test('12345_Configuration_RegionRoutingMaster_CreateNewRecord_Success', async ({ page }) => {
    // Validates successful creation of new region routing master record
});

test('67890_Routing_CancelRequest_WithConfirmation_StatusUpdated', async ({ page }) => {
    // Verifies routing request status changes to 'Cancelled' after cancellation
});
```

### **2.4 Reusable Function/Method JSDoc Comments**

**Requirements:**
- 1-2 line description
- @param for each parameter (brief, one line per param)
- @returns section (brief, what is returned)
- NO Examples section

**Format:**
```javascript
/**
 * <1-2 line description of what the method does>.
 *
 * @param {Type} paramName - <Brief description>
 * @param {Type} paramName2 - <Brief description>
 * @returns {ReturnType} <Brief description of return value>
 */
async methodName(paramName, paramName2) {
    // Implementation
}
```

**Example:**
```javascript
/**
 * Finds a row in the table by matching a column value and clicks its action button.
 *
 * @param {string} columnName - The column header name to search in
 * @param {string} columnValue - The value to match in the specified column
 * @returns {Promise<void>}
 */
async clickActionByColumnValue(columnName, columnValue) {
    // Implementation
}
```

### **2.5 Inline Comments**

**Requirements:**
- Comment GROUPS of related lines, not individual lines
- Comments should be SHORT and describe WHAT is being done
- NO suggestions, examples, or improvements in comments
- Use `//` for single-line comments, `/* */` for multi-line

**Good Examples:**
```javascript
// Navigate to manual request page and fill form
await page.goto('/manual-request');
await manualRequestPage.fillRequestForm(testData);
await manualRequestPage.submitRequest();

// Wait for confirmation and validate
await expect(page.locator('.confirmation-message')).toBeVisible();
const requestId = await manualRequestPage.getRequestId();
```

**Bad Examples:**
```javascript
// Click the submit button (you could also use click() here)
await manualRequestPage.submitRequest();

// Wait for the page to load - this is important because otherwise the form won't be available
await page.waitForLoadState('networkidle');

await page.click('.submit-btn'); // Click the submit button
```

### **2.6 Line Length and Formatting**

**Maximum line length: 120 characters**

**Rules:**
- Keep all lines (code, comments, JSDoc) within 120 characters
- Split long lines using appropriate continuation methods
- Use proper indentation (2 spaces per level for JavaScript/Playwright convention)

**Splitting Methods:**

**1. Function/Method Calls:**
```javascript
// Good - arguments on new lines
await expect(page.locator('.status'))
  .toHaveText('Submitted', {
    timeout: 10000
  });

// Bad - exceeds 120 characters
await expect(page.locator('.status')).toHaveText('Submitted', { timeout: 10000, ignoreCase: true });
```

**2. Assertions:**
```javascript
// Good - split with proper indentation
expect(actualValue).toBe(expectedValue,
  `Value mismatch: expected '${expectedValue}', got '${actualValue}'`);

// Good - multi-line with template literals
expect(actualValue).toBe(expectedValue,
  `Value mismatch: expected '${expectedValue}', ` +
  `got '${actualValue}'`);
```

**3. Long Locators:**
```javascript
// Good - split locator with proper indentation
this._submitButton = page.locator(
  '//div[contains(@class, "form-actions")]' +
  '//button[text()="Submit Request"]'
);
```

### **2.7 Private Locator Helper Methods**

**Rules:**
- Add single line comment for the locator helper method
- No JSDoc, No @param, No @returns

**Bad Example:**
```javascript
/**
 * Get the status cell for a specific row in the table.
 *
 * @param {string} rowId - The row identifier
 * @returns {Locator} Locator for the status cell
 */
getStatusCell(rowId) {
  return this.page.locator(`#row-${rowId} .status-cell`);
}
```

**Good Example:**
```javascript
// Get the status cell for a specific row in the table
getStatusCell(rowId) {
  return this.page.locator(`#row-${rowId} .status-cell`);
}
```

### **2.8 Avoid Section Separators**

**Rules:**
- Avoid adding decorative comment separators like:

```javascript
// ==================================================================================
// Header Section
// ==================================================================================
```

---

## **3. Code Structure**

### **3.1 Folder Structure**

```
transportation-ads-tps-automation/
├── pages/
│   ├── Configuration/          # Configuration-related page objects
│   ├── MaintenancePage/        # Maintenance-related page objects
│   └── Routing/                # Routing-related page objects
├── tests/
│   ├── ConfigurationTest/      # Configuration test specs
│   ├── MaintenanceTest/        # Maintenance test specs
│   └── RoutingTest/            # Routing test specs
├── Utils/                      # Utility functions and helpers
├── playwright.config.js        # Playwright configuration
└── testData/                   # Test data files (JSON, CSV)
```

### **3.2 Class Organization**

**Order within a Page Object class:**
1. Class JSDoc comment
2. `constructor()` method with locator initialization
3. Public methods (alphabetically)
4. Private helper methods (alphabetically)

**Example:**
```javascript
/**
 * Page object for manual request creation and management.
 *
 * @author John Leonard
 * @created 2025-01-15
 */
class ManualRequestPage {
  constructor(page) {
    this.page = page;
    // Locators
    this._requestTypeDropdown = page.locator('#request-type');
    this._submitButton = page.locator('button[type="submit"]');
  }

  // Public methods
  async fillRequestForm(data) {
    // Implementation
  }

  async submitRequest() {
    // Implementation
  }

  // Private methods
  async _validateFormFields() {
    // Implementation
  }
}
```

### **3.3 Test File Organization**

**Order:**
1. Imports
2. Test data loading
3. `test.describe` block
4. Setup/teardown hooks (`beforeAll`, `beforeEach`, `afterAll`, `afterEach`)
5. Test cases (grouped by feature/flow)

**Example:**
```javascript
const { test, expect } = require('@playwright/test');
const { ManualRequestPage } = require('../../pages/Routing/manualRequestPage');
const testData = require('../../Utils/testData.json');

test.describe('Manual Request Page Tests', () => {

  test.beforeEach(async ({ page }) => {
    // Setup code
  });

  // Without TestID
  test('Routing_ManualRequest_WithValidData_Success', async ({ page }) => {
    // Test implementation
  });

  // With TestID (optional)
  test('12345_Routing_ManualRequest_RequiredFields_ValidationError', async ({ page }) => {
    // Test implementation
  });
});
```

---

## **4. Import Standards**

### **4.1 Import Order**

1. Playwright test framework imports
2. Third-party library imports (if any)
3. Page object imports
4. Utility/helper imports
5. Test data imports

**Example:**
```javascript
const { test, expect } = require('@playwright/test');
const { chromium } = require('playwright');

const { ManualRequestPage } = require('../../pages/Routing/manualRequestPage');
const { RegionRoutingMasterPage } = require('../../pages/Configuration/regionRoutingMasterPage');

const { emailService } = require('../../Utils/emailService');
const { reportGenerator } = require('../../Utils/reportGenerator');

const testData = require('../../Utils/testData.json');
```

### **4.2 Import Style**

- Use `require()` for CommonJS modules (current project standard)
- Use `import` for ES6 modules if migrating to ESM
- Group related imports together
- One import per line for clarity
- Imports should be at the top of the file
- Dynamic imports inside functions are allowed only when necessary

---

## **5. Playwright Test Standards**

### **5.1 Test Annotations and Tags**

**Usage:**
```javascript
test.describe('Region Routing Master Tests', () => {

  // Without TestID
  test('Configuration_RegionRoutingMaster_CreateNewRecord_Success @smoke @regression', async ({ page }) => {
    // Test implementation
  });

  // With TestID (optional)
  test('67890_Configuration_RegionRoutingMaster_EditExisting_UpdatedSuccessfully @regression', async ({ page }) => {
    // Test implementation
  });
});
```

### **5.2 Assertions**

**All assertions MUST include descriptive error messages for better test failure diagnosis.**

**Standard Format:**
```javascript
expect(requestId).toBeTruthy();
expect(requestId).not.toBe('',
  `Request ID should not be empty, got: ${requestId}`);

expect(status).toBe('Submitted',
  `Status mismatch: expected 'Submitted', got '${status}'`);

await expect(page.locator('.confirmation-message'))
  .toHaveText('Request submitted successfully',
    'Confirmation message not displayed correctly');
```

### **5.3 Test Fixtures and Hooks**

**Usage:**
```javascript
test.beforeAll(async () => {
  // One-time setup for all tests
});

test.beforeEach(async ({ page }) => {
  // Setup before each test
  await page.goto('/');
});

test.afterEach(async ({ page }, testInfo) => {
  // Cleanup after each test
  if (testInfo.status !== 'passed') {
    await page.screenshot({ path: `failure-${testInfo.title}.png` });
  }
});

test.afterAll(async () => {
  // One-time cleanup for all tests
});
```

### **5.4 Page Object Fixtures**

**Example:**
```javascript
// In conftest or fixture file
const { test: base } = require('@playwright/test');
const { ManualRequestPage } = require('../pages/Routing/manualRequestPage');

const test = base.extend({
  manualRequestPage: async ({ page }, use) => {
    const manualRequestPage = new ManualRequestPage(page);
    await use(manualRequestPage);
  }
});

// In test file
test('Routing_ManualRequest_WithValidData_Success', async ({ page, manualRequestPage }) => {
  await manualRequestPage.fillForm(testData);
});
```

---

## **6. Locator Standards**

### **6.1 Locator Priority**

**Preference order:**
1. `page.getByRole()` - Most stable, accessibility-friendly
2. `page.getByLabel()` - Good for form fields
3. `page.getByText()` - For unique text content
4. `page.getByTestId()` - For elements with test-specific attributes
5. CSS selectors - For simple, stable selectors
6. XPath - Last resort for complex scenarios

**Rules:**
- Never hardcode locators inside methods
- Define all locators in the constructor
- Use single quotes for locator strings

**Examples:**
```javascript
// Preferred
this._submitButton = page.getByRole('button', { name: 'Submit Request' });
this._userNameInput = page.getByLabel('User Name');
this._statusText = page.getByText('Status: Active');

// Acceptable for complex cases
this._tableRow = page.locator('table.data-grid tbody tr').first();
this._specificCell = page.locator('//td[@class="status-cell"]');
```

### **6.2 Dynamic Locators**

**For dynamic elements, use helper methods:**
```javascript
// In page object class
getRowByStatus(status) {
  return this.page.locator(`tr[data-status="${status}"]`);
}

getCellByColumnName(rowIndex, columnName) {
  return this.page.locator(`tr:nth-child(${rowIndex}) td.${columnName}`);
}
```

---

## **7. Async/Await Standards**

- All page interactions MUST use `await`
- Test methods MUST be `async`
- Use `await` for all Playwright actions and assertions

**Example:**
```javascript
test('Routing_ManualRequest_SubmitForm_Success', async ({ page }) => {
  await page.goto('/manual-request');
  await page.fill('#user-name', 'TestUser');
  await page.click('button[type="submit"]');
  await expect(page.locator('.success-message')).toBeVisible();
});
```

**Parallel Actions (when safe):**
```javascript
// Execute independent actions in parallel
await Promise.all([
  page.waitForResponse(response => response.url().includes('/api/submit')),
  page.click('button[type="submit"]')
]);
```

---

## **8. Error Handling**

- Use try-catch for expected failures
- Provide meaningful error messages
- Include context in error messages
- Use Playwright's built-in retry and timeout mechanisms

**Example:**
```javascript
async submitRequest() {
  try {
    await this._submitButton.click({ timeout: 5000 });
  } catch (error) {
    throw new Error(`Failed to click submit button: ${error.message}`);
  }
}

async getRequestId() {
  const requestId = await this._requestIdField.textContent();
  if (!requestId || requestId.trim() === '') {
    throw new Error('Request ID is empty or not found');
  }
  return requestId.trim();
}
```

---

## **9. Logging and Output Standards**

### **9.1 No Console.log in Production Code**

**IMPORTANT: Minimize console.log() usage in test code and page objects**

**Rules:**
- ❌ **Avoid `console.log()`** in:
  - Test files (`tests/**/*.spec.js`)
  - Page object classes (`pages/**/*.js`)
  - Utility classes (`Utils/*.js`)

- ✅ **Allowed/Recommended:**
  - **Test reporting frameworks** - Use Playwright's built-in reporting
  - **Selective logging** - Only log when:
    - Important data needs to be captured (e.g., request ID, transaction ID)
    - Critical errors occur
    - Debugging complex issues (remove after fixing)

### **9.2 When to Use Logging**

**Log sparingly - only for significant events:**
```javascript
// ✅ GOOD - Log important data generation
console.log(`Request created: ${requestId}`);

// ✅ GOOD - Log critical errors
console.error(`Failed to submit request: ${error.message}`);

// ❌ BAD - Don't log every action
console.log('Clicking submit button');  // Too granular
console.log('Entering user name');      // Too granular
console.log('Waiting for page load');   // Too granular
```

### **9.3 Use Playwright Reporters**

**Prefer built-in reporting over manual logging:**
```javascript
// In playwright.config.js
reporter: [
  ['html'],
  ['json', { outputFile: 'test-results.json' }],
  ['junit', { outputFile: 'junit-results.xml' }]
]

// In tests, use test.step for structured logging
test('Routing_ManualRequest_CompleteWorkflow_Success', async ({ page }) => {
  await test.step('Navigate to manual request page', async () => {
    await page.goto('/manual-request');
  });

  await test.step('Fill and submit form', async () => {
    await manualRequestPage.fillForm(testData);
    await manualRequestPage.submit();
  });
});
```

---

## **10. Constants and Configuration**

- Define constants at module or config level
- Use `UPPER_SNAKE_CASE` for constants
- Group related constants together
- Use environment variables for environment-specific values

**Example:**
```javascript
// constants.js
const TIMEOUTS = {
  DEFAULT: 20000,
  LONG: 60000,
  SHORT: 5000
};

const MAX_RETRIES = 5;
const PAGE_LOAD_TIMEOUT = 30000;

const ROUTES = {
  MANUAL_REQUEST: '/manual-request',
  ROUTING_MASTER: '/configuration/region-routing-master',
  CANCEL_PAGE: '/routing/cancel'
};

module.exports = {
  TIMEOUTS,
  MAX_RETRIES,
  PAGE_LOAD_TIMEOUT,
  ROUTES
};
```

**Environment Configuration:**
```javascript
// In .env file
BASE_URL=https://test.example.com
API_TIMEOUT=30000
MAX_WORKERS=4

// In playwright.config.js
require('dotenv').config();

module.exports = defineConfig({
  use: {
    baseURL: process.env.BASE_URL,
  },
  timeout: parseInt(process.env.API_TIMEOUT),
  workers: parseInt(process.env.MAX_WORKERS)
});
```

---

## **Summary Checklist**

✅ **Files:** `camelCase.spec.js`, `camelCase.js` (except folders: `PascalCase`)
✅ **Classes:** `PascalCase`, JSDoc with author/dates
✅ **Methods:** `camelCase`, descriptive names
✅ **Variables:** `camelCase` (constants: `UPPER_SNAKE_CASE`)
✅ **Locators:** `this._camelCase` or `this.#camelCase`
✅ **Test names:** `Module_Feature_Scenario_ExpectedResult` or `TestID_Module_Feature_Scenario_ExpectedResult`
✅ **Test tags:** Use `@smoke`, `@regression` for test categorization
✅ **Function JSDoc:** Description + @param + @returns (no Examples)
✅ **Comments:** Group related lines, short, describe WHAT not HOW
✅ **Imports:** Playwright → Third-party → Local → Test data
✅ **Locators:** Prefer getByRole/getByLabel, define in constructor
✅ **Async:** Use `await` for all page interactions
✅ **Line length:** Maximum 120 characters
✅ **Indentation:** 2 spaces per level

---

**Document Version:** 1.0.0
**Last Updated:** 2026-08-18
**Maintained By:** Test Automation Team
