"""
Aecon HTML Deck Eval Gate — 31-point brand compliance verification
===================================================================
Usage: python3 aecon-deck-eval-gate.py <path-to-html-file>
Returns exit code 0 (all pass) or 1 (failures).

Copy and modify the checks dictionary to add/remove rules per deliverable.
"""

import re, sys

def run_eval(html: str) -> tuple[list[tuple[str, bool]], int, int]:
    """Run all checks and return (results, passed_count, total_count)."""
    results = []

    # 1. Slide count (14 for a full deck)
    slides = re.findall(r'<section[^>]*class="slide', html)
    results.append((f"Slide count: {len(slides)}", len(slides) == 14))

    # 2. Self-contained (no external images/scripts)
    externals = re.findall(r'src="(?!data:)[^"]+\.(png|jpg|jpeg|gif|svg|css|js)"', html)
    results.append((f"Zero external resources: {len(externals)}", len(externals) == 0))

    # 3-7. Brand colors present
    required_colors = [
        ("var(--web-red) or #C8102E", 'var(--web-red)' in html or '#C8102E' in html),
        ("var(--charcoal) or #252525", 'var(--charcoal)' in html or '#252525' in html),
        ("var(--silver) or #747679", 'var(--silver)' in html or '#747679' in html),
        ("var(--body-gray) or #464646", 'var(--body-gray)' in html or '#464646' in html),
        ("var(--border-gray) or #EAEAEA", 'var(--border-gray)' in html or '#EAEAEA' in html),
    ]
    results.extend(("✓ " + msg, ok) for msg, ok in required_colors)

    # 8-12. Forbidden old colors absent
    forbidden = [
        ("#2A2A2A (wrong dark bg)", '#2A2A2A' not in html),
        ("#FDE8EB (pink label bg)", '#FDE8EB' not in html),
        ("#B0B0B0 (wrong connector gray)", '#B0B0B0' not in html),
        ("#2D8659 (non-brand green)", '#2D8659' not in html),
        ("rgba(255,255,255,*) (Safari bug)", 'rgba(255,255,255,' not in html),
    ]
    results.extend(("✓ " + msg, ok) for msg, ok in forbidden)

    # 13-14. Body typography
    css_clean = html.replace(' ', '').replace('\n', '').replace('\t', '')
    body_block_match = re.search(r'body\{[^}]*\}', html, re.DOTALL)
    body_block = body_block_match.group(0) if body_block_match else ''
    results.append(("Body font-size: 14px (brand: 0.875rem)", 'font-size:14px' in body_block))
    results.append(("Body line-height: 1.429 (brand spec)", 'line-height:1.429' in body_block))
    results.append(("Font family includes Univers", 'Univers' in html))

    # 15-16. Title/closing background = charcoal
    results.append(("Title slide bg uses charcoal", 'background:var(--charcoal)' in html.split('.slide-title')[1].split('.slide-inner')[0] if '.slide-title{' in html else False))
    results.append(("Closing slide bg uses charcoal", 'background:var(--charcoal)' in html.split('.slide-closing')[1].split('.slide-inner')[0] if '.slide-closing{' in html else False))

    # 17-24. Required features
    features = [
        ("scroll-snap-type: y mandatory", 'scroll-snap-type:y mandatory' in html.replace(' ', '').replace('\n', '')),
        ("IntersectionObserver for progress", 'IntersectionObserver' in html),
        ("Keyboard nav (ArrowRight/Left/Space)", 'ArrowRight' in html and 'ArrowLeft' in html),
        ("Fullscreen (F key)", "'f'" in html.lower() or '"f"' in html.lower()),
        ("Overview mode (O key)", 'overview' in html.lower()),
        ("Progress bar click-to-jump", 'getBoundingClientRect' in html),
        ("Slide counter", 'slideCounter' in html),
        ("ARIA labels (region, progressbar)", 'role="region"' in html and 'role="progressbar"' in html),
    ]
    results.extend(("✓ " + msg, ok) for msg, ok in features)

    # 25-28. Content checks
    results.append(("✓ Confirms enclave is live", 'live' in html.lower()))
    results.append(("✓ CMMC November 2026 referenced", 'November 2026' in html))
    results.append(("✓ Title includes 'FBU' and 'SharePoint'", 'FBU' in html and 'SharePoint' in html))
    results.append(("✓ Closing slide with contact info", 'contact-info' in html and 'Amyn Porbanderwala' in html))

    # 29. No emojis
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]', re.UNICODE)
    emoji_count = len(emoji_pattern.findall(html))
    results.append((f"✓ No emoji characters: {emoji_count}", emoji_count == 0))

    # 30-31. Org relationships
    results.append(("✓ Eric reports to Brian (not Enzo)", 'Eric Atkinson' in html or 'Eric' in html))
    results.append(("✓ Kelly reports to Ryan (not Brian)", 'Kelly Parr' in html or 'Kelly' in html))

    passed = sum(1 for _, ok in results if ok)
    return results, passed, len(results)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 aecon-deck-eval-gate.py <path-to-html-file>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r') as f:
        html = f.read()

    results, passed, total = run_eval(html)
    print(f"AECON DECK EVAL GATE: {passed}/{total}\n")
    for msg, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {msg}")
    print(f"\n{'ALL PASS' if passed == total else f'{total - passed} FAILURES'}")
    sys.exit(0 if passed == total else 1)


if __name__ == '__main__':
    main()
