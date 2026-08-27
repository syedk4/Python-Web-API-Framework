# Coding Standards - Python Test Automation

This document defines the coding standards and conventions for **Python** test automation frameworks using Playwright and Pytest.

> **Note:** For **JavaScript** coding standards, refer to [CODING_STANDARDS_JS.md](./CODING_STANDARDS_JS.md)
> **Note:** For **TypeScript** coding standards, refer to [CODING_STANDARDS_TS.md](./CODING_STANDARDS_TS.md)

---

## **Table of Contents**

1. [Naming Conventions](#naming-conventions)
2. [Documentation Standards](#documentation-standards)
3. [Code Structure](#code-structure)
4. [Import Standards](#import-standards)
5. [Pytest Standards](#pytest-standards)
6. [Database Query Standards](#database-query-standards)
7. [Locator Standards](#locator-standards)
8. [Async/Await Standards](#asyncawait-standards)
9. [Error Handling](#error-handling)
10. [Logging and Output Standards](#logging-and-output-standards)
11. [Constants and Configuration](#constants-and-configuration)

---

## **1. Naming Conventions**

### **1.1 Files and Folders**

| Type | Convention | Example |
|------|-----------|---------|
| **Folder names** | `snake_case` | `booking_tests/`, `test_classes/`, `page_objects_utilities/` |
| **Test files** | `test_*.py` | `test_booking_creation.py`, `test_shipping_instructions.py` |
| **Page object files** | `*_page.py` | `create_booking_page.py`, `view_booking_page.py` |
| **Helper files** | `*_helper.py` | `booking_helper.py`, `database_data_helper.py` |
| **Utility files** | `*_util.py` | `web_element_util.py`, `common_data_util.py` |

### **1.2 Classes**

- **Convention:** `PascalCase`
- **Examples:**
  - `CreateBookingPage`
  - `BookingHelper`
  - `WebElementUtil`

### **1.3 Functions and Methods**

- **Convention:** `snake_case` (Python standard - PEP 8)
- **Test methods:** MUST start with `test_` and use `snake_case`
- **Examples:**
  - ✅ `async def create_booking(...)` (regular method)
  - ✅ `async def test_verify_xml_generated(...)` (test method)
  - ✅ `async def click_when_visible(...)` (utility method)
  - ✅ `def get_user_credentials(...)` (helper method)
  - ❌ `async def createBooking(...)` (wrong - don't use camelCase in Python)

### **1.4 Variables**

| Type | Convention | Example |
|------|-----------|---------|
| **Instance variables** | `snake_case` | `booking_number`, `transaction_number`, `user_name` |
| **Local variables** | `snake_case` | `row_index`, `column_name`, `voyage_number` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT`, `BASE_URL` |
| **Pytest fixtures** | `snake_case` | `test_helper`, `csv_test_data_reader`, `database_connection` |

### **1.5 Locators (Page Objects)**

- **Convention:** Private instance variables with `_` prefix, `snake_case`
- **Pattern:** `self._<element_purpose>`
- **Examples:**
  - `self._search_essel: Locator`
  - `self._cargo_ready_date: Locator`
  - `self._edit_booking_title: Locator`
  - `self._remarks_textbox: Locator`

### **1.6 Test Method Names**

- **Convention (Option 1):** `test_[module]_[feature]_[scenario]_[expected_result]`
- **Convention (Option 2):** `test_[TestID]_[module]_[feature]_[scenario]_[expected_result]` (when linking to test management system)
- **Must:** Start with `test_`, use `snake_case`

**Format Components:**
- `[TestID]`: Test case identifier from test management system (e.g., ADO, Jira, TestRail) - optional
- `[module]`: The module or area being tested (e.g., `authentication`, `checkout`, `reporting`)
- `[feature]`: The specific feature or functionality (e.g., `create`, `edit`, `export`, `login`)
- `[scenario]`: The test scenario or condition (e.g., `with_valid_data`, `multiple_items`, `filtered_data`)
- `[expected_result]`: What should happen (e.g., `success`, `data_saved`, `error_displayed`)

**Examples:**

**Without TestID:**
- `test_authentication_login_with_valid_credentials_success`
- `test_checkout_payment_processing_with_credit_card_order_created`
- `test_reporting_template_create_and_export_data_matches_ui`
- `test_user_profile_edit_update_email_changes_reflected`

**With TestID:**
- `test_12345_authentication_login_with_valid_credentials_success`
- `test_67890_checkout_payment_processing_with_credit_card_order_created`
- `test_54321_reporting_template_create_and_export_data_matches_ui`

**Notes:**
- TestID is optional but recommended when tracking tests in test management systems
- Each component should be descriptive but concise
- Use `snake_case` throughout (Python convention)
- Order without TestID: module → feature → scenario → expected_result
- Order with TestID: TestID → module → feature → scenario → expected_result
- Omit optional components (scenario) if not applicable, but maintain logical flow

---

## **2. Documentation Standards**

### **2.1 Module/File Docstrings**

**Format:**
```python
"""
<Module Name>
<Brief 1-2 line description of module purpose>

@author <Your Name>
@created YYYY-MM-DD
@version X.Y.Z
"""
```

**Example:**
```python
"""
Common Data Utility Module
Provides utility methods for date formatting, random number generation, and data operations
for test automation.

@author John Leonard
@created 2025-08-11
@version 1.0.0
"""
```

### **2.2 Class Docstrings**

**Requirements:**
- 1-3 lines describing the class purpose
- Generic description (should not change when adding/removing methods)
- Include author, created, modified by, modified metadata

**Format:**
```python
"""
<1-3 line description of class purpose>

@author <Your Name>
@created YYYY-MM-DD
@modified_by <Modifier Name>
@modified YYYY-MM-DD
"""
from ...
class ClassName:
    <no description here as it is redundant>
```

**Example:**
```python
"""
Page object for user authentication and login functionality.
Contains locators and methods for login form interactions.

@author John Leonard
@created 2025-01-15
@modified_by John Leonard
@modified 2025-02-20
"""
from playwright.async_api import Page, Locator

class LoginPage:
```

### **2.3 Test Method Docstrings**

**Requirements:**
- 1-2 line concise description only
- No Args, Returns, Raises, or Examples sections
- Focus on WHAT the test validates, not HOW

**Format:**
```python
async def test_method_name(...):
    """<1-2 line description of what test validates>."""
```

**Examples:**
```python
async def test_authentication_login_with_valid_credentials_success(...):
    """Verify successful user login with valid credentials."""

async def test_checkout_payment_processing_with_invalid_card_error_displayed(...):
    """Verify error message is displayed when processing payment with invalid card."""

async def test_user_profile_update_email_changes_reflected(...):
    """Verify email changes are saved and reflected in user profile."""
```

### **2.4 Reusable Function/Method Docstrings**

**Requirements:**
- 1-2 line description
- Args section (brief, one line per arg)
- Returns section (brief, what is returned)
- NO Examples section
- NO Raises section

**Format:**
```python
async def method_name(arg1: Type, arg2: Type) -> ReturnType:
    """
    <1-2 line description of what the method does>.

    Args:
        arg1: <Brief description>
        arg2: <Brief description>

    Returns:
        <Brief description of return value>
    """
```

**Example:**
```python
async def click_radio_button_by_column_value(self, column_name: str, column_value: str) -> None:
    """
    Find a row by matching a column value and click its radio button.

    Args:
        column_name: The column header name to search in
        column_value: The value to match in the specified column

    Returns:
        None
    """
```

### **2.5 Inline Comments**

**Requirements:**
- Comment GROUPS of related lines, not individual lines
- Comments should be SHORT and describe WHAT is being done
- NO suggestions, examples, or improvements in comments
- Use `#` for single-line comments

**Good Examples:**
```python
# Update user profile and verify changes
user_profile.email = "newemail@example.com"
await profile_page.click_edit_button()
await profile_page.wait_for_edit_form()
await profile_page.submit_changes()

# Wait for database record update
await database_helper.wait_for_record_update(
    table_name="users",
    record_id=user_id,
    expected_status='ACTIVE'
)
```

**Bad Examples:**
```python
# Click the edit button (you could also use scroll_to_element_and_click here)
await profile_page.click_edit_button()

# Wait for the edit page to load - this is important because otherwise the email field won't be available
await profile_page.wait_for_edit_form()

await profile_page.click_edit_button() # Click the edit button
```

### **2.6 Line Length and Formatting**

**Maximum line length: 120 characters**

**Rules:**
- Keep all lines (code, comments, docstrings) within 120 characters
- Split long lines using appropriate continuation methods
- Maintain proper indentation (4 spaces per level) when splitting

### **2.7 Private locator functions**

**Rules:**
- Just add single line comment for the locator function.
- No examples, No Args, No Returns, No Raises

Bad Example:
```python
def _get_field_toggle(self, column_header: TableColumnHeaders) -> Locator:
        """
        Get the toggle switch for a specific field in the Save Template dialog.

        Args:
            column_header: TableColumnHeaders enum value for the field

        Returns:
            Locator for the field toggle switch
        """
        return self._save_template_dialog.locator(
            f'//label[normalize-space()="{column_header.value}"]/preceding-sibling::button[@role="switch"]'
        )
        
```
Good Example:
```python
def _get_field_toggle(self, column_header: TableColumnHeaders) -> Locator:
        # Get the toggle switch for a specific field in the Save Template dialog.
        return self._save_template_dialog.locator(
            f'//label[normalize-space()="{column_header.value}"]/preceding-sibling::button[@role="switch"]'
        )
        
```

### **2.8 Avoid section separators**

**Rules:**
- Avoid adding comments like below throught the code.

# ==================================================================================
        # Header Section
# ================================================================================== 

**Splitting Methods:**

**1. Function/Method Calls:**

Good - arguments on new lines with proper indentation:
```python
await database_helper.get_record_by_criteria(
    table_name="users",
    user_id=current_user_id,
    status='ACTIVE',
    max_attempts=15
)
```

Bad - exceeds 120 characters:
```python
await database_helper.get_record_by_criteria(table_name="users", user_id=current_user_id, status='ACTIVE')
```

**2. Assertions:**

Good - backslash continuation:
```python
assert user_profile.email == expected_email, \
    f"Email mismatch: expected '{expected_email}', got '{user_profile.email}'"
```

Good - parentheses for multi-line messages:
```python
assert user_profile.email == expected_email, (
    f"Email mismatch: expected '{expected_email}', "
    f"got '{user_profile.email}'"
)
```

**3. Long Locators:**

Good - split XPath with proper indentation:
```python
self._submit_button = self.page.locator(
    '//div[@class="form-actions"]'
    '//button[@type="submit"]'
)
```

**4. Conditionals:**

Good - split condition with proper indentation:
```python
if (
    user_id is not None
    and user_id != ""
    and status == "Active"
):
    await process_user()
```

**5. Long Comments:**

Good - split into multiple comment lines:
```python
# Wait for database record update
# This may take up to 5 minutes depending on system load
await wait_for_record_update()
```

**Indentation Rules:**
- Use 4 spaces per indentation level
- Indent continuation lines by one level (4 spaces) from the statement
```

---

## **3. Code Structure**

### **3.1 Folder Structure**

```
test-automation-project/
├── helpers/
│   ├── api/                    # API helper classes
│   ├── test_classes/           # Test execution helpers
│   └── testdata/               # Test data helpers
├── pages/
│   ├── authentication/         # Authentication-related page objects
│   ├── checkout/               # Checkout-related page objects
│   ├── user_profile/           # User profile page objects
│   └── page_objects_utilities/ # Shared page utilities
├── utils/                      # General utility functions
├── tests/
│   ├── e2e_tests/              # End-to-end test files
│   ├── api_tests/              # API test files
│   └── integration_tests/      # Integration test files
├── testdata/                   # Test data files
│   ├── dev/                    # Development environment data
│   ├── stage/                  # Stage environment data
│   └── prod/                   # Production environment data
└── conftest.py                 # Pytest fixtures and configuration
```

### **3.2 Class Organization**

**Order within a class:**
1. Class docstring
2. `__init__` method with locators (for page objects)
3. Public methods (alphabetically)
4. Private methods (alphabetically)

**Example:**
```python
class LoginPage:
    """Page object for user login functionality."""

    def __init__(self, page: Page):
        self.page = page
        # Locators
        self._username_input: Locator = page.get_by_label("Username")
        self._password_input: Locator = page.get_by_label("Password")
        self._submit_button: Locator = page.get_by_role("button", name="Sign In")

    # Public methods
    async def login(self, username: str, password: str) -> None:
        """Perform user login with provided credentials."""
        await self._username_input.fill(username)
        await self._password_input.fill(password)
        await self._submit_button.click()

    async def get_error_message(self) -> str:
        """Get error message text if displayed."""
        return await self._error_message.text_content()

    # Private methods
    async def _validate_form(self) -> bool:
        """Validate form fields are visible."""
        return await self._submit_button.is_visible()
```

### **3.3 Method Organization in Test Files**

**Order:**
1. Setup/teardown fixtures (if any)
2. Test methods (grouped by feature/flow)

---

## **4. Import Standards**

### **4.1 Import Order**

1. Standard library imports
2. Third-party imports (pytest, playwright)
3. Local application imports (helpers, pages, utils)

**Example:**
```python
# Standard library imports
import asyncio
from datetime import datetime
from typing import Optional

# Third-party imports
from playwright.async_api import Page, Locator
import pytest

# Local application imports
from helpers.test_classes.test_helper import TestHelper
from helpers.testdata.database_helper import DatabaseHelper
from helpers.testdata.csv_reader import CSVReader
from pages.authentication.login_page import LoginPage
from utils.date_utils import format_date
```

### **4.2 Import Style**

- Use absolute imports from project root
- Group related imports together
- One import per line for clarity
- Imports should be on the top of the file
- Imports inside the functions are allowed only in case of dynamic imports

---

## **5. Pytest Standards**

### **5.1 Test Markers**

**Usage:**
```python
@pytest.mark.authentication
@pytest.mark.smoke
@pytest.mark.usefixtures("database_connection")
class TestUserAuthentication:

    @pytest.mark.asyncio
    async def test_login_with_valid_credentials_success(...):
        pass

    @pytest.mark.asyncio
    async def test_login_with_invalid_credentials_error_displayed(...):
        pass
```

### **5.2 Assertions**

**All assertions MUST include descriptive messages for better test failure diagnosis.**

**Standard Format:**
```python
assert user_id is not None and user_id != "", \
    f"User ID should not be None or empty, got: {user_id}"

assert user_profile.email == expected_email, \
    f"Email mismatch: expected '{expected_email}', got '{user_profile.email}'"

assert status == 'Active', \
    f"Status should be 'Active', got: '{status}'"
```

### **5.3 Test Fixtures**

- Must use `snake_case`
- Place in `conftest.py`
- Document purpose clearly
- Use type hints

**Example:**
```python
@pytest.fixture
async def test_helper(page: Page) -> TestHelper:
    """Provides TestHelper instance for test execution."""
    return TestHelper(page)

@pytest.fixture
async def authenticated_page(page: Page, test_config: dict) -> Page:
    """Provides an authenticated page instance."""
    login_page = LoginPage(page)
    await login_page.login(test_config['username'], test_config['password'])
    return page

@pytest.fixture(scope="session")
def database_connection():
    """Provides database connection for the test session."""
    conn = create_database_connection()
    yield conn
    conn.close()
```

---

## **6. Database Query Standards**

### **6.1 SQL Queries**

- Always use `WITH (NOLOCK)` for SELECT queries (SQL Server specific)
- Always specify `connection_name` parameter when using multiple databases
- Use parameterized queries to prevent SQL injection
- Never concatenate user input into SQL strings

**Examples:**

**SQL Server:**
```python
query = """
    SELECT * FROM users WITH (NOLOCK)
    WHERE user_id = @user_id AND status = @status
"""
result = await database_helper.execute_query(
    query=query,
    connection_name="app_database",
    params={"user_id": user_id, "status": "Active"}
)
```

**PostgreSQL/MySQL:**
```python
query = """
    SELECT * FROM users
    WHERE user_id = %s AND status = %s
"""
result = await database_helper.execute_query(
    query=query,
    connection_name="app_database",
    params=(user_id, "Active")
)
```

**Using ORM (SQLAlchemy):**
```python
from sqlalchemy import select
from models.user import User

async def get_user_by_id(user_id: int) -> Optional[User]:
    """Get user from database by ID."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
```

---

## **7. Locator Standards**

### **7.1 Locator Priority**

**Preference order:**
1. `get_by_role()` - Most stable
2. `get_by_label()` - Good for form fields
3. `get_by_text()` - For unique text
4. XPath - Last resort for complex scenarios

**Rules**
- Never hardcode locator inside any function
- Even if its child locator everything has to be added to the constructor function
- When using locator() enclose it with '' and not ""

**Examples:**
```python
# Preferred - use semantic locators
self._submit_button = self.page.get_by_role("button", name="Submit")
self._username_input = self.page.get_by_label("Username")
self._password_input = self.page.get_by_label("Password")
self._error_message = self.page.get_by_text("Invalid credentials")

# Acceptable for complex cases
self._main_nav = self.page.locator('//nav[@class="main-navigation"]')
self._user_dropdown = self.page.locator('//div[@id="user-menu"]//button[@aria-label="User Options"]')
```

---

## **8. Async/Await Standards**

- All page interactions MUST use `await`
- Test methods MUST be `async def`
- Use `@pytest.mark.asyncio` for async tests

**Example:**
```python
@pytest.mark.asyncio
async def test_user_login_with_valid_credentials_success(self, test_helper):
    """Test successful user login."""
    await test_helper.login(username, password)
    user_data = await test_helper.get_user_profile()
    assert user_data is not None
```

---

## **9. Error Handling**

- Use specific exceptions where possible
- Provide meaningful error messages
- Include context in error messages

**Example:**
```python
if row_count == 0:
    raise ValueError(f"No rows found for user_id: {user_id}")

if matching_row_index is None:
    raise ValueError(
        f'No row found where {column_name} = "{column_value}"\n'
        f'Available values: {all_values}'
    )

if not user_data:
    raise RuntimeError(f"Failed to retrieve user data for user_id: {user_id}")

# Custom exception classes
class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class PageLoadError(Exception):
    """Raised when page fails to load within timeout."""
    pass

# Usage
if not login_successful:
    raise AuthenticationError(f"Login failed for user: {username}")
```

---

## **10. Logging and Output Standards**

### **10.1 No Print or Log Statements in Tests and Helpers**

**IMPORTANT: Do NOT add print() or logging statements in test classes and helper classes**

**Rules:**
- ❌ **Never add new `print()` statements** in:
  - Test methods (`tests/**/*test_*.py`)
  - Helper classes (`helpers/test_classes/*_helper.py`)
  - Page objects (`pages/**/*_page.py`)
  - Utility classes (`utils/*_util.py`)

- ❌ **Never add new logging statements** unless absolutely necessary:
  - Do NOT log every line of code execution
  - Do NOT log intermediate variable values
  - Do NOT log "entering method" or "exiting method"

- ✅ **Allowed/Recommended:**
  - **Assertion messages** - ALWAYS include descriptive messages in assertions
  - **Existing log functions** - If helper already uses `IStepReporter`, continue using it
  - **Selective logging** - Only log when:
    - Important data needs to be captured (e.g., booking number, transaction ID)
    - A complete module of actions is finished (e.g., "Booking created successfully")
    - Critical state changes occur (e.g., "Template deleted")

### **10.2 When to Use Logging in Helpers**

**Log sparingly - only for significant events:**

```python
# ✅ GOOD - Log when important data is generated
logger.info(f"User created successfully: {user_id}")

# ✅ GOOD - Log when a module of actions completes
logger.info("Authentication completed successfully")

# ✅ GOOD - Log important data collection
logger.info(f"Retrieved {len(user_records)} user records from database")

# ✅ GOOD - Log important state changes
logger.info(f"User status changed from '{old_status}' to '{new_status}'")

# ❌ BAD - Don't log every single action
logger.info("Clicking submit button")  # Too granular
logger.info("Entering username")  # Too granular
logger.info("Waiting for page load")  # Too granular
```

---
## **11. Constants and Configuration**

- Define constants at module or class level
- Use `UPPER_SNAKE_CASE` for constants
- Group related constants together

**Example:**
```python
# Timeout constants (in milliseconds)
DEFAULT_TIMEOUT = 20000
LONG_TIMEOUT = 60000
SHORT_TIMEOUT = 5000
MAX_RETRIES = 5

# User status constants
USER_STATUS_ACTIVE = "ACTIVE"
USER_STATUS_INACTIVE = "INACTIVE"
USER_STATUS_PENDING = "PENDING"
USER_STATUS_SUSPENDED = "SUSPENDED"

# Environment URLs
BASE_URL_DEV = "https://dev.example.com"
BASE_URL_STAGE = "https://stage.example.com"
BASE_URL_PROD = "https://prod.example.com"

# Database configuration
DB_CONNECTION_TIMEOUT = 30
DB_MAX_POOL_SIZE = 10
DB_MIN_POOL_SIZE = 2
```

---

## **Summary Checklist**

✅ **Files:** `snake_case`, appropriate suffixes (`_page.py`, `_helper.py`, `_util.py`, `test_*.py`)
✅ **Classes:** `PascalCase`, 1-3 line docstring with author/dates
✅ **Methods/Functions:** `snake_case` (including test methods: `test_snake_case`)
✅ **Variables:** `snake_case` (all variables), `UPPER_SNAKE_CASE` for constants
✅ **Locators:** `self._element_name` (private, snake_case)
✅ **Test names:** `test_[module]_[feature]_[scenario]_[result]` or `test_[TestID]_[module]_[feature]_[scenario]_[result]`
✅ **Test docstrings:** 1-2 lines, no Args/Returns/Examples
✅ **Function docstrings:** 1-2 lines + Args + Returns (no Examples/Raises)
✅ **Comments:** Group related lines, short, describe WHAT not HOW
✅ **Imports:** Standard library → Third-party → Local application
✅ **Type hints:** Use for all function parameters and return values
✅ **SQL:** Use parameterized queries, `WITH (NOLOCK)` for SQL Server
✅ **Async:** Use `await` for all async operations, `async def` for async functions
✅ **Line length:** Maximum 120 characters
✅ **Indentation:** 4 spaces per level (Python standard - PEP 8)

---

**Document Version:** 1.0.0
**Last Updated:** 2026-08-18
**Maintained By:** Test Automation Team