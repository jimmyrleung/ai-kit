# Feature: [API Endpoint Name]

> **Feature Type**: API Endpoint Addition

> **Instructions**: This template is pre-filled for adding a new API endpoint. Customize the bracketed sections.

## Definition

Add a new API endpoint `[METHOD] /api/[resource]/[action]` that allows [users/systems] to [perform what action].

**Business Value**: [Why is this endpoint needed? What problem does it solve?]

**Example Use Case**: [Concrete example of when/how this endpoint would be used]

---

## Relevant Files/Flows

- `Controllers/[Resource]Controller.cs` - Controller with API endpoints
- `Services/[Resource]Service.cs` - Business logic layer
- `Services/I[Resource]Service.cs` - Service interface
- `Models/[Resource].cs` - Data model / Entity
- `Repositories/[Resource]Repository.cs` - Data access layer
- `Middleware/AuthenticationMiddleware.cs` - Authentication middleware (if endpoint is protected)
- Database table: `[TableName]`

---

## Expected Output

**Current State**:

- [Describe what API endpoints currently exist for this resource]
- [What workarounds are users doing without this endpoint?]

**Future State**:

- New endpoint `[METHOD] /api/[resource]/[action]` available
- [Describe the behavior when called]
- Returns [describe response format]

---

## Acceptance Criteria

- [ ] Endpoint `[METHOD] /api/[resource]/[action]` responds correctly
- [ ] Request validation works (reject invalid inputs with 400)
- [ ] Authentication required (returns 401 if not authenticated)
- [ ] Authorization checked (returns 403 if user lacks permission)
- [ ] Success response matches contract (200 or 201)
- [ ] Error responses follow standard format (400, 404, 500)
- [ ] Endpoint documented in API docs
- [ ] Rate limiting applied (if applicable)

---

## API Contract

### Request

**Method**: `[GET/POST/PUT/DELETE/PATCH]`

**URL**: `/api/[resource]/[action]` or `/api/[resource]/{id}/[action]`

**Headers**:

- Authorization: Bearer <token>
- Content-Type: application/json

**Body** (if POST/PUT/PATCH):

```json
{
  "field1": "string",
  "field2": 123,
  "field3": true
}
```

**C# DTO**:

```csharp
public class [Resource]Request
{
    public string Field1 { get; set; }
    public int Field2 { get; set; }
    public bool Field3 { get; set; }
}
```

**Query Parameters** (if GET):

- param1: [description] (required/optional)
- param2: [description] (required/optional)

### Response

Success (200/201):

```json
{
  "success": true,
  "data": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "field1": "value",
    "field2": 123
  }
}
```

**C# Response DTO**:

```csharp
public class [Resource]Response
{
    public bool Success { get; set; }
    public [Resource]Data Data { get; set; }
}

public class [Resource]Data
{
    public Guid Id { get; set; }
    public string Field1 { get; set; }
    public int Field2 { get; set; }
}
```

Error (400 - Bad Request):

```json
{
  "success": false,
  "error": "Validation error",
  "details": ["field1 is required", "field2 must be a positive number"]
}
```

Error (401 - Unauthorized):

```json
{
  "success": false,
  "error": "Authentication required"
}
```

Error (404 - Not Found):

```json
{
  "success": false,
  "error": "Resource not found"
}
```

Error (500 - Internal Server Error):

```json
{
  "success": false,
  "error": "Internal server error"
}
```

## Constraints

- Performance: Response time should be < [X]ms for typical requests
- Rate Limiting: [X] requests per minute per user/IP (use AspNetCoreRateLimit)
- Data Size: Request body should not exceed [X]KB
- Authentication: Must use existing JWT authentication ([Authorize] attribute)
- Backwards Compatibility: [Should not break existing endpoints]
- Model Validation: Use DataAnnotations or FluentValidation

## Edge Cases

- Request with missing required fields → Return 400 with validation errors
- Request with invalid data types → Return 400 with type error
- User not authenticated → Return 401
- User lacks permission → Return 403
- Resource not found → Return 404
- Database unavailable → Return 500, log error, don't expose internals
- [Add more edge cases specific to your endpoint]

## Dependencies

- Authentication: Existing JWT middleware (Microsoft.AspNetCore.Authentication.JwtBearer)
- Database: [TableName] table must exist
- External Services: [List any external APIs this depends on]
- NuGet Packages:
  - Entity Framework Core (if database access)
  - FluentValidation.AspNetCore (if using FluentValidation)
  - AutoMapper (if using DTO mapping)

## Additional Context

Related Endpoints:

GET /api/[resource] - [Description]
POST /api/[resource] - [Description]

Database Schema (if creating/modifying):

**SQL Schema**:
```sql
CREATE TABLE [TableName] (
  Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
  Field1 NVARCHAR(255) NOT NULL,
  Field2 INT,
  CreatedAt DATETIME2 DEFAULT GETDATE()
);
```

**C# Entity Model**:
```csharp
public class [Resource]
{
    public Guid Id { get; set; }
    public string Field1 { get; set; }
    public int Field2 { get; set; }
    public DateTime CreatedAt { get; set; }
}
```

**Controller Example**:
```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize] // If authentication required
public class [Resource]Controller : ControllerBase
{
    private readonly I[Resource]Service _service;
    private readonly ILogger<[Resource]Controller> _logger;

    public [Resource]Controller(I[Resource]Service service, ILogger<[Resource]Controller> logger)
    {
        _service = service;
        _logger = logger;
    }

    [HttpPost("{id}/[action]")]
    [ProducesResponseType(typeof([Resource]Response), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<[Resource]Response>> [Action](Guid id, [FromBody] [Resource]Request request)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        try
        {
            var result = await _service.[Action]Async(id, request);
            return Ok(new [Resource]Response { Success = true, Data = result });
        }
        catch (NotFoundException ex)
        {
            return NotFound(new { Success = false, Error = ex.Message });
        }
        catch (ValidationException ex)
        {
            return BadRequest(new { Success = false, Error = ex.Message });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in [Action] for {Id}", id);
            return StatusCode(500, new { Success = false, Error = "Internal server error" });
        }
    }
}
```

Security Considerations:

- [Data sanitization needed?] - Use DataAnnotations validation
- [PII/sensitive data involved?] - Apply data protection if needed
- [SQL injection prevention?] - Use parameterized queries (EF Core handles this)

## Clarifications

[Leave empty - agent will populate]
