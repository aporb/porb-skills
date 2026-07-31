# Toolkit Export & Sanitisation Workflow

When the request is to **export a completed compliance toolkit for SharePoint/corporate distribution** — creating a clean copy with personal names stripped to role titles — use this workflow.

## When To Use

- User wants a "clean export" or "sanitised version" of an existing CMMC L2 toolkit
- Output is going to a SharePoint site, shared drive, or other broad-distribution channel
- Source toolkit contains personal names that should be replaced with role titles
- C3PAO mock assessment files (personae, gap reports, gap summaries) should be excluded

## Workflow

### 1. Explore Source Structure

First, understand what exists at the top level:

```
ls -la <source-toolkit>/
find <source-toolkit>/ -type d | sort
```

Then get a complete file inventory:

```
find <source-toolkit>/ -type f | sort
```

### 2. Plan the Structure

The target export structure depends on what exists:

```
target-toolkit/
├── README.md               # SharePoint landing page
├── templates/              # All template files (names stripped)
├── sops/                   # If exists in source (skip if absent)
└── reference-docs/         # Clean reference materials (if any)
```

**DO NOT include:** C3PAO mock assessment files (personae, gap reports, gap summaries, unified summaries).

### 3. Check for Personal Names

Search all template files for the people listed in the user's instructions:

```
grep -rn "Enzo Zoratto\|Brian Gregorio\|Amyn Porbanderwala\|Douglas Henderson\|Olivia Baer\|Joe Smith\|Ryan Aragon\|Eric Atkinson\|Kelly Parr" <source>/templates/
```

Also check for first-name-only references (e.g., "Brian," "Enzo," "Olivia") in training materials, phishing scenarios, and role assignment tables:

```
grep -rn "Enzo\|Brian\|Amyn\|Douglas\|Olivia\|Joe\b" <source>/templates/
```

### 4. Copy and Sanitise

Copy the source templates and reference docs to the target directory, then batch-replace names with `sed`:

```
mkdir -p target/templates target/reference-docs
cp <source>/templates/* target/templates/
cp -r <source>/reference-docs/* target/reference-docs/  # if exists
```

**Batch replacement strategy (prefer `sed -i` with full names):**

```
cd target/templates

# Enzo Zoratto (multiple forms)
sed -i 's/Enzo Zoratto, Head of Federal Business Unit/FBU Head (Head of Federal Business Unit)/g' *.md *.csv 2>/dev/null
sed -i 's/Enzo Zoratto/FBU Head/g' *.md *.csv 2>/dev/null

# Brian Gregorio (may also appear as standalone "Brian")
sed -i 's/Brian Gregorio/Compliance Director/g' *.md *.csv 2>/dev/null

# Amyn Porbanderwala (occurs in many forms with titles)
sed -i 's/Amyn Porbanderwala, FCICS \/ Enclave Lead/Chief Information Compliance Specialist (CICS), Enclave Lead/g' *.md *.csv 2>/dev/null
sed -i 's/Amyn Porbanderwala, FCICS/Chief Information Compliance Specialist (CICS)/g' *.md *.csv 2>/dev/null
sed -i 's/Amyn Porbanderwala (CICS)/Chief Information Compliance Specialist (CICS)/g' *.md *.csv 2>/dev/null
sed -i 's/Amyn Porbanderwala/Chief Information Compliance Specialist (CICS)/g' *.md *.csv 2>/dev/null

# Douglas Henderson
sed -i 's/Douglas Henderson/Director of Operations/g' *.md *.csv 2>/dev/null

# Olivia Baer (multiple forms)
sed -i 's/Olivia Baer, GCC High Administrator/GCC High Administrator/g' *.md *.csv 2>/dev/null
sed -i 's/Olivia Baer, GCC High Admin/GCC High Administrator/g' *.md *.csv 2>/dev/null
sed -i 's/Olivia Baer/Sr Cybersecurity Analyst/g' *.md *.csv 2>/dev/null

# Joe Smith
sed -i 's/Joe Smith, IT Engineer/IT Support Specialist/g' *.md *.csv 2>/dev/null
sed -i 's/Joe Smith/IT Support Specialist/g' *.md *.csv 2>/dev/null

# Ryan Aragon (if present)
sed -i 's/Ryan Aragon/Business Development Director/g' *.md *.csv 2>/dev/null
```

For first-name-only references in training/tabletop content, use targeted patches:

```
sed -i 's/from Brian, Enzo, Douglas/from Compliance Director, FBU Head, Director of Operations/g' Security-Awareness-Training-Curriculum.md
```

**Check for any "Sam" or other non-list names:**

```
grep -rn "\bSam\b" *.md *.csv 2>/dev/null
```

### 5. Verify Thoroughly

After sed replacements, run a comprehensive verification:

```
cd target/templates
for pattern in "Enzo" "Zoratto" "Brian" "Gregorio" "Amyn" "Porbanderwala" "Douglas" "Henderson" "Olivia" "Baer" "Joe Smith" "Ryan" "Aragon" "Eric Atkinson" "Kelly Parr"; do
  results=$(grep -rnil "$pattern" . 2>/dev/null)
  if [ -n "$results" ]; then
    echo "STILL FOUND '$pattern' in: $results"
  fi
done
```

### 6. Write the README

The README.md is the **SharePoint landing page**. Structure:

- Purpose & Scope — why the toolkit exists, scope table
- How to Use — separate guidance per audience (Compliance Leads, IT, Executives)
- Quick Reference — CMMC Phase 2 timeline table (Phase 1: now, Phase 2: Nov 2026, Phase 3: TBD)
- Document Index — table of all templates with descriptions and owner roles
- Role-Based Naming Convention — mapping table + "populate before formal submission" warning
- Directory Structure — ASCII tree
- Next Steps — checklists for 30-day, 60-90 day, and pre-assessment milestones
- Version History

### 7. Final Sanity Check

```
echo "Total files: $(find target/ -type f | wc -l)"
echo "  Templates (.md): $(ls target/templates/*.md 2>/dev/null | wc -l)"
echo "  Templates (.csv): $(ls target/templates/*.csv 2>/dev/null | wc -l)"
echo "  Reference docs:   $(find target/reference-docs/ -type f | wc -l)"
du -sh target/
```

## Name-to-Role Mapping Reference

| Original Name | Role Title |
|---------------|------------|
| Enzo Zoratto | FBU Head / Federal Business Unit Director |
| Brian Gregorio | Compliance Director / Senior Director of Compliance |
| Amyn Porbanderwala | Chief Information Compliance Specialist (CICS) |
| Douglas Henderson | Director of Operations |
| Olivia Baer | Sr Cybersecurity Analyst / GCC High Administrator |
| Joe Smith | IT Support Specialist / Field Operations Specialist |
| Ryan Aragon | Business Development Director |
| Eric Atkinson | [role title — report to Compliance Director] |
| Kelly Parr | [role title — report to Compliance Director] |
| Sam (SVP) | SVP, Senior Vice President |

## Pitfalls

### sed Order Matters

Replace longer strings first (with titles appended), then shorter strings. If you do `Amyn Porbanderwala → CICS` BEFORE `Amyn Porbanderwala, FCICS → CICS, Enclave Lead`, the longer form is already gone and you lose the title information. Strategy: most-specific → least-specific.

### sed `g` Flag Across Mixed File Types

Using `sed -i 's/.../.../g' *.md *.csv` works but if one glob matches nothing, sed errors. Append `2>/dev/null` to suppress.

### First-Name-Only References in Training Content

Names like "Enzo," "Brian," "Olivia" appear standalone in phishing scenarios and training curriculum. Read the exact line before replacing — these need targeted patches, not broad sed.

### Check for Names Outside the Known List

After replacing the known names, scan for any other `[First Last]` patterns. Use grep for two-capitalized-word patterns and filter non-person matches (Microsoft, Azure, NIST, role names, locations, months).

### Reference Docs Are Usually Clean

Government PDFs and DFARS clause extracts in reference-docs/ should NOT be scrubbed. Verify with grep but don't sed them.

### CSV Files Have Fragile Formatting

CSV files with quoted strings containing commas can break if sed modifies partial content. Stick to full-name replacements which are unambiguous.

### README Landing Page Can Re-Introduce Names

The agent writing the README.md may pull personal names from context even though all template files have been scrubbed. **Always run the name verification pass AFTER the README is written**, not just after template copying. In the July 2026 Aecon export, the README had all 6 personal names while every template was clean.

### Do NOT Modify Source Files

Always work on copied files in the target directory. Verify source still has names and target doesn't after replacement.
