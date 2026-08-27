# Coding Standards - TypeScript Test Automation

This document defines the coding standards and conventions for **TypeScript** test automation frameworks using Playwright.

> **Note:** For **JavaScript** coding standards, refer to [CODING_STANDARDS_JS.md](./CODING_STANDARDS_JS.md)

---

## **Table of Contents**

1. [Naming Conventions](#naming-conventions)
2. [TypeScript-Specific Standards](#typescript-specific-standards)
3. [Documentation Standards](#documentation-standards)
4. [Code Structure](#code-structure)
5. [Import Standards](#import-standards)
6. [Playwright Test Standards](#playwright-test-standards)
7. [Locator Standards](#locator-standards)
8. [Async/Await Standards](#asyncawait-standards)
9. [Error Handling](#error-handling)
10. [Logging and Output Standards](#logging-and-output-standards)
11. [Constants and Configuration](#constants-and-configuration)
12. [TypeScript Configuration](#typescript-configuration)

---

## **1. Naming Conventions**

### **1.1 Files and Folders**

| Type | Convention | Example |
|------|-----------|---------|
| **Folder names** | `PascalCase` | `Configuration/`, `MaintenancePage/`, `Routing/` |
| **Test spec files** | `camelCase.spec.ts` | `regionRoutingMaster.spec.ts`, `routeRegionPage.spec.ts` |
| **Page object files** | `camelCase.ts` | `manualRequestPage.ts`, `cancelPage.ts` |
| **Utility files** | `camelCase.ts` | `emailService.ts`, `reportGenerator.ts` |
| **Type definition files** | `camelCase.types.ts` | `testData.types.ts`, `pageModels.types.ts` |
| **Interface files** | `camelCase.interface.ts` | `requestData.interface.ts` |
| **Setup files** | `*.setup.ts` | `auth.setup.ts` |

### **1.2 Classes**

- **Convention:** `PascalCase`
- **Examples:**
  - `ManualRequestPage`
  - `RegionRoutingMasterPage`
  - `ReportGenerator`

### **1.3 Functions and Methods**

- **Convention:** `camelCase`
- **Examples:**
  - ✅ `async navigateToPage(): Promise<void>` (regular method)
  - ✅ `async clickSubmitButton(): Promise<void>` (action method)
  - ✅ `async validatePageLoad(): Promise<boolean>` (validation method)
  - ❌ `async navigate_to_page()` (wrong - don't use snake_case)

### **1.4 Variables**

| Type | Convention | Example |
|------|-----------|---------|
| **Local variables** | `camelCase` | `userName: string`, `productPrice: number`, `rowIndex: number` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT`, `BASE_URL` |
| **Test data objects** | `camelCase` | `dataSet: TestData`, `testData: RequestData`, `configData: Config` |

### **1.5 Interfaces and Types**

| Type | Convention | Example |
|------|-----------|---------|
| **Interfaces** | `PascalCase` with `I` prefix (optional) | `IRequestData`, `RequestData`, `IUserCredentials` |
| **Type Aliases** | `PascalCase` | `RequestStatus`, `TestDataSet`, `ConfigOptions` |
| **Enums** | `PascalCase` | `RequestStatus`, `UserRole`, `PageState` |
| **Enum members** | `PascalCase` | `RequestStatus.Pending`, `UserRole.Admin` |

### **1.6 Locators (Page Objects)**

- **Convention:** Private properties with `private` modifier, `camelCase`
- **Pattern:** `private <elementPurpose>: Locator`
- **Examples:**
  - `private submitButton: Locator`
  - `private userNameInput: Locator`
  - `private confirmationMessage: Locator`
  - `private tableRow: Locator`

### **1.7 Test Method Names**

- **Convention:** Descriptive test names that convey purpose
- **Format (Option 1):** `[Module]_[Feature]_[Scenario]_[Expected Result]`
- **Format (Option 2):** `[TestID]_[Module]_[Feature]_[Scenario]_[Expected Result]` (when linking to test management system)

**Examples:**

**Without TestID:**
- `test('Routing_ManualRequest_WithValidData_Success', async ({ page }) => { ... })`
- `test('Configuration_RegionRouting_CreateNewRoute_SavedSuccessfully', async ({ page }) => { ... })`
- `test('Checkout_PaymentProcessing_ValidCreditCard_Success', async ({ page }) => { ... })`

**With TestID:**
- `test('12345_Routing_ManualRequest_WithValidData_Success', async ({ page }) => { ... })`
- `test('67890_Configuration_RegionRouting_CreateNewRoute_SavedSuccessfully', async ({ page }) => { ... })`

**Notes:**
- Use PascalCase for each component to maintain readability
- Each component should be descriptive but concise
- Avoid abbreviations unless universally understood in the domain
- TestID is optional but recommended when tracking tests in test management systems

---

## **2. TypeScript-Specific Standards**

### **2.1 Type Annotations**

**Always use explicit type annotations for:**
- Function parameters
- Function return types
- Class properties
- Complex variables

**Examples:**
```typescript
// ✅ GOOD - Explicit types
async clickActionByColumnValue(columnName: string, columnValue: string): Promise<void> {
    // Implementation
}

const userName: string = 'TestUser';
const requestId: number = 12345;
const isActive: boolean = true;

// ❌ BAD - Missing types
async clickActionByColumnValue(columnName, columnValue) {
    // Implementation
}
```

### **2.2 Interfaces**

**Use interfaces for:**
- Test data structures
- Page object method parameters
- API response shapes
- Configuration objects

**Convention:**
- Use `PascalCase` for interface names
- Prefix with `I` is optional but be consistent across the project
- Define in separate `.types.ts` or `.interface.ts` files when shared

**Examples:**
```typescript
// testData.types.ts
export interface RequestData {
    requestType: string;
    userName: string;
    priority: number;
    notes?: string; // Optional property
}

export interface UserCredentials {
    username: string;
    password: string;
    role: UserRole;
}

export interface TestConfig {
    baseUrl: string;
    timeout: number;
    retries: number;
}
```

**Usage in Page Objects:**
```typescript
import { RequestData } from '../types/testData.types';

class ManualRequestPage {
    async fillRequestForm(data: RequestData): Promise<void> {
        await this.requestTypeDropdown.selectOption(data.requestType);
        await this.userNameInput.fill(data.userName);
        if (data.notes) {
            await this.notesTextarea.fill(data.notes);
        }
    }
}
```

### **2.3 Type Aliases**

**Use type aliases for:**
- Union types
- Literal types
- Complex type compositions
- Function signatures

**Examples:**
```typescript
// types.ts
export type RequestStatus = 'Pending' | 'Submitted' | 'Approved' | 'Rejected';
export type UserRole = 'Admin' | 'User' | 'Guest';
export type TestEnvironment = 'dev' | 'stage' | 'prod';

// Function type
export type ClickHandler = (element: Locator) => Promise<void>;
export type ValidationFunction = (value: string) => boolean;

// Complex type composition
export type RequestWithMetadata = RequestData & {
    createdAt: Date;
    createdBy: string;
};
```

**Usage:**
```typescript
async updateRequestStatus(requestId: number, status: RequestStatus): Promise<void> {
    // Implementation
}

const currentStatus: RequestStatus = 'Pending';
```

### **2.4 Enums**

**Use enums for:**
- Fixed set of constants
- Status values
- Configuration options
- Page states

**Convention:**
- Use `PascalCase` for enum names
- Use `PascalCase` for enum members
- Prefer string enums for better debugging

**Examples:**
```typescript
// enums.ts
export enum RequestStatus {
    Pending = 'PENDING',
    Submitted = 'SUBMITTED',
    Approved = 'APPROVED',
    Rejected = 'REJECTED',
    Cancelled = 'CANCELLED'
}

export enum UserRole {
    Admin = 'ADMIN',
    Manager = 'MANAGER',
    User = 'USER',
    Guest = 'GUEST'
}

export enum PageState {
    Loading = 'LOADING',
    Ready = 'READY',
    Error = 'ERROR'
}
```

**Usage:**
```typescript
import { RequestStatus } from '../types/enums';

class RequestPage {
    async getRequestStatus(): Promise<RequestStatus> {
        const statusText = await this.statusField.textContent();
        return statusText as RequestStatus;
    }

    async validateStatus(expected: RequestStatus): Promise<boolean> {
        const actual = await this.getRequestStatus();
        return actual === expected;
    }
}
```

### **2.5 Generics**

**Use generics for:**
- Reusable utility functions
- Page object base classes
- Data transformation functions

**Examples:**
```typescript
// Generic utility function
async function getTableData<T>(rows: Locator[]): Promise<T[]> {
    const data: T[] = [];
    for (const row of rows) {
        const rowData = await extractRowData<T>(row);
        data.push(rowData);
    }
    return data;
}

// Generic base page class
export class BasePage<T> {
    constructor(protected page: Page, protected validator?: (data: T) => boolean) {}

    async loadData(): Promise<T> {
        // Implementation
    }

    async validateData(data: T): Promise<boolean> {
        return this.validator ? this.validator(data) : true;
    }
}

// Usage
interface RequestPageData {
    requestId: string;
    status: RequestStatus;
}

class RequestPage extends BasePage<RequestPageData> {
    // Implementation
}
```

### **2.6 Access Modifiers**

**Use TypeScript access modifiers:**
- `public` - Accessible from anywhere (default)
- `private` - Only accessible within the class
- `protected` - Accessible within the class and subclasses
- `readonly` - Cannot be modified after initialization

**Examples:**
```typescript
class ManualRequestPage {
    private page: Page;
    protected baseUrl: string;
    public readonly pageName: string = 'Manual Request Page';

    private submitButton: Locator;
    protected validationRules: ValidationRule[];

    constructor(page: Page) {
        this.page = page;
        this.submitButton = page.locator('button[type="submit"]');
    }

    // Public method
    public async fillForm(data: RequestData): Promise<void> {
        await this.validateFormData(data);
        await this.fillFormFields(data);
    }

    // Private helper method
    private async validateFormData(data: RequestData): Promise<void> {
        if (!data.requestType) {
            throw new Error('Request type is required');
        }
    }

    // Protected method for subclasses
    protected async fillFormFields(data: RequestData): Promise<void> {
        // Implementation
    }
}
```

### **2.7 Readonly and Const Assertions**

**Use `readonly` for:**
- Properties that shouldn't change after initialization
- Array/object properties that should be immutable

**Use `as const` for:**
- Literal type inference
- Constant arrays/objects

**Examples:**
```typescript
class TestConfig {
    readonly baseUrl: string;
    readonly timeout: number;
    readonly supportedBrowsers: readonly string[];

    constructor(baseUrl: string, timeout: number) {
        this.baseUrl = baseUrl;
        this.timeout = timeout;
        this.supportedBrowsers = ['chromium', 'firefox', 'webkit'];
    }
}

// Const assertion
const REQUEST_TYPES = ['Manual', 'Automated', 'Scheduled'] as const;
type RequestType = typeof REQUEST_TYPES[number]; // 'Manual' | 'Automated' | 'Scheduled'

const CONFIG = {
    maxRetries: 3,
    timeout: 30000,
    environments: ['dev', 'stage', 'prod']
} as const;
```

### **2.8 Utility Types**

**Use built-in TypeScript utility types:**
- `Partial<T>` - Make all properties optional
- `Required<T>` - Make all properties required
- `Pick<T, K>` - Pick specific properties
- `Omit<T, K>` - Omit specific properties
- `Record<K, T>` - Create object type with specific keys

**Examples:**
```typescript
interface RequestData {
    requestType: string;
    userName: string;
    priority: number;
    notes: string;
}

// Make all properties optional for updates
type PartialRequestData = Partial<RequestData>;

async function updateRequest(id: number, data: PartialRequestData): Promise<void> {
    // Can update only specific fields
}

// Pick specific properties
type RequestSummary = Pick<RequestData, 'requestType' | 'userName'>;

// Omit specific properties
type RequestWithoutNotes = Omit<RequestData, 'notes'>;

// Create a lookup object
type StatusMessages = Record<RequestStatus, string>;

const messages: StatusMessages = {
    [RequestStatus.Pending]: 'Request is pending approval',
    [RequestStatus.Submitted]: 'Request has been submitted',
    [RequestStatus.Approved]: 'Request approved',
    [RequestStatus.Rejected]: 'Request rejected',
    [RequestStatus.Cancelled]: 'Request cancelled'
};
```

### **2.9 Type Guards and Type Narrowing**

**Use type guards for:**
- Runtime type checking
- Narrowing union types
- Validating data structures

**Examples:**
```typescript
// Type guard function
function isRequestData(data: unknown): data is RequestData {
    return (
        typeof data === 'object' &&
        data !== null &&
        'requestType' in data &&
        'userName' in data &&
        'priority' in data
    );
}

// Usage
async function processData(data: unknown): Promise<void> {
    if (isRequestData(data)) {
        // TypeScript knows data is RequestData here
        await submitRequest(data);
    } else {
        throw new Error('Invalid request data');
    }
}

// Discriminated unions
type SuccessResult = { success: true; data: RequestData };
type ErrorResult = { success: false; error: string };
type Result = SuccessResult | ErrorResult;

function handleResult(result: Result): void {
    if (result.success) {
        // TypeScript knows result.data exists
        console.log('Request submitted:', result.data);
    } else {
        // TypeScript knows result.error exists
        console.error('Error:', result.error);
    }
}
```

### **2.10 Null and Undefined Handling**

**Always enable strict null checks in `tsconfig.json`**

**Use optional chaining and nullish coalescing:**

**Examples:**
```typescript
// Optional chaining (?.)
const userName = user?.profile?.name ?? 'Unknown';
const requestId = data?.request?.id;

// Nullish coalescing (??)
const timeout = config.timeout ?? DEFAULT_TIMEOUT;
const retries = options?.retries ?? MAX_RETRIES;

// Non-null assertion (use sparingly!)
const element = page.locator('#submit')!; // Only if you're 100% sure it exists

// Better: Handle null explicitly
async function getRequestId(): Promise<string | null> {
    const element = await this.page.locator('#request-id').textContent();
    return element ?? null;
}

async function getRequiredRequestId(): Promise<string> {
    const requestId = await this.getRequestId();
    if (!requestId) {
        throw new Error('Request ID not found');
    }
    return requestId;
}
```

---

## **3. Documentation Standards**

### **3.1 Module/File TSDoc Comments**

**Format:**
```typescript
/**
 * @file Module Name
 * @description Brief 1-2 line description of module purpose
 * @author Your Name
 * @created YYYY-MM-DD
 * @version X.Y.Z
 */
```

**Example:**
```typescript
/**
 * @file Email Service Module
 * @description Provides utility methods for sending test execution reports via email
 * @author John Leonard
 * @created 2025-08-11
 * @version 1.0.0
 */

import { Page } from '@playwright/test';
import { EmailConfig } from './types/config.types';

export class EmailService {
    // Implementation
}
```

### **3.2 Class TSDoc Comments**

**Requirements:**
- 1-3 lines describing the class purpose
- Generic description (should not change when adding/removing methods)
- Include author and date metadata
- Document generic type parameters if used

**Format:**
```typescript
/**
 * Brief 1-3 line description of class purpose
 *
 * @template T - Description of generic type parameter (if applicable)
 * @author Your Name
 * @created YYYY-MM-DD
 * @modified_by Modifier Name
 * @modified YYYY-MM-DD
 */
export class ClassName<T> {
    // Class implementation
}
```

**Example:**
```typescript
/**
 * Page object for creating and managing manual routing requests in the TPS application.
 * Contains locators and methods for manual request form interactions.
 *
 * @author John Leonard
 * @created 2025-01-15
 * @modified_by John Leonard
 * @modified 2025-02-20
 */
export class ManualRequestPage {
    private page: Page;
    private submitButton: Locator;

    constructor(page: Page) {
        this.page = page;
        this.submitButton = page.locator('button[type="submit"]');
    }
}
```

### **3.3 Interface/Type TSDoc Comments**

**Document interfaces and types with TSDoc:**

**Examples:**
```typescript
/**
 * Represents the data structure for a manual routing request.
 */
export interface RequestData {
    /** Unique identifier for the request */
    requestId: number;

    /** Type of request (Manual, Automated, Scheduled) */
    requestType: string;

    /** Name of the user creating the request */
    userName: string;

    /** Priority level (1-5, where 1 is highest) */
    priority: number;

    /** Optional notes or comments */
    notes?: string;
}

/**
 * Status values for a routing request.
 */
export enum RequestStatus {
    /** Request is awaiting approval */
    Pending = 'PENDING',

    /** Request has been submitted for processing */
    Submitted = 'SUBMITTED',

    /** Request has been approved */
    Approved = 'APPROVED'
}
```

### **3.4 Function/Method TSDoc Comments**

**Requirements:**
- 1-2 line description
- `@param` for each parameter with type
- `@returns` with type description
- `@throws` for exceptions (optional but recommended)
- NO Examples section

**Format:**
```typescript
/**
 * Brief 1-2 line description of what the method does.
 *
 * @param paramName - Brief description
 * @param paramName2 - Brief description
 * @returns Brief description of return value
 * @throws Error description (optional)
 */
async methodName(paramName: Type, paramName2: Type): Promise<ReturnType> {
    // Implementation
}
```

**Example:**
```typescript
/**
 * Finds a row in the table by matching a column value and clicks its action button.
 *
 * @param columnName - The column header name to search in
 * @param columnValue - The value to match in the specified column
 * @returns Promise that resolves when the action button is clicked
 * @throws Error if the row is not found
 */
async clickActionByColumnValue(columnName: string, columnValue: string): Promise<void> {
    const row = await this.findRowByColumnValue(columnName, columnValue);
    if (!row) {
        throw new Error(`Row not found for ${columnName} = ${columnValue}`);
    }
    await row.locator('button.action').click();
}
```

### **3.5 Inline Comments**

**Same rules as JavaScript:**
- Comment GROUPS of related lines, not individual lines
- Comments should be SHORT and describe WHAT is being done
- Use `//` for single-line comments

**Examples:**
```typescript
// Navigate to manual request page and fill form
await page.goto('/manual-request');
await manualRequestPage.fillRequestForm(testData);
await manualRequestPage.submitRequest();

// Wait for confirmation and validate status
await expect(page.locator('.confirmation-message')).toBeVisible();
const status = await manualRequestPage.getRequestStatus();
expect(status).toBe(RequestStatus.Submitted);
```

---

## **4. Code Structure**

### **4.1 Folder Structure**

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
├── types/                      # TypeScript type definitions
│   ├── enums.ts               # Enum definitions
│   ├── interfaces.ts          # Shared interfaces
│   ├── testData.types.ts      # Test data types
│   └── config.types.ts        # Configuration types
├── utils/                      # Utility functions and helpers
├── playwright.config.ts        # Playwright configuration
├── tsconfig.json              # TypeScript configuration
└── testData/                   # Test data files (JSON, CSV)
```

### **4.2 Class Organization**

**Order within a Page Object class:**
1. Class TSDoc comment
2. Private/protected properties (locators, state)
3. Constructor with parameter types
4. Public methods (alphabetically)
5. Protected methods (alphabetically)
6. Private helper methods (alphabetically)

**Example:**
```typescript
/**
 * Page object for manual request creation and management.
 *
 * @author John Leonard
 * @created 2025-01-15
 */
export class ManualRequestPage {
    // Properties
    private readonly page: Page;
    private readonly submitButton: Locator;
    private readonly requestTypeDropdown: Locator;

    // Constructor
    constructor(page: Page) {
        this.page = page;
        this.submitButton = page.locator('button[type="submit"]');
        this.requestTypeDropdown = page.locator('#request-type');
    }

    // Public methods
    public async fillRequestForm(data: RequestData): Promise<void> {
        await this.requestTypeDropdown.selectOption(data.requestType);
        await this.submitButton.click();
    }

    public async getRequestId(): Promise<string> {
        const id = await this.page.locator('#request-id').textContent();
        if (!id) throw new Error('Request ID not found');
        return id;
    }

    // Protected methods
    protected async validateFormData(data: RequestData): Promise<boolean> {
        return !!data.requestType && !!data.userName;
    }

    // Private methods
    private async waitForFormLoad(): Promise<void> {
        await this.submitButton.waitFor({ state: 'visible' });
    }
}
```

### **4.3 Test File Organization**

**Order:**
1. Imports (typed imports)
2. Type/Interface definitions (if test-specific)
3. Test data with types
4. `test.describe` block
5. Setup/teardown hooks with types
6. Test cases

**Example:**
```typescript
import { test, expect, Page } from '@playwright/test';
import { ManualRequestPage } from '../../pages/Routing/manualRequestPage';
import { RequestData, RequestStatus } from '../../types/testData.types';
import testData from '../../testData/requests.json';

test.describe('Manual Request Page Tests', () => {
    let manualRequestPage: ManualRequestPage;

    test.beforeEach(async ({ page }: { page: Page }) => {
        manualRequestPage = new ManualRequestPage(page);
        await page.goto('/manual-request');
    });

    test('Routing_ManualRequest_WithValidData_Success', async ({ page }: { page: Page }) => {
        const requestData: RequestData = testData.validRequest;
        await manualRequestPage.fillRequestForm(requestData);

        const status = await manualRequestPage.getRequestStatus();
        expect(status).toBe(RequestStatus.Submitted);
    });
});
```

---

## **5. Import Standards**

### **5.1 Import Order**

1. Playwright test framework imports
2. Third-party library imports
3. Type imports (using `import type`)
4. Page object imports
5. Utility/helper imports
6. Type definition imports
7. Enum imports
8. Test data imports

**Example:**
```typescript
// Playwright imports
import { test, expect, Page, Locator } from '@playwright/test';

// Third-party imports
import { chromium } from 'playwright';

// Type-only imports
import type { RequestData, UserCredentials } from '../types/testData.types';
import type { TestConfig } from '../types/config.types';

// Page object imports
import { ManualRequestPage } from '../pages/Routing/manualRequestPage';
import { RegionRoutingMasterPage } from '../pages/Configuration/regionRoutingMasterPage';

// Utility imports
import { EmailService } from '../utils/emailService';
import { ReportGenerator } from '../utils/reportGenerator';

// Enum imports
import { RequestStatus, UserRole } from '../types/enums';

// Test data imports
import testData from '../testData/requests.json';
```

### **5.2 Import Style**

- Use ES6 `import` syntax (not `require()`)
- Use `import type` for type-only imports (optimizes bundle size)
- Use named imports over default imports for better refactoring
- Group related imports together
- One import per line for clarity

**Examples:**
```typescript
// ✅ GOOD - Type-only import
import type { RequestData } from './types';
import { processRequest } from './utils';

// ✅ GOOD - Named imports
import { ManualRequestPage, CancelPage } from './pages/Routing';

// ❌ BAD - Mixed value and type imports (use import type instead)
import { RequestData, processRequest } from './module';

// ✅ GOOD - Separate type and value imports
import type { RequestData } from './types';
import { processRequest } from './utils';
```

---

## **6. Playwright Test Standards**

### **6.1 Test Annotations and Tags**

**Usage:**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Region Routing Master Tests', () => {

    test('Configuration_RegionRoutingMaster_CreateNewRecord_Success @smoke @regression',
        async ({ page }: { page: Page }) => {
        // Test implementation
    });

    test('67890_Configuration_RegionRoutingMaster_EditExisting_UpdatedSuccessfully @regression',
        async ({ page }: { page: Page }) => {
        // Test implementation
    });
});
```

### **6.2 Typed Assertions**

**Use typed assertions for better type safety:**

**Examples:**
```typescript
// Typed page fixture
test('test with typed page', async ({ page }: { page: Page }) => {
    await page.goto('/manual-request');

    // TypeScript knows exact types
    const requestId: string | null = await page.locator('#request-id').textContent();
    expect(requestId).toBeTruthy();
});

// Typed expectations with interfaces
interface RequestResponse {
    id: number;
    status: RequestStatus;
}

test('API response validation', async ({ request }) => {
    const response = await request.get<RequestResponse>('/api/requests/123');
    const data = await response.json();

    expect(data.id).toBe(123);
    expect(data.status).toBe(RequestStatus.Submitted);
});
```

### **6.3 Custom Fixtures with Types**

**Create strongly-typed custom fixtures:**

**Example:**
```typescript
// fixtures.ts
import { test as base, Page } from '@playwright/test';
import { ManualRequestPage } from '../pages/Routing/manualRequestPage';
import { TestConfig } from '../types/config.types';

type MyFixtures = {
    manualRequestPage: ManualRequestPage;
    testConfig: TestConfig;
};

export const test = base.extend<MyFixtures>({
    manualRequestPage: async ({ page }: { page: Page }, use) => {
        const manualRequestPage = new ManualRequestPage(page);
        await use(manualRequestPage);
    },

    testConfig: async ({}, use) => {
        const config: TestConfig = {
            baseUrl: process.env.BASE_URL || 'https://test.example.com',
            timeout: 30000,
            retries: 3
        };
        await use(config);
    }
});

export { expect } from '@playwright/test';
```

**Usage in tests:**
```typescript
import { test, expect } from './fixtures';

test('Routing_ManualRequest_WithValidData_Success',
    async ({ page, manualRequestPage, testConfig }) => {
    // TypeScript knows all fixture types
    await page.goto(testConfig.baseUrl + '/manual-request');
    await manualRequestPage.fillRequestForm(testData);

    const requestId = await manualRequestPage.getRequestId();
    expect(requestId).toBeTruthy();
});
```

---

## **7. Locator Standards**

### **7.1 Typed Locators**

**Always explicitly type locators:**

**Examples:**
```typescript
export class ManualRequestPage {
    private readonly submitButton: Locator;
    private readonly userNameInput: Locator;
    private readonly statusText: Locator;

    constructor(private readonly page: Page) {
        this.submitButton = page.getByRole('button', { name: 'Submit Request' });
        this.userNameInput = page.getByLabel('User Name');
        this.statusText = page.getByText('Status: Active');
    }
}
```

### **7.2 Locator Methods with Return Types**

**Always specify return types for methods returning locators:**

**Examples:**
```typescript
export class TablePage {
    private readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    // Returns a single locator
    getRowByStatus(status: RequestStatus): Locator {
        return this.page.locator(`tr[data-status="${status}"]`);
    }

    // Returns multiple locators
    getAllRows(): Locator {
        return this.page.locator('table tbody tr');
    }

    // Returns a specific cell
    getCellByColumnName(rowIndex: number, columnName: string): Locator {
        return this.page.locator(`tr:nth-child(${rowIndex}) td.${columnName}`);
    }
}
```

---

## **8. Async/Await Standards**

**All page interactions must:**
- Be declared as `async`
- Return `Promise<T>` with explicit type
- Use `await` for all Playwright actions

**Examples:**
```typescript
export class ManualRequestPage {
    private readonly page: Page;
    private readonly submitButton: Locator;

    constructor(page: Page) {
        this.page = page;
        this.submitButton = page.locator('button[type="submit"]');
    }

    // ✅ GOOD - Explicit Promise<void> return type
    async submitRequest(): Promise<void> {
        await this.submitButton.click();
    }

    // ✅ GOOD - Explicit Promise<string> return type
    async getRequestId(): Promise<string> {
        const id = await this.page.locator('#request-id').textContent();
        if (!id) throw new Error('Request ID not found');
        return id;
    }

    // ✅ GOOD - Explicit Promise<boolean> return type
    async isSubmitButtonEnabled(): Promise<boolean> {
        return await this.submitButton.isEnabled();
    }
}
```

---

## **9. Error Handling**

### **9.1 Custom Error Classes**

**Define typed error classes:**

**Examples:**
```typescript
// errors.ts
export class PageLoadError extends Error {
    constructor(
        public readonly pageName: string,
        public readonly timeout: number
    ) {
        super(`Failed to load ${pageName} within ${timeout}ms`);
        this.name = 'PageLoadError';
    }
}

export class ElementNotFoundError extends Error {
    constructor(
        public readonly elementName: string,
        public readonly selector: string
    ) {
        super(`Element ${elementName} not found using selector: ${selector}`);
        this.name = 'ElementNotFoundError';
    }
}

export class ValidationError extends Error {
    constructor(
        public readonly field: string,
        public readonly expectedValue: unknown,
        public readonly actualValue: unknown
    ) {
        super(`Validation failed for ${field}: expected ${expectedValue}, got ${actualValue}`);
        this.name = 'ValidationError';
    }
}
```

**Usage:**
```typescript
export class ManualRequestPage {
    async submitRequest(): Promise<void> {
        try {
            await this.submitButton.click({ timeout: 5000 });
        } catch (error) {
            throw new ElementNotFoundError('Submit Button', 'button[type="submit"]');
        }
    }

    async validateStatus(expected: RequestStatus): Promise<void> {
        const actual = await this.getRequestStatus();
        if (actual !== expected) {
            throw new ValidationError('Request Status', expected, actual);
        }
    }
}
```

### **9.2 Type Guards for Error Handling**

**Use type guards for error handling:**

**Examples:**
```typescript
function isPageLoadError(error: unknown): error is PageLoadError {
    return error instanceof PageLoadError;
}

async function handlePageLoad(page: Page): Promise<void> {
    try {
        await page.goto('/manual-request', { waitUntil: 'networkidle' });
    } catch (error) {
        if (isPageLoadError(error)) {
            console.error(`Page load error: ${error.pageName}`);
        } else if (error instanceof Error) {
            console.error(`Unknown error: ${error.message}`);
        } else {
            console.error('Unknown error occurred');
        }
        throw error;
    }
}
```

---

## **10. Logging and Output Standards**

### **10.1 Typed Logging Functions**

**Create typed logging utilities:**

**Examples:**
```typescript
// logger.ts
export enum LogLevel {
    Debug = 'DEBUG',
    Info = 'INFO',
    Warn = 'WARN',
    Error = 'ERROR'
}

export interface LogEntry {
    level: LogLevel;
    message: string;
    timestamp: Date;
    context?: Record<string, unknown>;
}

export class Logger {
    private static formatMessage(entry: LogEntry): string {
        const contextStr = entry.context
            ? ` | Context: ${JSON.stringify(entry.context)}`
            : '';
        return `[${entry.timestamp.toISOString()}] [${entry.level}] ${entry.message}${contextStr}`;
    }

    static log(level: LogLevel, message: string, context?: Record<string, unknown>): void {
        const entry: LogEntry = {
            level,
            message,
            timestamp: new Date(),
            context
        };

        const formatted = this.formatMessage(entry);

        switch (level) {
            case LogLevel.Error:
                console.error(formatted);
                break;
            case LogLevel.Warn:
                console.warn(formatted);
                break;
            default:
                console.log(formatted);
        }
    }

    static info(message: string, context?: Record<string, unknown>): void {
        this.log(LogLevel.Info, message, context);
    }

    static error(message: string, context?: Record<string, unknown>): void {
        this.log(LogLevel.Error, message, context);
    }
}
```

**Usage:**
```typescript
import { Logger } from '../utils/logger';

async function submitRequest(data: RequestData): Promise<string> {
    Logger.info('Submitting request', {
        requestType: data.requestType,
        userName: data.userName
    });

    try {
        const requestId = await processRequest(data);
        Logger.info('Request submitted successfully', { requestId });
        return requestId;
    } catch (error) {
        Logger.error('Failed to submit request', {
            error: error instanceof Error ? error.message : 'Unknown error'
        });
        throw error;
    }
}
```

---

## **11. Constants and Configuration**

### **11.1 Typed Constants**

**Define constants with explicit types:**

**Examples:**
```typescript
// constants.ts
export const TIMEOUTS = {
    DEFAULT: 20000,
    LONG: 60000,
    SHORT: 5000
} as const;

export type TimeoutKey = keyof typeof TIMEOUTS;
export type TimeoutValue = typeof TIMEOUTS[TimeoutKey];

export const MAX_RETRIES: number = 5;
export const PAGE_LOAD_TIMEOUT: number = 30000;

export const ROUTES = {
    MANUAL_REQUEST: '/manual-request',
    ROUTING_MASTER: '/configuration/region-routing-master',
    CANCEL_PAGE: '/routing/cancel'
} as const;

export type RoutePath = typeof ROUTES[keyof typeof ROUTES];
```

### **11.2 Configuration with Interfaces**

**Define configuration objects with interfaces:**

**Examples:**
```typescript
// config.types.ts
export interface DatabaseConfig {
    host: string;
    port: number;
    database: string;
    username: string;
    password: string;
}

export interface ApiConfig {
    baseUrl: string;
    timeout: number;
    retries: number;
    headers: Record<string, string>;
}

export interface TestConfig {
    environment: 'dev' | 'stage' | 'prod';
    database: DatabaseConfig;
    api: ApiConfig;
    playwright: {
        headless: boolean;
        slowMo: number;
        timeout: number;
    };
}

// config.ts
import { TestConfig } from './types/config.types';

export const config: TestConfig = {
    environment: (process.env.ENV as 'dev' | 'stage' | 'prod') || 'dev',
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: parseInt(process.env.DB_PORT || '5432'),
        database: process.env.DB_NAME || 'test_db',
        username: process.env.DB_USER || 'user',
        password: process.env.DB_PASS || 'password'
    },
    api: {
        baseUrl: process.env.API_URL || 'https://api.test.com',
        timeout: 30000,
        retries: 3,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    },
    playwright: {
        headless: process.env.HEADLESS === 'true',
        slowMo: parseInt(process.env.SLOW_MO || '0'),
        timeout: 30000
    }
};
```

---

## **12. TypeScript Configuration**

### **12.1 tsconfig.json**

**Recommended TypeScript configuration for test automation:**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./",
    "strict": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "types": ["node", "@playwright/test"],
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["pages/*"],
      "@utils/*": ["utils/*"],
      "@types/*": ["types/*"],
      "@tests/*": ["tests/*"]
    }
  },
  "include": [
    "pages/**/*.ts",
    "tests/**/*.ts",
    "utils/**/*.ts",
    "types/**/*.ts",
    "playwright.config.ts"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

### **12.2 Path Aliases**

**Use path aliases for cleaner imports:**

**tsconfig.json setup:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["pages/*"],
      "@utils/*": ["utils/*"],
      "@types/*": ["types/*"]
    }
  }
}
```

**Usage in code:**
```typescript
// Instead of: import { ManualRequestPage } from '../../../pages/Routing/manualRequestPage';
import { ManualRequestPage } from '@pages/Routing/manualRequestPage';

// Instead of: import { Logger } from '../../utils/logger';
import { Logger } from '@utils/logger';

// Instead of: import { RequestData } from '../types/testData.types';
import type { RequestData } from '@types/testData.types';
```

---

## **Summary Checklist**

✅ **Files:** `camelCase.spec.ts`, `camelCase.ts` (folders: `PascalCase`)
✅ **Type files:** `camelCase.types.ts`, `camelCase.interface.ts`
✅ **Classes:** `PascalCase`, TSDoc with author/dates
✅ **Interfaces:** `PascalCase` (optional `I` prefix)
✅ **Types:** `PascalCase` for type aliases
✅ **Enums:** `PascalCase` with `PascalCase` members
✅ **Methods:** `camelCase` with explicit return types
✅ **Variables:** `camelCase` with type annotations (constants: `UPPER_SNAKE_CASE`)
✅ **Locators:** `private elementName: Locator`
✅ **Test names:** `Module_Feature_Scenario_ExpectedResult` or `TestID_Module_Feature_Scenario_ExpectedResult`
✅ **Type annotations:** Always use explicit types for parameters and return values
✅ **Access modifiers:** Use `public`, `private`, `protected`, `readonly` appropriately
✅ **Null safety:** Enable strict null checks, use optional chaining (`?.`) and nullish coalescing (`??`)
✅ **Imports:** Use ES6 imports, separate type imports with `import type`
✅ **Error handling:** Use custom typed error classes
✅ **Line length:** Maximum 120 characters
✅ **Indentation:** 2 spaces per level
✅ **TSConfig:** Enable strict mode and all strict flags

---

**Document Version:** 1.0.0
**Last Updated:** 2026-08-18
**Maintained By:** Test Automation Team
