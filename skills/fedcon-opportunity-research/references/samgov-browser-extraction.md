# SAM.gov Browser Extraction (No API Key)

Verified 2026-07-18. SAM.gov's opportunities API returns 401 without a registered key; the public search UI works anonymously and exposes live notice metadata. Use browser tools — curl returns only the JS shell.

## Interaction sequence

1. Navigate: `https://sam.gov/search/?index=opp&sfm%5Bstatus%5D%5Bis_active%5D=true`
   (adding `&keywords=541611` does NOT pre-fill the simple-search box — skip it)
2. In the Filter By panel, locate the `keyword-text` textbox. Type the NAICS code and press Enter. Bare NAICS codes are valid keywords and return the full active set for that code.
3. Wait ~5 seconds for the result list to render. Confirm with:
   `document.body.innerText.match(/Showing [\d,\s-]+ of [\d,]+ results/)`
4. Extract cards with the JS below.
5. To query another code, re-navigate to the base search URL (fresh page) and repeat — re-typing into a stale page is unreliable.

## Card extraction JS

```js
(()=>{
  const out = [];
  document.querySelectorAll('h3 a').forEach(a=>{
    let n = a, container = null;
    for(let i=0;i<12 && n;i++){
      if(n.innerText && n.innerText.includes('Notice ID:') && n.innerText.includes('Contract Opportunities')){
        container = n; break;
      }
      n = n.parentElement;
    }
    if(!container) return;
    out.push({title: a.textContent.trim(), url: a.href,
              raw: container.innerText.replace(/\s+/g,' ').slice(0,800)});
  });
  return JSON.stringify(out);
})()
```

## Fields available per card (parse from `raw`)

- Title + view URL (`https://sam.gov/workspace/contract/opp/<id>/view`)
- Notice ID
- Department / Subtier / Office
- Current Response Date or Current Date Offers Due (with time + TZ)
- Notice Type (Solicitation, Combined Synopsis/Solicitation, Sources Sought, Presolicitation, Special Notice, Award Notice, Justification)
- Published / Updated dates
- Awardee + Unique Entity ID (only on Award Notices)

## NOT in the list view

- Set-aside status — must open the individual notice page
- Estimated value / ceiling — infer from USAspending history of similar actions
- NAICS of record — the keyword match is the only NAICS signal in list view

## Result volumes (2026-07-18 snapshot, active only)

| NAICS | Active notices |
|---|---|
| 541611 | 762 |
| 541519 | 1,450 |
| 611430 | 283 |

Only the first 25 cards render per page; default sort is Updated Date desc, so page 1 is the freshest slice — usually enough for a 30-day deadline window.

## Filtering recipe

1. Parse deadline from `raw` (`Current (?:Response Date|Date Offers Due)` followed by the date string).
2. Keep deadlines inside the target window.
3. Drop notice types `Award Notice`, `Justification`, and cards whose `raw` contains `intent to sole source` (already decided).
4. Keep `Sources Sought` — zero-cost entry points for firms with no past performance; responses shape the set-aside decision.
5. Confirm set-aside and PWS details by opening each surviving notice URL.
