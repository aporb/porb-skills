# SAM.gov Public UI Search — Proven Workflow

Verified 2026-07-18. The SAM.gov opportunities search UI works anonymously (no login) at
`https://sam.gov/search?index=opp`. This is the reliable way to filter by NAICS + set-aside + active status.

## Filter application

- Start URL: `https://sam.gov/search?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm%5Bstatus%5D%5Bis_active%5D=true`
- **URL `sfm[]` params are unreliable for NAICS** — they are silently ignored on first load (~16,008 unfiltered results = tell-tale sign). Set-aside `sfm[setAside]` params DO tend to stick. Verify chips in the left filter panel.
- **NAICS:** expand "Product or Service Information" (may need 2 clicks), click the NAICS combobox, type the code, wait ~2s for typeahead, press Enter. Repeat per code (codes are OR'd). Element refs change after each search — re-snapshot before each subsequent code entry.
- **Set-aside "SB or unrestricted":** add BOTH `Total Small Business` and `No set aside used` chips.
- **Do NOT type NAICS codes into the keyword textbox** — keyword search doesn't cover the NAICS field; returns "No matches found".

## Result-count sanity checks (2026-07-18, Active + SBA + NONE)

| NAICS | Results |
|---|---|
| 541611 alone | 21 |
| + 541519 | 104 |
| + 611430 | 135 |

## DOM extraction snippet (browser_console)

Each page shows 25 result cards. Cards: h3 > a[href*="/workspace/contract/opp/"], plus Notice ID,
deadline, notice type, agency/subtier/office, dates. This snippet returns JSON for the current page:

```js
(() => {
  const items = [];
  const seen = new Set();
  document.querySelectorAll('h3 a[href*="/workspace/contract/opp/"]').forEach(a => {
    const href = a.href;
    if (seen.has(href)) return;
    seen.add(href);
    let card = a;
    for (let i=0; i<8; i++) { card = card.parentElement; if (!card) break; if (card.innerText && card.innerText.length > 300) break; }
    if (!card) return;
    const text = card.innerText.replace(/\s+/g,' ');
    const grab = (re) => { const m = text.match(re); return m ? m[1].trim() : null; };
    items.push({
      title: a.textContent.trim(),
      href,
      notice_id: grab(/Notice ID:\s*([A-Z0-9\-_\.]+)/i),
      deadline: grab(/Current (?:Response Date|Date Offers Due)\s*([A-Za-z0-9, :]+?(?:AM|PM)\s*[A-Z]{3,4})/),
      notice_type: grab(/Notice Type\s*([A-Za-z ]+?)(?:Updated Date|$)/),
      updated: grab(/Updated Date\s*([A-Za-z0-9, ]+?)(?:Published|\(|$)/),
      awardee: grab(/Awardee\s*([A-Z0-9 &.,'\"-]+?)\s*Unique Entity/),
      agency: (() => { const m = text.match(/Department\/Ind\.Agency\s*([A-Z0-9 ,.&()'-]+?)\s*Subtier/); return m?m[1].trim():null; })(),
      subtier: (() => { const m = text.match(/Subtier\s*([A-Z0-9 ,.&()'-]+?)\s*Office/); return m?m[1].trim():null; })(),
      office: (() => { const m = text.match(/Office\s*([A-Z0-9 ,.&()'-]+?)\s*(?:Contract Opportunities|$)/); return m?m[1].trim():null; })()
    });
  });
  return JSON.stringify({count: items.length, items});
})()
```

Notes:
- Not every card has every field — sole-source notices often lack deadline/type in list view; award notices have `awardee` instead of deadline. Nulls are expected.
- **Value is NOT in list view.** For <$X filters, open each notice detail page.
- Paginate via the "Next Page" button; re-run the snippet per page and concatenate.
- Detail URL pattern: `https://sam.gov/workspace/contract/opp/<32-char-hex>/view`
- Biddable notice types: `Original/Updated Solicitation`, `Combined Synopsis/Solicitation`, `Sources Sought`. `Award Notice` and most `Presolicitation`/`Special Notice` sole-source items are FYI only.

## Aggregator access notes

- **HigherGov**: anonymous users get a few free views, then a hard "You've used all of your free views" wall (trial/login required). Paid-only in practice.
- **State portals** (SC SCBO `web.casm.sc.gov`, TX ESBD `txsmartbuy.com`): bare curl returns 0 bytes/redirects — use the browser tool.
