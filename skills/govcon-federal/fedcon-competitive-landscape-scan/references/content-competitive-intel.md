# Content / Voice Competitive Intelligence Methodology

**Sibling to `fedcon-competitive-landscape-scan`.** This is NOT the USASpending/NAICS federal-contract-data competitive scan. This methodology analyzes the thought-leadership / content landscape — who is covering which angles in a topic space, what coverage gaps exist, and how to position an article to occupy an unserved intersection.

## When to Use

- User asks "who's covering [topic] on LinkedIn/X" or "competitive intelligence on [topic space]"
- Pre-publication analysis: what angles exist, what's missing, where to position
- User provides an article or draft article and wants to know "who else talks about this and how"
- Any task asking about "coverage gaps," "dominant narratives," "top voices," or "what nobody is covering"

## Methodology

### Phase 1: Extract the Article's Framework

Before researching competitors, understand what the article uniquely provides:

1. **Identify the named framework** — e.g., "AI Sovereignty Ladder," "One Question Litmus Test," "the platform playbook"
2. **Extract the evidence structure** — what data points, sources, or anecdotes anchor each claim
3. **Note the three-domain intersection** — what topic domains does the article connect that normally exist separately? The moat is the intersection, not any single domain.
4. **Identify quotable one-liners** — these are what gets shared

### Phase 2: Map the Competitive Voice Landscape

Run parallel searches to discover who covers the topic space. When search tools are down, use the source list embedded in the article itself (briefings, cited articles, references) as the seed list.

**Competitor types to look for:**

| Cluster | Typical Voices | Angle |
|---------|---------------|-------|
| Architecture/Infrastructure | Platform vendors, GovCon consultants | Sovereignty as vendor choice or architecture decision |
| Business Media | Trade press, startup-focused outlets | Platform competition, startup risk, corporate drama |
| Enterprise / Privacy | Tech CEOs, security researchers | Information asymmetry, control your data |
| Compliance | FedRAMP/CMMC content providers | Sovereignty as regulatory checkbox |
| Commodity | Generic consultants | Surface-level, no original research |

### Phase 3: Extract Competitor Content

For each known competitor URL, extract structured metadata and content:

1. **JSON-LD extraction** (see `web-research` skill, `references/curl-python-html-extraction.md`, Pattern 8): Get title, word count, publish date, description, author. Word count reveals depth — 4,700+ words is a definitive guide; 1,500 words is a blog post.
2. **X/Twitter search**: When x_search is unavailable, curl the competitor's Twitter/X profile page or use web_extract on public sources that archive posts.
3. **Content body extraction**: Use generic tag extraction (Pattern 2) or keyword search (Pattern 3) from the curl-python-html-extraction reference to read article body content.
4. **Cross-reference date** — a Feb 2026 article vs. a Jul 2026 article: the gap may explain differences in claims.

### Phase 4: Answer the Structured Questions

Map each competitor's content against the article's framework to answer:

1. What angles are other voices taking on this topic?
2. What's the dominant narrative (the "default" framing)?
3. **What's the coverage gap** — what does this article provide that NO ONE else does?
4. What's getting engagement on these topics (what patterns work)?
5. Who are the top voices and what's their angle?
6. Is anyone else connecting the same three domains?
7. What's the competitive risk — how fast could someone else fill this gap?
8. How to position the article to maximize the coverage gap

### Phase 5: Assess Competitive Risk

**Risk factors (in order of threat):**
- Does a platform vendor (selling into this space) already cover the angle? High risk — they have audience + domain expertise.
- Does a niche creator have one piece of the puzzle? Medium risk — they could add the missing domain.
- Does anyone have all three domains? Low-to-none — this IS the gap.

**Moat factors (in order of defense):**
- First-mover advantage on a specific intersection
- A named, proprietary framework (not a generic concept)
- Verified source checklist or traceable evidence
- Domain-specific depth the gap-filler lacks (GovCon ≠ developer audience)
- Credible external voices as validation (Nadella, Karp, etc.)

**Timeline estimate:** Expect LinkedIn copycats in 2-4 weeks. Expect platform competitors to absorb the angle in 3-6 weeks. The moat degrades by ~25% per week after publication.

### Phase 6: Produce the Report

Standard 8-section structure:

1. Executive Summary — 1 paragraph: the gap, risk, positioning
2. Voice Landscape — per-cluster breakdown of who covers what
3. Dominant Narrative — the default framing competitors use
4. Coverage Gap — what the article provides that nothing else does
5. Engagement Patterns — what works for who
6. Top Voices Table — voice | platform | angle | GovCon depth | CLIO-aware
7. Competitive Risk — timeline, who could close the gap, protections
8. Positioning Recommendations — platform-specific advice, defensive moats, what NOT to do

## Pitfalls

- **"Unverifiable" search claims.** When Tavily/Firecrawl/browser are all down, you cannot claim negative findings. Say "all search/extraction tools were unavailable during research" and note which sources you could access directly.
- **Competitor-as-author vs. competitor-as-platform.** A platform like Cabrillo Club publishes articles as an Organization — its author is vested in selling the platform. A journalist like Paul Drecksler has different incentives. Note the source type in the report.
- **Date gaps matter.** A February 2026 article cannot address an April 2026 product launch. Don't fault a competitor for missing recent events unless their content claims currency.
- **JSON-LD word counts are authoritative but may exclude captions/tables.** A 2,402-word article in JSON-LD means the prose body is ~2,400 words. Full tables and embedded content push real depth higher.
- **Open-weight model claim verification.** When a competitor article claims "open-weight models have closed the capability gap," verify against actual benchmarks (MMLU, HumanEval, SWE-Bench). Cabrillo Club makes this claim; it's generally true for 70B+ models on standard benchmarks but may not hold for agentic coding or domain-specific tasks.
- **Nadella/Karp quotes are powerful but context-dependent.** Verifying the exact quote source (original speech, interview, earnings call transcript) adds credibility. LinkedIn paraphrase is NOT source authority.
- **Do not fabricate engagement scores.** Without X API or social analytics, you cannot know actual engagement. Say "based on available signal (Shopifreaks coverage, The Decoder analysis, LinkedIn articles)" rather than claiming engagement numbers.
