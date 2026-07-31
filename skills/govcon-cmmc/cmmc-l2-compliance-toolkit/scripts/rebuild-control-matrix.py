#!/usr/bin/env python3
"""
Rebuild Control-Implementation-Matrix.csv with full NIST 800-171 Rev 2 control text.

Extracts complete control text from the PDF using pdftotext -raw with a
DISCUSSION-header stop condition, then rebuilds the CSV. Optionally applies
client-specific implementation examples from a dict.

Usage:
    python3 scripts/rebuild-control-matrix.py [--pdf-path PATH] [--matrix-path PATH]

Defaults:
    --pdf-path:   reference-docs/NIST-SP-800-171-Rev2.pdf (relative to toolkit root)
    --matrix-path: templates/Control-Implementation-Matrix.csv
"""

import subprocess
import re
import csv
import sys
import os
import argparse


def extract_controls_from_pdf(pdf_path):
    """Extract full control text from NIST SP 800-171 Rev 2 PDF."""
    proc = subprocess.run(
        ["pdftotext", "-raw", pdf_path, "-"],
        capture_output=True, text=True
    )
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

    return controls


FAMILIES = {
    "3.1": "AC - Access Control",
    "3.2": "AT - Awareness and Training",
    "3.3": "AU - Audit and Accountability",
    "3.4": "CM - Configuration Management",
    "3.5": "IA - Identification and Authentication",
    "3.6": "IR - Incident Response",
    "3.7": "MA - Maintenance",
    "3.8": "MP - Media Protection",
    "3.9": "PS - Personnel Security",
    "3.10": "PE - Physical Protection",
    "3.11": "RA - Risk Assessment",
    "3.12": "CA - Security Assessment",
    "3.13": "SC - System and Communications Protection",
    "3.14": "SI - System and Information Integrity",
}


def rebuild_matrix(pdf_path, matrix_path, client_examples=None):
    """Rebuild the Control Implementation Matrix CSV with full control text."""

    controls = extract_controls_from_pdf(pdf_path)
    print(f"Extracted {len(controls)} controls from PDF")

    # Read existing CSV to preserve status/role/evidence columns
    existing_rows = []
    if os.path.exists(matrix_path):
        with open(matrix_path) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for r in reader:
                existing_rows.append(r)
    else:
        fieldnames = [
            "Control_ID", "Control_Family", "Control_Text",
            "Implementation_Status", "Responsible_Role",
            "Implementation_Description", "Evidence_Artifact",
            "Last_Assessed_Date", "Next_Assessment_Date"
        ]

    print(f"Existing rows: {len(existing_rows)}")

    # Rebuild
    new_rows = []
    for r in existing_rows:
        cid = r.get("Control_ID", "")
        family_key = ".".join(cid.split(".")[:2])
        full_text = controls.get(cid, r.get("Control_Text", ""))

        # Apply client-specific example if provided
        impl_desc = r.get("Implementation_Description", "See SOP.")
        if client_examples and cid in client_examples:
            impl_desc = client_examples[cid]

        nr = {
            "Control_ID": cid,
            "Control_Family": FAMILIES.get(family_key, r.get("Control_Family", "")),
            "Control_Text": full_text,
            "Implementation_Status": r.get("Implementation_Status", "Planned"),
            "Responsible_Role": r.get("Responsible_Role", "TBD"),
            "Implementation_Description": impl_desc,
            "Evidence_Artifact": r.get("Evidence_Artifact", ""),
            "Last_Assessed_Date": r.get("Last_Assessed_Date", ""),
            "Next_Assessment_Date": r.get("Next_Assessment_Date", ""),
        }
        new_rows.append(nr)

    # Write
    with open(matrix_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(new_rows)

    print(f"Written {len(new_rows)} rows to {matrix_path}")

    # Verify
    for cid in ["3.1.1", "3.1.2", "3.5.1", "3.13.1"]:
        for r in new_rows:
            if r["Control_ID"] == cid:
                text = r["Control_Text"]
                print(f"  {cid}: {text[:100]}...")
                break

    return len(new_rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild Control Implementation Matrix")
    parser.add_argument("--pdf-path", default="reference-docs/NIST-SP-800-171-Rev2.pdf")
    parser.add_argument("--matrix-path", default="templates/Control-Implementation-Matrix.csv")
    args = parser.parse_args()

    rebuild_matrix(args.pdf_path, args.matrix_path)
