# Feature: [Feature Name/ID]

> **Instructions**: Fill out all sections below. The more detail you provide, the better the analysis. Use examples where helpful.

## Definition - High-level description of what needs to be done

[Describe what the feature does and why it's needed. Be specific about the user problem being solved.]

**Example**: Users need to be able to export service orders to PDF format so they can share order details with external contractors who don't have system access.

---

## Relevant Files/Flows to be Aware Of

[List existing code files, components, API endpoints, or workflows that are relevant to this feature. Include why they're relevant.]

**Example**:

- `src/pages/ServiceOrderDetails.tsx` - Where the new export button will be added
- `src/api/serviceOrders.ts` - Contains the getServiceOrder function that needs to return additional metadata
- `src/services/pdfGenerator.ts` - Existing PDF generation utility (if any)

---

## Expected Output - Compare system when feature is implemented vs. current state

**Current State**: [What happens now]

**Future State**: [What will happen after implementation]

**Example**:

- **Current**: Users can only view service order details on screen
- **Future**: Users will see an "Export to PDF" button on the order details page that generates a downloadable PDF with order information, line items, and signatures

---

## Acceptance Criteria - Clear, testable success conditions

[List specific, measurable criteria that define when this feature is complete]

**Example**:

- [ ] "Export to PDF" button visible on service order details page
- [ ] Button is disabled for orders in draft status
- [ ] Generated PDF includes: order number, customer info, line items, total, and signatures
- [ ] Loading indicator shows during PDF generation
- [ ] PDF downloads automatically when ready
- [ ] Error message displays if PDF generation fails

---

## Constraints - Performance, security, compatibility requirements

[Any technical limitations, performance requirements, security considerations, or compatibility needs]

**Example**:

- For orders with 50+ line items, PDF generation must complete within 5 seconds
- PDFs must be generated server-side (not client-side) for security
- Must work on Chrome, Firefox, Safari, Edge (latest versions)
- PDF file size should not exceed 2MB

---

## Edge Cases - Known scenarios that need special handling

[Unusual situations, data conditions, or user scenarios that need consideration]

**Example**:

- Orders migrated from old ERP may be missing signature images - show "N/A" in these cases
- Orders with custom line items need special formatting
- If PDF generation service is down, show user-friendly error and offer retry option
- Very old orders (>5 years) may have different data structure

---

## Dependencies - External systems, APIs, or features this relies on

[List any external services, APIs, libraries, or other features this depends on]

**Example**:

- PDF generation library (e.g., QuestPDF, IronPDF, PuppeteerSharp)
- Service order API must return `IsExportable` flag
- Azure Blob Storage / AWS S3 or similar for temporary PDF storage (if applicable)
- Email service (if we add "email PDF" feature later)

---

## Additional Context (Optional)

[Any other relevant information, links to designs, user stories, related tickets, etc.]

**Example**:

- Figma design: [link]
- Related ticket: JIRA-1234
- Customer request from: ABC Corp, XYZ Industries

---

## Clarifications (Auto-populated by agent)

[Leave empty - the integration analysis agent will append Q&A here]
