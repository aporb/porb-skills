---
name: contact-extractor
description: Extract contact information from HTML briefings and documents, then generate iPhone-compatible vCard (.vcf) files.
version: 1.0.0
tags: [contacts, vcard, html, briefing, extraction, iphone, ios]
tier: A
related_skills: [research-briefing, strategic-research, zoho-mail]
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---

# Contact Extractor and vCard Generator

Extract contact information from HTML briefings, markdown documents, and other sources, then generate iPhone-compatible vCard (.vcf) files.

## When to Use

- User asks to "extract contacts" from any HTML or markdown briefing
- User requests "contact cards" for people referenced in a document
- User wants vCard files to import into iPhone/Android contacts
- User says "send me the contacts" after viewing a briefing

## Supported Sources

- **HTML briefings** (HARBOR-style, dark-themed briefings in `~/Documents/Briefings/`)
- **Markdown files** (Obsidian vault notes, README files, documentation)
- **LinkedIn exports** (profile data in HTML or CSV format)
- **Email threads** (signatures, headers, quoted text)
- **Manual input** (user provides contact details in free text)

## vCard Format (iPhone Compatible)

Generate `.vcf` files using vCard 3.0 standard (widest iOS compatibility). Required fields:

- `FN` - Full Name (display name)
- `N` - Structured Name (Family Name;Given Name;Additional Names;Honorific Prefixes;Honorific Suffixes)
- `TEL;TYPE=CELL` or `TEL;TYPE=WORK` - Phone numbers
- `EMAIL;TYPE=WORK` or `EMAIL;TYPE=HOME` - Email addresses
- `TITLE` - Job title
- `ORG` - Organization/Company
- `NOTE` - Context, relationship, or meeting notes

## Workflow

1. **Locate the source file**
   - If user provides a path, read directly
   - If user mentions an email subject line, search Briefings folder by date/content
   - If ambiguous, ask the user to specify: path, subject line, or date

2. **Extract contact information**
   - Parse HTML: look for `<h2>`, `<h3>` heading patterns with names + titles
   - Parse markdown: look for `##`, `###` headers with contact patterns
   - Look for contact section patterns:
     - "Key Contacts", "People", "Team", "Stakeholders"
     - `<table>` rows with name/title/email/phone
     - `<ul>` lists with contact details
   - Extract structured data per person:
     - Full name, honorifics
     - Job title, role
     - Company, organization
     - Email address(es)
     - Phone number(s)
     - LinkedIn URL (map to `X-SOCIALPROFILE` field)
     - Context notes (relationship, meeting date, relevant details)

3. **Generate vCard files**
   - Create one `.vcf` file per person
   - Filename format: `firstname-lastname-YYYY-MM-DD.vcf` (date = source document date)
   - Use vCard 3.0 format for iOS compatibility
   - Include all available fields
   - Add `NOTE` field with source context

4. **Deliver to user**
   - If Discord: Send each .vcf file as attachment (use MEDIA:/path syntax)
   - Provide summary of contacts extracted
   - Note: "Open each file on iPhone to auto-import to Contacts"

5. **Post-processing**
   - Verify files exist at specified paths
   - Ensure proper ownership/permissions (run `chown $USER:staff + chmod 644` if running in sandbox)

## Pitfalls

- **Ambiguous source file:** User says "the HTML file" or "the briefing" without specifying path or subject. Don't guess — ask for clarification (path, subject line, or date).

- **HTML briefing not found at Briefings folder:** Briefings may live in other locations (e.g., `~/Documents/_Projects/2026_books/_personal/job-applications/aecon/`). Search recursively with `find` or ask user for specific path.

- **vCard format errors:** Some vCard parsers are strict. Test format with:
  - Only use vCard 3.0 (not 4.0) for iOS compatibility
  - Escape special characters in values (backslashes, commas, semicolons)
  - Ensure each vCard ends with `END:VCARD` followed by blank line

- **Missing email/phone:** vCard without contact info still imports but is less useful. Generate anyway, but note in summary which contacts have incomplete data.

- **Multiple contacts in one file:** Don't bundle multiple vCards in one `.vcf` file. Generate separate files per person for easier iPhone import.

## Example vCard Template

```vcf
BEGIN:VCARD
VERSION:3.0
FN:John Smith
N:Smith;John;;;
TITLE:VP Business Development
ORG:Aecon Federal
EMAIL;TYPE=WORK:john.smith@aeconfederal.com
TEL;TYPE=WORK:+1-704-555-0100
TEL;TYPE=CELL:+1-704-555-0101
X-SOCIALPROFILE;TYPE=linkedin:https://www.linkedin.com/in/johnsmith
NOTE:HARBOR briefing 2026-06-29 - Key stakeholder for FCS overlay
END:VCARD
```

## Tool Patterns

Use `write_file` to create .vcf files. Example:
```python
vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{full_name}
N:{last_name};{first_name};;;
TITLE:{title}
ORG:{company}
EMAIL;TYPE=WORK:{email}
TEL;TYPE=WORK:{phone}
NOTE:{context}
END:VCARD
"""

write_file(path=f"/tmp/contacts/{filename}.vcf", content=vcard_content)
```

Use `read_file` with offset/limit to parse large HTML files in chunks if needed.

## Related Skills

- `research-briefing` - Generates HTML briefings that may contain contact information
- `strategic-research` - Produces people/company briefings with contact details
- `zoho-mail` - May be needed to locate email sources when briefings are not found