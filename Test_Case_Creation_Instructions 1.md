# Test Case Creation Instructions

## Overview

Please note that this is for manual test case creation, not unit tests.

We need to adhere to a proper flow to validate the scenarios rather than validating fields separately.

Generate comprehensive test scenarios covering: 

Happy path flows 

Edge cases 

Error handling 

Business-critical functionality 

Avoid creating too many test cases; test scenarios can be merged where appropriate without compromising flow and coverage.

## Git Guidelines

**Never do:** git commit, git add, git push. Use folder navigation to find the subfolders.

**Code changes are in folder:** `Not Applicable`

**Git Branch (already checked out):** `Not Applicable`

**Note:** Analyze story requirements to create test cases and code implementation to find any deviations from the requirements.

## Reference Documents

The following documents should be referenced when creating Excel and Markdown test files:

- BOOKING_PLATFORM_FLOW.md
- GTM_IT_Booking Platform_Functional_specification.docx
- User Story Acceptance Criteria (mentioned below)

## Excel File Requirements

**File type:** Excel (.xlsx)

**File Name:** GTMG-Split SI QA Report

**Path:** test-case-creation-docs

### Summary Sheet

**SheetName:** TestCases

**Columns:**
- Test Case ID
- Test Description
- Priority
- Regression

**Note:** 
- Test Description: This acts as the test title and this should be a short description of the test case. 
Good Example: Cancel booking from carrier 301 request
Bad Eample: Create a booking, accept the booking from 301 carrier request, validate the acceptance, cancel the booking from 301 request and validate the cancellation.
- The Regression column is a Yes/No. 
- If the test case can be considered to be added in existing regression suite then mark it as Yes.
- If the test case is not a regression test case then mark it as No.
- Priority: Critical, High, Medium

### Individual Test Case Sheets

Create separate worksheets for each test case in the same Excel file.

**SheetName:** [Test Case ID]

**Columns:**
- Action
- Data
- Expected Result

**Note:** Data column can be empty

## Markdown File Requirements

**File type:** .md

**File Name:** Test_Steps_For_Automation.md

**Path:** test-case-creation-docs

**Content:** Document the steps to be automated for each test case. Ensure a proper flow is added here, and this Markdown file will be passed to Augment for test automation script creation later. Refer to the Reference Documents section above. Create the test steps for only Critical and High tests

### Template

```markdown
**Test Case:** [Name]
**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
...
```

## Additional Notes

- No need for summary document.
- Delete any supporting files you create for Excel generation.
- Only an Excel file with test cases should be added.

## User Story Acceptance Criteria

As a shipping operations user, when a booking has multiple containers, I want to split SI submissions by container so that each container is submitted as its own SI.

As a user, when I edit an SI after it has been submitted, I want the system to handle container changes correctly so that updates, replacements, and cancellations are sent properly.

The current need is to support SI splitting by container with mass upload support.  

A checkbox for "split SI's by container" is needed and should be defaulted for current business needs.  

This lets users upload all containers on a booking in one SI step, while the system submits one SI for each container number.

Add “Split SIs by Container” checkbox to SI Submission Form

The "split SI's by container" checkbox default state should be checked for current business needs.

When the business changes back to multiple containers on one bill of lading, the checkbox should not be defaulted as checked.

This checkbox allows the users to upload all containers on a booking if they want and do "one" SI step, but the system submits an SI for each container #.

Submit New SI - When Checkbox is CHECKED:

System submits separate SI for each container#

No changes to the current UI for submit new SI.

For a new SI submission with 10 containers:

System sends 10 XML files, one for each container.

Each XML file contains one <ContainerGroup>.

All files share the same booking # and common data.

The following data can differ by container:

Container details

Commodity details

Marks and Remarks

PO#

“No solid wood packing material” in <ContainerGroup>

Weight and Measurement in <Totals>

Submit New SI - When checkbox is UNCHECKED:

System submits one SI with all containers

For a booking with 10 containers: System sends 1 XML file

The XML file contains multiple <ContainerGroup> entries (one per container)

All containers share the same booking # and common data

After SI submission completes, system displays a pop-up confirmation message:

If checked: “X# if SIs Submitted” (Where X = number of containers)

Example: “10 SIs Submitted'

If unchecked: “1 SI Submitted”

Pop-up displays total count of SIs submitted

For editing SI after it is submitted:

No change to the current UI.

Mass upload remains disabled.

Users edit container details on the Edit SI screen.

After submitting changes, validate the container # if container # is a key:

If container # is unchanged/modified, allow update.

If container # is removed, show: “Do you want to cancel the SI for this container?”  
Consider asking users to send an updated booking with the actual number of containers shipped.

For XML updates:

If the container # is unchanged or modified, send the updated container details for those containers with ActionType = Replace.

If a container is removed, send ActionType = Cancellation for that container.

For editing information other than container/commodity details, such as consignee, POD, or destination:

No changes to the current UI.

All ten XML files, one per container, will be resent with the updated common data.

