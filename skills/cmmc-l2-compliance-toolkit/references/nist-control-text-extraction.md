# NIST SP 800-171 Control Text Extraction

The skill's original extraction script (`scripts/nist-controls-extraction.py`) produces TRUNCATED control text because it extracts only the first sentence of each control from the PDF table of contents, not the full control text body.

## The Correct Approach

Use `pdftotext -raw` mode (not `-layout`) and parse with a DISCUSSION-header stop condition:

```python
import subprocess, json, re

PDF_PATH = "/path/to/NIST-SP-800-171-Rev2.pdf"
proc = subprocess.run(["pdftotext", "-raw", PDF_PATH, "-"], capture_output=True, text=True)
text = proc.stdout

controls = {}
lines = text.split("\n")
cid = None
ctext = []

for line in lines:
    s = line.strip()
    m = re.match(r"^(\d+\.\d+\.\d+)\s+(.*)", s)
    if m:
        if cid:
            controls[cid] = " ".join(ctext).strip()
        cid = m.group(1)
        ctext = [m.group(2).strip()]
    elif cid:
        if s == "DISCUSSION" or s.startswith("DISCUSSION"):
            controls[cid] = " ".join(ctext).strip()
            cid = None
            ctext = []
        elif not re.match(r"^\d+\.\d+\s", s):
            ctext.append(s)

if cid and ctext:
    controls[cid] = " ".join(ctext).strip()

print(f"Extracted {len(controls)} controls")
```

## Why This Works

- `pdftotext -raw` outputs text in reading order instead of preserving layout columns. This gives full sentences instead of word-wrapped fragments.
- The NIST PDF uses `DISCUSSION` as a section header after each control's full text. Stopping at `DISCUSSION` (rather than the next control ID) captures the complete requirement statement, including trailing phrases like "devices (including other systems)" or "permitted to execute".
- The `-layout` mode (used by the original script) preserves column positions, but NIST's two-column layout causes text to be read across the page boundary, truncating each control's text mid-sentence.

## Verification

After extraction, spot-check the first few controls:

```python
for cid in ["3.1.1", "3.1.2", "3.1.3"]:
    if cid in controls:
        print(f"{cid}: {controls[cid]}")
```

Expected output:
```
3.1.1: Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).
3.1.2: Limit system access to the types of transactions and functions that authorized users are permitted to execute.
3.1.3: Control the flow of CUI in accordance with approved authorizations.
```

## Integration with Control Matrix

After extraction, use the full control texts to rebuild the CSV:

```python
import csv

# Read existing matrix
with open("Control-Implementation-Matrix.csv") as f:
    reader = csv.DictReader(f)
    rows = [r for r in reader]

# Apply full text from extracted controls
for r in rows:
    full = controls.get(r["Control_ID"])
    if full:
        r["Control_Text"] = full

# Write back
with open("Control-Implementation-Matrix.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
```

## Important

This extraction also picks up RELATED and parenthetical notes (like "AC-2 Account Management") that follow the control text in the PDF but appear after DISCUSSION on the same paragraph boundary. These are harmless but make the control text slightly longer than the official NIST text. They can be trimmed, but for CMMC compliance purposes the complete extracted text is sufficient — the C3PAO cares that the requirement is captured, not that it matches the official text verbatim.
