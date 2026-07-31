---
name: api-research
title: External API Research and Integration
description: Systematically research, evaluate, and integrate external APIs - registration, authentication, rate limits, documentation, and client libraries
version: 1.0.0
tags: [api, integration, research, client-libraries]
related_skills: [federal-contracting-research, strategic-research, sbir-topic-pull, deep-research]
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# API Research and Integration

Systematic approach to researching, evaluating, and integrating external APIs.

## When to Use

Load this skill when you need to:
- Research a new external API for integration
- Find client libraries for an API
- Understand authentication, rate limits, and usage patterns
- Evaluate multiple API options for a use case

## Research Checklist

For each API, gather:

### 1. Registration and Access
- Registration URL and process
- Required information (email, company info, etc.)
- Time to receive credentials
- Any approval process

### 2. Authentication
- Authentication method (API key, OAuth, JWT, etc.)
- How to pass credentials (headers, query params, etc.)
- Token format and examples
- Any scope or permission requirements

### 3. Rate Limits
- Requests per second/minute/hour
- Daily/monthly quotas
- Burst allowances
- Throttling behavior
- How limits are tracked (per key, per IP, etc.)

### 4. Base URL and Endpoints
- Base URL(s) for different regions/environments
- Key endpoints and their purposes
- URL patterns and path parameters
- Versioning strategy

### 5. Request/Response Format
- Request format (JSON, XML, form data)
- Required and optional parameters
- Response format and structure
- Error handling and status codes
- Pagination mechanisms

### 6. Documentation Quality
- Official documentation URLs
- Getting started guides
- API reference
- Code examples
- SDK/client libraries mentioned

### 7. Client Libraries

#### Finding Python Libraries
1. Search GitHub: `github.com/search?q=<api-name>+python`
2. Check PyPI: `pip search <api-name>` (if available)
3. Look for official SDKs
4. Evaluate community libraries

#### Evaluating Libraries
Criteria:
- **Activity**: Last commit date, recent issues
- **Popularity**: Stars, forks, downloads
- **Maintenance**: Active maintainers, issue response time
- **Documentation**: README, examples, API docs
- **Features**: Endpoint coverage, pagination handling, error handling
- **Dependencies**: Lightweight vs. heavy dependencies
- **Python Version**: Support for your target version

#### Recommended Library Information
For each recommended library, provide:
- GitHub/repository URL
- Installation command
- Quick start example
- Key features and benefits
- Any limitations or caveats

## Research Workflow

1. **Initial Discovery**
   - Find official documentation
   - Identify authentication method
   - Note any registration requirements

2. **Deep Dive**
   - Review rate limits and quotas
   - Explore key endpoints
   - Check for SDKs/client libraries

3. **Client Library Search**
   - Search GitHub for Python libraries
   - Evaluate candidates against criteria
   - Test top candidates if time permits

4. **Documentation**
   - Compile findings into structured format
   - Provide code examples
   - Note any pitfalls or gotchas

## Common Patterns

### API Key Authentication
```python
import requests

headers = {"token": "your_api_key"}  # or "Authorization": "Bearer token"
response = requests.get("https://api.example.com/endpoint", headers=headers)
```

### Rate Limiting
- Implement exponential backoff
- Respect Retry-After headers
- Cache responses when appropriate
- Use connection pooling

### Pagination
```python
all_results = []
page = 1
while True:
    response = requests.get(f"https://api.example.com/data?page={page}")
    data = response.json()
    all_results.extend(data['results'])
    if not data.get('has_more'):
        break
    page += 1
```

## Pitfalls

- **Incomplete Documentation**: Always test with actual API calls
- **Hidden Rate Limits**: Monitor headers for rate limit info
- **Authentication Changes**: APIs sometimes change auth methods
- **Deprecated Endpoints**: Check documentation for deprecation notices
- **Regional Differences**: Some APIs have different endpoints by region
- **Client Library Abandonment**: Prefer active, maintained libraries
- **Over-engineering**: For simple APIs, direct HTTP requests may be better than a library
- **Documentation Navigation**: Homepage links may not work; try direct paths like `/docs/developer-manual/` or search for "developer" in the site
- **Platform vs API Docs**: Some services separate platform infrastructure docs (e.g., GitHub repos) from API documentation; check both and follow the API-specific links
- **No Official Client is Normal**: Gateway infrastructure services (like api.data.gov) often don't have official clients because they're not APIs themselves; use standard HTTP libraries
- **Bot Protection is a Critical Signal**: If a site shows "Just a moment..." with Cloudflare or similar challenge pages, the site is blocking automated access. This is especially common with government sites (FBI, federal agencies). In these cases:
  - Accept that direct documentation access may be impossible
  - Use alternative sources: Data.gov catalog, GitHub repositories, community documentation
  - Look for dataset listings that might contain API information
  - Consider direct contact with the agency if API access is critical
- **404 Doesn't Always Mean Gone**: If a well-documented URL returns 404, the API may have been moved or restructured. Check:
  - Data.gov for official dataset listings (especially for US government APIs)
  - GitHub for alternative documentation or community-maintained wrappers
  - The agency's main website for updated links
- **Government APIs Often Split into Multiple Services**: Federal agencies frequently have separate APIs for different data types. For example, the FBI has both:
  - A public API (wanted persons, art crimes) with open access
  - A UCR (Uniform Crime Reporting) API for crime statistics with potential registration requirements
  Always search for "[agency] API" broadly, not just the specific data you need
- **Outdated Data.gov Listings**: Dataset entries on Data.gov can be years old (last updated dates like 2017 are common). These may not reflect current API status. Cross-reference with:
  - GitHub repositories that actually use the API
  - Recent issues in those repositories discussing API changes
  - The agency's current website
- **Limited Client Libraries for Niche APIs**: Specialized government APIs often have minimal or abandoned Python client libraries. When searching GitHub:
  - Sort by stars, but check last commit date (abandoned repos may still have high stars)
  - Look for recent activity in issues/discussions
  - Be prepared to implement direct HTTP requests using requests/urllib3
  - Multiple repos may exist in different languages (R, Node.js, Python) - check all for documentation patterns

## Reference APIs

Documented in `references/`:
- `agent-framework-evaluation.md` — Pattern for evaluating AI agent infrastructure, frameworks, and tools. 8-step evaluation: discovery → deep code scan → architecture understanding → security assessment → platform coverage analysis → maintenance evidence → verification strategy → HTML briefing deliverable.
- `noaa-climate-data-online.md` - NOAA Climate Data Online Web Services
- `api-data-gov.md` - API.data.gov federal API gateway (authentication, rate limits, registration)
- `fbi-crime-data-api.md` - FBI Crime Data API research notes, including challenges with bot protection and deprecated endpoints
- `dsip-dod-sbir-api.md` - DoD SBIR/STTR DSIP public API — endpoints, auth boundaries, download URL patterns, pitfalls
- `usaspending-company-recipient-lookup.md` - USAspending company/recipient resolver endpoints, UEI/DUNS lookup, award counts, and award-search pitfalls
- `usaspending-api.md` - USAspending API for company/recipient research: recipient lookup, UEI/DUNS resolution, award-search quirks, and one-box company resolver pattern (includes spending_over_time, spending_by_category, grouped subawards, and IDV code quirks)
- `usaspending-cgo-dashboard.md` - Fractional CGO dashboard data architecture for GovCon growth intelligence: obligation trends, recompete detection, vehicle inference, NAICS/PSC lane mapping, and subaward posture

## CGO Dashboard Pattern

When a user wants a federal contracting company dashboard (not just a lookup), load `references/usaspending-cgo-dashboard.md`. It covers the six-parallel-call pipeline, recompete window detection, vehicle/IDV inference, and known endpoint pitfalls for real-time USAspending dashboards.

## Support Files

- `references/` - API-specific research and documentation
