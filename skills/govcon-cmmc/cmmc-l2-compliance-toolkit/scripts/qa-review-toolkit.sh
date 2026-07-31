#!/usr/bin/env bash
# qa-review-toolkit.sh — Comprehensive QA review for a CMMC L2 compliance toolkit.
#
# Usage:  bash qa-review-toolkit.sh /path/to/compliance-toolkit
#
# Runs the full audit matrix (SOPs, templates, index docs, references, overall quality)
# and emits structured PASS/FAIL output suitable for translating into a report.
# Correctly handles grep alternation (uses bare | with -E, never \|).
#
# Output sections:
#   1. SOPs (14 files)            4. Reference Documents
#   2. Templates (11 files)       5. Overall Quality
#   3. Index Documents            6. Summary counts

set -euo pipefail

TOOLKIT="${1:-.}"
cd "$TOOLKIT"

PASS=0; FAIL=0
mark_pass() { echo "  [PASS] $*"; PASS=$((PASS+1)); }
mark_fail() { echo "  [FAIL] $*"; FAIL=$((FAIL+1)); }

check_contains() {  # <file> <label> <pattern>
  local file="$1" label="$2" pattern="$3"
  if grep -qiE "$pattern" "$file"; then mark_pass "$label"; else mark_fail "$label ($file)"; fi
}

echo "============================================================"
echo " CMMC L2 Compliance Toolkit — QA Review"
echo " Path: $(pwd)"
echo " Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "============================================================"

# ---------------------------------------------------------------------------
# 1. SOPs
# ---------------------------------------------------------------------------
echo ""; echo "=== 1. SOPs (control-families/) ==="
declare -A EXP=( [1]=22 [2]=3 [3]=9 [4]=9 [5]=11 [6]=3 [7]=6 [8]=9 [9]=2 [10]=6 [11]=3 [12]=4 [13]=16 [14]=7 )
sop_total=0
for f in control-families/*/CS-*.SOP.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  echo "--- $name ($(wc -l < "$f") lines) ---"

  # Document Control fields (7)
  for field in "Document ID" "Version" "Effective Date" "Last Reviewed" "Next Review" "Owner" "Approved By"; do
    check_contains "$f" "DocCtrl: $field" "$field"
  done

  # Required sections (numbered headings like "## 1. Purpose")
  for sec in Purpose Scope References "Roles and Responsibilities" "Controls Covered" Procedures "Evidence Collection" "Exceptions and Variance" "Review and Maintenance" "Revision History"; do
    if grep -qiE "^#+ +([0-9]+\. +)?$sec" "$f"; then mark_pass "Section: $sec"; else mark_fail "Section: $sec ($name)"; fi
  done

  # Control count for this family (3.N.M headings)
  fam=$(grep -oE '3\.([0-9]+)\.' "$f" | head -1 | grep -oE '[0-9]+' | tail -1)
  found=$(grep -cE "^### +3\." "$f")
  want=${EXP[$fam]:-?}
  if [ "$found" = "$want" ]; then mark_pass "Controls 3.$fam: $found (want $want)"; else mark_fail "Controls 3.$fam: found=$found want=$want ($name)"; fi
  sop_total=$((sop_total+found))
done
echo "--- SOP control total: $sop_total (want 110) ---"

# ---------------------------------------------------------------------------
# 2. Templates
# ---------------------------------------------------------------------------
echo ""; echo "=== 2. Templates (templates/) ==="

# SSP — 110 unique control IDs
ssp_ids=$(grep -oE '3\.[0-9]+\.[0-9]+' templates/SSP-Template.md | sort -u | wc -l)
[ "$ssp_ids" = "110" ] && mark_pass "SSP: 110 unique control IDs" || mark_fail "SSP: $ssp_ids unique control IDs (want 110)"

# POAM — 111 lines, no duplicate header, 110 data rows
poam_lines=$(wc -l < templates/POAM-Tracker.csv)
poam_dup=$([ "$(sed -n '1p' templates/POAM-Tracker.csv)" = "$(sed -n '2p' templates/POAM-Tracker.csv)" ] && echo YES || echo NO)
[ "$poam_lines" = "111" ] && mark_pass "POAM: 111 lines" || mark_fail "POAM: $poam_lines lines (want 111)"
[ "$poam_dup" = "NO" ] && mark_pass "POAM: no duplicate header" || mark_fail "POAM: DUPLICATE HEADER (lines 1=2)"

# CIM — 111 lines, no duplicate header
cim_lines=$(wc -l < templates/Control-Implementation-Matrix.csv)
cim_dup=$([ "$(sed -n '1p' templates/Control-Implementation-Matrix.csv)" = "$(sed -n '2p' templates/Control-Implementation-Matrix.csv)" ] && echo YES || echo NO)
[ "$cim_lines" = "111" ] && mark_pass "CIM: 111 lines" || mark_fail "CIM: $cim_lines lines (want 111)"
[ "$cim_dup" = "NO" ] && mark_pass "CIM: no duplicate header" || mark_fail "CIM: DUPLICATE HEADER (lines 1=2)"

# Checklist — >=30 procedures + key terms
check_rows=$(tail -n +2 templates/Cybersecurity-Program-Checklist.csv | grep -c .)
[ "$check_rows" -ge 30 ] && mark_pass "Checklist: $check_rows procedures (>=30)" || mark_fail "Checklist: $check_rows procedures (want >=30)"
for term in SPRS C3PAO "awareness" "vulnerability" "access review" "incident" "backup" POAM; do
  check_contains templates/Cybersecurity-Program-Checklist.csv "Checklist: $term" "$term"
done

# Asset inventory — header + >=5 example rows
asset_rows=$(tail -n +2 templates/Asset-Inventory-Template.csv | grep -c .)
[ "$asset_rows" -ge 5 ] && mark_pass "Asset-Inventory: $asset_rows example rows (>=5)" || mark_fail "Asset-Inventory: $asset_rows rows (want >=5)"

# Risk register — header + >=3 example rows
risk_rows=$(tail -n +2 templates/Risk-Register-Template.csv | grep -c .)
[ "$risk_rows" -ge 3 ] && mark_pass "Risk-Register: $risk_rows example rows (>=3)" || mark_fail "Risk-Register: $risk_rows rows (want >=3)"

# IR Plan — required elements (use separate checks to avoid alternation escaping bugs)
check_contains templates/Incident-Response-Plan.md "IR: 72-hour reporting" "72 hour"
check_contains templates/Incident-Response-Plan.md "IR: DIBNet" "DIBNet|dibnet"
check_contains templates/Incident-Response-Plan.md "IR: severity matrix" "severity"
check_contains templates/Incident-Response-Plan.md "IR: Containment" "Containment"
check_contains templates/Incident-Response-Plan.md "IR: Eradication" "Eradication"
check_contains templates/Incident-Response-Plan.md "IR: Recovery" "Recovery"
check_contains templates/Incident-Response-Plan.md "IR: lessons learned" "[Ll]essons [Ll]earned"
check_contains templates/Incident-Response-Plan.md "IR: escalation" "[Ee]scalat"

# Scope Determination — required elements
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: enclave boundary" "[Ee]nclave|[Bb]oundary"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: in-scope" "[Ii]n-[Ss]cope|[Ii]n [Ss]cope"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: out-of-scope" "[Oo]ut-[Oo]f-[Ss]cope|[Oo]ut of [Ss]cope"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: CUI data flow" "[Dd]ata [Ff]low|dataflow"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: ESP" "ESP|External Service Provider|Managed Service"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: GCC High" "GCC High|GCC-High|Government Community Cloud"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: facilities" "[Ff]acilit"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: mobile" "mobile|[Mm]obile"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: printing" "print|[Pp]rint"
check_contains templates/CMMC-L2-Scope-Determination.md "Scope: removable media" "removable"

# Evidence Matrix — all 14 families
ev_fams=$(tail -n +2 templates/Evidence-Collection-Matrix.csv | cut -d',' -f1 | sort -u | wc -l)
[ "$ev_fams" = "14" ] && mark_pass "Evidence-Matrix: $ev_fams families (want 14)" || mark_fail "Evidence-Matrix: $ev_fams families (want 14)"

# CUI Data Flow Register
check_contains templates/CUI-Data-Flow-Register.md "CUI-DF: entry" "[Ee]ntry|[Ii]ngress|[Ii]ntake|[Ii]nput"
check_contains templates/CUI-Data-Flow-Register.md "CUI-DF: processing" "[Pp]rocess"
check_contains templates/CUI-Data-Flow-Register.md "CUI-DF: storage" "[Ss]tor"
check_contains templates/CUI-Data-Flow-Register.md "CUI-DF: transmission" "[Tt]ransmis"
check_contains templates/CUI-Data-Flow-Register.md "CUI-DF: destruction" "[Dd]estruct|[Dd]isposal|[Ss]anitiz|[Pp]urge|[Ss]hred"

# TAA / Section 889
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: Trade Agreements Act" "Trade Agreements|TAA"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: Section 889" "Section 889|889"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: Huawei" "Huawei"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: ZTE" "ZTE"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: Hytera" "Hytera"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: Hikvision" "Hikvision"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: Dahua" "Dahua"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: False Claims Act" "False Claims Act"
check_contains templates/TAA-Section889-Pre-Purchase-Checklist.md "TAA: FAR citations" "52\.204|48 CFR|FAR"

# ---------------------------------------------------------------------------
# 3. Index Documents
# ---------------------------------------------------------------------------
echo ""; echo "=== 3. Index Documents ==="

# README — tree matches actual template files
echo "--- README drift check (templates/) ---"
readme_missing=0
for f in templates/*; do
  base=$(basename "$f")
  if ! grep -q "$base" README.md; then echo "  [FAIL] MISSING FROM README: $base"; readme_missing=$((readme_missing+1)); FAIL=$((FAIL+1)); fi
done
[ "$readme_missing" = "0" ] && mark_pass "README: all template files listed in tree"

# Control-to-Document-Mapping — 110 controls
map_ids=$(grep -oE '3\.[0-9]+\.[0-9]+' Control-to-Document-Mapping.md | sort -u | wc -l)
[ "$map_ids" = "110" ] && mark_pass "Control-Mapping: $map_ids controls (want 110)" || mark_fail "Control-Mapping: $map_ids controls (want 110)"

# JSON — 14 families, total=110
if command -v python3 >/dev/null 2>&1; then
  json_total=$(python3 -c "import json; d=json.load(open('nist_800_171_controls.json')); print(d.get('total', sum(len(v) for v in d['families'].values())))" 2>/dev/null || echo "?")
  json_fams=$(python3 -c "import json; print(len(json.load(open('nist_800_171_controls.json'))['families']))" 2>/dev/null || echo "?")
  [ "$json_total" = "110" ] && mark_pass "JSON: total=$json_total" || mark_fail "JSON: total=$json_total (want 110)"
  [ "$json_fams" = "14" ] && mark_pass "JSON: $json_fams families" || mark_fail "JSON: $json_fams families (want 14)"
fi

# ---------------------------------------------------------------------------
# 4. Reference Documents
# ---------------------------------------------------------------------------
echo ""; echo "=== 4. Reference Documents ==="
[ -f reference-docs/NIST-SP-800-171-Rev2.pdf ] && {
  sz=$(stat -c%s reference-docs/NIST-SP-800-171-Rev2.pdf)
  [ "$sz" -gt 1000000 ] && mark_pass "NIST 800-171 Rev2 PDF ($sz bytes)" || mark_fail "NIST 800-171 Rev2 PDF too small ($sz bytes)"
} || mark_fail "NIST 800-171 Rev2 PDF missing"
[ -f reference-docs/NIST-SP-800-171A-Rev2.pdf ] && {
  sz=$(stat -c%s reference-docs/NIST-SP-800-171A-Rev2.pdf)
  [ "$sz" -gt 1000000 ] && mark_pass "NIST 800-171A Rev2 PDF ($sz bytes)" || mark_fail "NIST 800-171A Rev2 PDF too small ($sz bytes)"
} || mark_fail "NIST 800-171A Rev2 PDF missing"
dfars_count=$(ls -1 reference-docs/dfars-key-clauses/ 2>/dev/null | wc -l)
[ "$dfars_count" = "7" ] && mark_pass "DFARS key clauses: $dfars_count (want 7)" || mark_fail "DFARS key clauses: $dfars_count (want 7)"
[ -f reference-docs/32-CFR-Part-170-CMMC-Final-Rule.html ] && mark_pass "32 CFR Part 170 present" || mark_fail "32 CFR Part 170 missing"

# ---------------------------------------------------------------------------
# 5. Overall Quality
# ---------------------------------------------------------------------------
echo ""; echo "=== 5. Overall Quality ==="

# Stray temp files
stray=$(find . -type f \( -name '*.py' -o -name '*.tmp' -o -name '*.bak' -o -name '*~' -o -name '*.swp' -o -name '.DS_Store' \) | wc -l)
[ "$stray" = "0" ] && mark_pass "No stray temp files" || { mark_fail "$stray stray temp files found"; find . -type f \( -name '*.py' -o -name '*.tmp' -o -name '*.bak' -o -name '*~' -o -name '*.swp' -o -name '.DS_Store' \) | sed 's/^/    /'; }

# Empty directories
empty_dirs=$(find . -type d -empty | wc -l)
if [ "$empty_dirs" = "0" ]; then
  mark_pass "No empty directories"
else
  mark_fail "$empty_dirs empty directories found:"
  find . -type d -empty | sed 's/^/    /'
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""; echo "============================================================"
echo " SUMMARY:  $PASS passed, $FAIL failed"
if [ "$FAIL" = "0" ]; then
  echo " VERDICT:  READY FOR COMMIT"
else
  echo " VERDICT:  GAPS FOUND ($FAIL items to review)"
fi
echo "============================================================"
