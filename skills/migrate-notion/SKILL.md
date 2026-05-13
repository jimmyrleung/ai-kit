---
name: migrate-notion
description: Guide a Notion-to-Obsidian migration using the Notion MCP tool. Covers content migration, image handling, and vault structure conventions.
argument-hint: "[notion-page-url] [target-vault-path]"
---

# Notion to Obsidian Migration Guide

You are guiding a migration of Notion pages into an Obsidian vault. Follow this approach strictly.

## Arguments

- `$0` - The Notion page URL (or ID) to migrate
- `$1` - The target Obsidian vault path (directory where migrated files should go)

If arguments are missing, ask the user for them before proceeding.

## Pre-migration: Understand the source

1. **Fetch the root Notion page** using `notion-fetch` with the provided URL
2. **Map the page tree**: identify all child pages, sub-child pages, and their hierarchy
3. **Identify page types**: categorize each page as:
   - **Parent page** (has child pages) - these become folders with a `Notes.md`
   - **Standalone page** (no children) - still gets its own folder with `Notes.md`
   - **Child page** (belongs to a parent) - becomes a `.md` file inside the parent's folder
   - **Meta/process pages** (e.g., "[Claude] Studying approach") - flag for user to decide skip/include
4. **Present the migration plan** to the user as a table: page name, has sub-pages, proposed action
5. **Get user confirmation** before proceeding

## Phase 1: Migrate content (text first, images later)

Migrate ALL text content before touching any images. This is critical because Notion image URLs are S3 presigned URLs that expire quickly (typically within 1 hour).

### Folder structure convention

```
<target-vault-path>/
  <Topic Name>/
    Notes.md              <- Main content from the Notion parent page
    <Child page>.md       <- Each child page as its own file
    assets/               <- Images (created in Phase 2)
```

- **Parent pages become `Notes.md`** - never repeat the folder name as the filename (use `Notes.md`, not `<Topic Name>.md`)
- **Each child page becomes its own `.md` file** named after the child page title
- **Deeply nested sub-pages** (children of children) should be merged inline into their parent file unless they are substantial enough to warrant their own file - ask the user if unclear

### Content formatting rules

For every `.md` file:

1. **H1 heading**: start with `# <Page Title>` matching the Notion page title
2. **Standard Obsidian markdown**: no Notion-specific formatting
3. **Clean up Notion artifacts**:
   - Remove `<empty-block/>` tags
   - Remove escaped brackets `\[` and `\]` (unless inside code blocks)
   - Remove any Notion URLs or Notion-specific HTML tags
4. **Notion toggle blocks** -> Obsidian collapsible callouts:
   ```markdown
   > [!info]- Toggle title here
   > Collapsed content goes here
   ```
   Use the callout type that best matches the content: `[!info]`, `[!note]`, `[!tip]`, `[!example]`, `[!warning]`, etc.
   Do NOT use raw HTML `<details><summary>` tags.
5. **Image placeholders**: while migrating content, convert Notion image references to local asset paths:
   ```markdown
   ![Descriptive alt text](assets/descriptive-filename.png)
   ```
   Use descriptive kebab-case filenames (e.g., `cap-theorem-partition-example.png`, not `image.png`)
6. **Child page links**: at the bottom of every `Notes.md` that has child pages, add:
   ```markdown
   ## Child pages

   - [[Child page name]]
   - [[Another child page]]
   ```
   Wiki-links MUST match the exact filename (without `.md` extension)

### Migration order

- Migrate parent pages before their children
- For each page: fetch from Notion, create the `.md` file, move to the next page
- Do NOT download images during this phase

## Phase 2: Migrate images

After ALL content is migrated, handle images. The strategy is to minimize time between fetching a Notion page (which generates fresh S3 presigned URLs) and downloading the images.

### Per-topic image migration

For each topic folder that has image references:

1. **Re-fetch the Notion page(s)** that contained images - this generates fresh presigned URLs
2. **Immediately download** all images from that page using `curl -sL -o <filename> <url>`
3. **Verify each download**:
   - Check file size is reasonable (most diagram PNGs are 10KB-100KB)
   - If a file is suspiciously small (< 2KB), check if it's an XML error response: `file <filename>` should say "PNG image data", not "XML"
   - If download failed (expired token), re-fetch the Notion page and retry immediately
4. Save images to the `assets/` subfolder within the topic directory

### Batch strategy

- Process one topic at a time (fetch page -> download all its images -> verify -> next topic)
- Do NOT fetch all pages first and then try downloading - the URLs will expire
- If a topic has images spread across multiple Notion sub-pages, fetch and download each sub-page's images before moving to the next

## Phase 3: Verify

After migration is complete, run a verification pass:

1. **Image reference check**: grep all `![` references in `.md` files and cross-reference against actual files in `assets/` directories. Flag any mismatches.
2. **Wiki-link check**: verify all `[[wiki-links]]` in `Notes.md` files point to files that actually exist in the same folder
3. **Notion artifact scan**: search for leftover `<empty-block/>`, `notion.so` URLs, or escaped brackets
4. **Empty assets directories**: flag any `assets/` folders that exist but are empty
5. **File size sanity**: flag any image files under 2KB (likely failed downloads)

Present the verification results to the user as a checklist.

## Important lessons learned

- **S3 presigned URLs expire fast**: the #1 cause of failed image downloads. Always re-fetch the Notion page right before downloading its images.
- **Wiki-links are exact-match**: `[[My Page]]` will NOT resolve to a file named `My page.md` (case matters) or a folder named `My Page/` (it must be a file)
- **Verify image downloads immediately**: a 1KB "PNG" that's actually an XML S3 error is easy to miss
- **Content curation is the user's job**: migrate everything faithfully first. The user decides what to keep, restructure, or delete after migration.
