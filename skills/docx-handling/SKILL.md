---
name: docx-handling
description: Create, read, and edit Word (.docx) documents. Use when a task involves a .docx file as input or output.
compatibility: Requires Python 3 with python-docx; pandoc optional. Installing them needs network access.
---

# DOCX handling

## Purpose

Read, create, and modify `.docx` files without losing formatting. Use `python-docx` for structured edits and `pandoc` for fast text extraction or conversion.

## When to use

- The user shares a `.docx` file or asks for one as output
- "Summarize this Word doc", "fill in this template", "convert this to Word"
- Find-and-replace, adding tables, or updating headings in an existing document

## When not to use

- `.doc` (legacy binary) files: convert first with `soffice --headless --convert-to docx file.doc`
- Google Docs, PDFs, or spreadsheets
- The user only wants plain text or Markdown output and never mentions Word

## Setup

```bash
pip install python-docx
# optional, for conversion/extraction
apt-get install -y pandoc   # or: brew install pandoc
```

## Steps

### Reading

1. For a quick text dump, run `pandoc input.docx -t markdown -o input.md`. This keeps headings, lists, and tables.
2. For structured access, walk the document in `python-docx`:

   ```python
   from docx import Document
   doc = Document("input.docx")
   for p in doc.paragraphs:
       print(p.style.name, "|", p.text)
   for table in doc.tables:
       for row in table.rows:
           print([cell.text for cell in row.cells])
   ```

### Creating

1. Start from a template (`Document("template.docx")`) when the output must match a house style. Otherwise start from `Document()`.
2. Use built-in styles (`Heading 1`, `List Bullet`, `Table Grid`) rather than manual font changes, so the document stays consistent and editable.
3. Save under a new filename. Never overwrite the user's original unless they asked you to.

```python
from docx import Document
from docx.shared import Pt

doc = Document()
doc.add_heading("Quarterly Report", level=1)
doc.add_paragraph("Revenue grew 12% quarter over quarter.")
doc.add_paragraph("New customers: 48", style="List Bullet")

table = doc.add_table(rows=1, cols=2, style="Table Grid")
table.rows[0].cells[0].text, table.rows[0].cells[1].text = "Region", "Revenue"
for region, revenue in [("North", "$1.2M"), ("South", "$0.9M")]:
    row = table.add_row().cells
    row[0].text, row[1].text = region, revenue

doc.save("report.docx")
```

### Editing

1. **Find and replace:** Word splits text into *runs*, so `{{NAME}}` may span several runs. Replace at the paragraph level, then rewrite the runs:

   ```python
   def replace_in_paragraph(p, old, new):
       if old not in p.text:
           return
       text = p.text.replace(old, new)
       for run in p.runs[1:]:
           run.text = ""
       p.runs[0].text = text  # keeps the first run's formatting
   ```

   Apply it to `doc.paragraphs` *and* to every cell paragraph in `doc.tables`, plus headers and footers (`doc.sections[i].header.paragraphs`).
2. **Verify** by re-reading the saved file (step 1 of Reading) and confirming each change landed.

## Pitfalls

| Issue | Fix |
|---|---|
| Placeholder not replaced | It spans runs. Use paragraph-level replace (above). |
| Formatting lost after edit | You assigned `p.text = ...`, which drops runs. Edit `p.runs` instead. |
| Images/charts missing in text dump | Expected: `pandoc` extracts text only. Use `--extract-media=./media` to pull images. |
| Tracked changes ignored | `python-docx` doesn't expose them. Accept or reject them in Word first, or parse `word/document.xml` directly. |

## Examples

### Example 1

**Input:** "Fill in `offer_template.docx` with name Jane Doe and start date March 3."

**Output:** Load the template, replace `{{NAME}}` and `{{START_DATE}}` in body, tables, and headers, then save as `offer_jane_doe.docx`. Re-read the file to confirm neither placeholder is left.
