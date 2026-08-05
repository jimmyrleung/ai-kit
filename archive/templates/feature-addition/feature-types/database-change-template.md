# Feature: [Database Change Description]

> **Feature Type**: Database Schema Change
> **Instructions**: This template is pre-filled for database modifications. Customize the bracketed sections.

## Definition

Modify the database schema to [add/modify/remove] [table/column/index/constraint] in order to [support what feature or fix what issue].

**Impact**: [Describe what features/functionality this enables or improves]

---

## Relevant Files/Flows

- `Migrations/` - EF Core migration files
- `Models/[ModelName].cs` - Entity model files
- `Data/ApplicationDbContext.cs` - DbContext configuration
- `Services/[Service].cs` - Services that interact with this data
- Database: `[DatabaseName]`
- Table(s): `[TableName(s)]`

---

## Expected Output

**Current Schema**:

```sql
-- Current table structure
CREATE TABLE [TableName] (
  Id UNIQUEIDENTIFIER PRIMARY KEY,
  ExistingColumn1 NVARCHAR(255),
  ExistingColumn2 INT
);
```

**Future Schema:**

```sql
-- Updated table structure
CREATE TABLE [TableName] (
  Id UNIQUEIDENTIFIER PRIMARY KEY,
  ExistingColumn1 NVARCHAR(255),
  ExistingColumn2 INT,
  NewColumn NVARCHAR(100) NOT NULL DEFAULT 'default_value'
);
```

Changes:

- ✅ Add: NewColumn
- ❌ Remove: [none / ColumnName]
- 🔄 Modify: [none / ColumnName from X to Y]

## Acceptance Criteria

- [ ] Migration file created with up and down methods
- [ ] Migration runs successfully in development
- [ ] Migration runs successfully in staging
- [ ] Existing data is preserved or properly transformed
- [ ] New constraints/validations work correctly
- [ ] ORM models updated to reflect schema changes
- [ ] Indexes added for performance (if needed)
- [ ] Foreign keys maintain referential integrity
- [ ] Migration is reversible (down migration works)
- [ ] No data loss during migration

## Migration Details

### Migration Type

- [ ] Add table
- [ ] Drop table
- [ ] Add column(s)
- [ ] Drop column(s)
- [ ] Modify column(s)
- [ ] Add index
- [ ] Drop index
- [ ] Add constraint
- [ ] Data transformation

Migration Script
File: `Migrations/[timestamp]_[Description].cs`

```csharp
public partial class [Description] : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        // Add column
        migrationBuilder.AddColumn<string>(
            name: "[ColumnName]",
            table: "[TableName]",
            type: "nvarchar(100)",
            maxLength: 100,
            nullable: false,
            defaultValue: "default_value");

        // Add index if needed
        migrationBuilder.CreateIndex(
            name: "IX_[TableName]_[ColumnName]",
            table: "[TableName]",
            column: "[ColumnName]");

        // Data transformation if needed
        migrationBuilder.Sql(@"
            UPDATE [TableName]
            SET [NewColumn] = [calculation/default]
            WHERE [condition]
        ");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        // Drop index
        migrationBuilder.DropIndex(
            name: "IX_[TableName]_[ColumnName]",
            table: "[TableName]");

        // Drop column
        migrationBuilder.DropColumn(
            name: "[ColumnName]",
            table: "[TableName]");
    }
}
```

### Data Transformation Required?

Is data transformation needed?: [Yes/No]
If yes:

```csharp
// In the migration Up method:
migrationBuilder.Sql(@"
    UPDATE [TableName]
    SET NewColumn = CASE
        WHEN ExistingColumn = 'value1' THEN 'new_value1'
        WHEN ExistingColumn = 'value2' THEN 'new_value2'
        ELSE 'default_value'
    END
");
```

Estimated rows affected: [X rows]
Estimated transformation time: [X seconds/minutes]

## Constraints

- Zero Downtime: Migration must not require application downtime
- Data Preservation: All existing data must be preserved
- Performance: Migration should complete in < [X] minutes on production
- Backwards Compatibility: [Application should work before/during/after migration]
- Transaction Safety: Migration should be wrapped in transaction (if DB supports it)

## Edge Cases

- Table has millions of rows → Migration might be slow, consider batching
- Production has different data than staging → Test with production-like data
- Concurrent writes during migration → Ensure migration locks appropriately
- Migration fails halfway → Ensure transaction rollback works
- Column being added is NOT NULL → Provide default value or backfill first
  [Add more edge cases specific to your change]

## Dependencies

- Database System: [SQL Server, PostgreSQL, MySQL, SQLite - version]
- Migration Tool: Entity Framework Core Migrations
- ORM: Entity Framework Core [version 6.0/7.0/8.0]
- Related Tables: [List tables with foreign key relationships]

## Performance Considerations

Before Migration:

- Current table size: [X rows, Y GB]
- Current query performance: [Acceptable/Slow]
- Existing indexes: [List relevant indexes]

After Migration:

- Expected table size: [X rows, Y GB]
- New indexes needed: [Yes/No - list them]
- Expected query performance: [Impact analysis]

Migration Execution Time:

- Small table (<1K rows): Instant
- Medium table (1K-100K rows): [X] seconds
- Large table (>100K rows): [X] minutes - Consider running during low-traffic period

## Backwards Compatibility Strategy

During Migration (application must work):

- [ ] Application can run with or without new column
- [ ] New code handles both old and new schema
- [ ] Use feature flags if needed

Multi-Step Migration (for breaking changes):

1. Step 1: Add new column (nullable, with default)
2. Step 2: Backfill data, deploy new application code
3. Step 3: Make column NOT NULL, remove old column (if applicable)

## Rollback Plan

How to rollback:

```bash
# Revert to previous migration
dotnet ef database update [PreviousMigrationName]

# Or remove the last migration (if not applied to production)
dotnet ef migrations remove
```

Verify data integrity after rollback
Ensure application works with reverted schema

Rollback Safety:

- [ ] Down migration tested in development
- [ ] Down migration tested in staging
- [ ] Data loss acceptable if rollback needed? [Yes/No - explain]

If data loss is NOT acceptable:

```bash
# SQL Server backup
BACKUP DATABASE [DatabaseName] TO DISK = 'C:\Backups\backup.bak'

# Or use your cloud provider's backup tool
```

- Keep backup for [X] days after successful migration

## Testing Strategy

Pre-Migration Testing:

- [ ] Test migration on copy of production data
- [ ] Measure migration execution time
- [ ] Test application with new schema
- [ ] Test rollback procedure

Post-Migration Verification:

- [ ] Verify all data present and correct
- [ ] Verify indexes created successfully
- [ ] Verify application functions correctly
- [ ] Run performance tests
- [ ] Check database logs for errors

## Deployment Plan

Preparation:

1. Backup production database
2. Notify team of maintenance window (if downtime needed)
3. Have rollback plan ready

Execution:

```bash
# 1. Deploy migration to staging → Verify
dotnet ef database update --connection "StagingConnectionString"

# 2. Run migration on production during [low-traffic period]
dotnet ef database update --connection "ProductionConnectionString"

# Or migrations run automatically on app startup if configured
```

3. Monitor for errors
4. Deploy updated application code
5. Monitor application and database performance

Post-Deployment:

1. Verify data integrity
2. Monitor query performance
3. Remove backup after [X] days

## Estimated Impact

Downtime Required: [None / X minutes]
User Impact:

- [None - transparent to users]
- [Users may experience slow responses during migration]
- [Feature will be unavailable during migration]

Database Load:

- [Minimal - simple column addition]
- [Moderate - requires index creation]
- [High - large data transformation]

## Additional Context

Why is this change needed?: [Business justification]
Alternatives considered: [Other approaches and why this one was chosen]
Related tickets: [JIRA-123, etc.]

## Clarifications

[Leave empty - agent will populate]
