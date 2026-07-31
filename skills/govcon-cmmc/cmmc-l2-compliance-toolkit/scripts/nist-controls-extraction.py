#!/usr/bin/env python3
"""
Extract the 110 NIST SP 800-171 Rev 2 controls from the PDF.

This script extracts all `3.x.x` controls from the NIST SP 800-171 Rev 2 PDF
and saves them to `nist_800_171_controls.json` in a structured format.

Requirements:
- pdftotext (poppler-utils package)

Usage:
    python3 nist-controls-extraction.py
"""

import subprocess
import re
import json

# Path to the NIST SP 800-171 Rev 2 PDF
PDF_PATH = "reference-docs/NIST-SP-800-171-Rev2.pdf"

# Output JSON path
OUTPUT_PATH = "nist_800_171_controls.json"

# Family codes mapping (3.x to family name)
FAMILY_CODES = {
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
    "3.14": "SI - System and Information Integrity"
}

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ['pdftotext', '-layout', pdf_path, '-'],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

def extract_controls(text):
    """Extract all 3.x.x controls from the PDF text."""
    # Pattern to match control lines (e.g., "3.1.1 Limit system access...")
    pattern = r'^(3\.\d+\.\d+)\s+(.+)$'
    
    controls = {}
    for line in text.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            control_id = match.group(1)
            control_text = match.group(2)
            
            # Extract family (e.g., "3.1" from "3.1.1")
            family = control_id[:3] if control_id[2] == '.' else control_id[:4]
            
            # Initialize family if not exists
            if family not in controls:
                controls[family] = []
            
            # Add control to family
            controls[family].append({
                "id": control_id,
                "text": control_text
            })
    
    return controls

def save_controls_to_json(controls, output_path):
    """Save controls to JSON file."""
    # Count total controls
    total = sum(len(family_controls) for family_controls in controls.values())
    
    output = {
        "families": controls,
        "total": total
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    return total

def main():
    """Main function."""
    print("Extracting controls from NIST SP 800-171 Rev 2 PDF...")
    
    # Extract text from PDF
    text = extract_text_from_pdf(PDF_PATH)
    print(f"Extracted {len(text)} characters from PDF")
    
    # Extract controls
    controls = extract_controls(text)
    print(f"Found {len(controls)} control families")
    
    # Save to JSON
    total = save_controls_to_json(controls, OUTPUT_PATH)
    print(f"Extracted {total} controls total")
    
    # Print family breakdown
    print("\nFamily breakdown:")
    for family, family_controls in sorted(controls.items()):
        print(f"  {family} ({FAMILY_CODES.get(family, 'Unknown')}): {len(family_controls)} controls")
    
    print(f"\nControls saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()