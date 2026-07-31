# SAM.gov Attachment Download — API Interception Technique

Proven technique for downloading attachments from SAM.gov opportunity detail pages. SAM.gov is an SPA — direct curl on the page or the public API returns empty 200 responses. This technique uses browser-based JavaScript interception to capture the actual download URLs.

## When to Use

- You need to download and parse PWS/SOW/Synopsis PDFs from a SAM.gov Sources Sought or Solicitation
- The SAM.gov detail page shows attachments (PDF, DOCX) in the Attachments table
- Direct API calls to SAM.gov return empty 200 (no credentials) or 401/403

## The Technique (Step-by-Step)

### Step 1: Install API interception in the browser

After the SAM.gov detail page has loaded, inject monkey-patches to intercept `XMLHttpRequest` and `fetch` calls:

```javascript
downloadUrls = [];
(function() {
  var origFetch = window.fetch;
  window.fetch = function(url, opts) {
    if (typeof url === 'string' && (url.includes('download') || url.includes('resource'))) {
      downloadUrls.push({method: 'fetch', url: url});
    }
    return origFetch.apply(this, arguments);
  };
  var origOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url) {
    if (url && (url.includes('download') || url.includes('resource'))) {
      downloadUrls.push({method: 'XHR', url: url});
    }
    return origOpen.apply(this, arguments);
  };
})();
```

### Step 2: Click "Download All" (or individual file link)

Scroll to the Attachments section and click the **"Download All"** button (or individual PDF links). The button triggers an XHR/fetch call that our monkey-patch captures.

### Step 3: Read the intercepted URL

```javascript
downloadUrls
```

Example output:
```json
[{"method": "GET", "url": "/api/prod/opps/v3/opportunities/48e4f42a7d7e4d08b99cce5314cfe7e1/resources/download/zip?api_key=null&random=1784407856470"}]
```

### Step 4: Fetch the zip endpoint to get the S3 presigned URL

The zip endpoint returns JSON with a `location` field — NOT binary content:

```bash
curl -s \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  -H "Referer: https://sam.gov/workspace/contract/opp/<oppId>/view" \
  "https://sam.gov/api/prod/opps/v3/opportunities/<oppId>/resources/download/zip?api_key=null"
```

Returns:
```json
{"location": "https://iae-fbo-attachments.s3.amazonaws.com/fbo/files/134/134977...zip?response-content-disposition=attachment%3B%20filename%3DFinancial%2BManagement...&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20260718T205141Z&X-Amz-SignedHeaders=host&X-Amz-Expires=9&X-Amz-Credential=AKIA...&X-Amz-Signature=313c23d9..."}
```

### Step 5: Download from the S3 presigned URL

Extract the `location` field and download:

```bash
URL=$(curl -s "https://sam.gov/api/prod/opps/v3/opportunities/<oppId>/resources/download/zip?api_key=null" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://sam.gov/" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['location'])")

curl -sL -o ~/sources-sought-responses/raw/<notice-id>/attachments.zip "$URL"
```

**Note:** The S3 presigned URL has a short expiration (9 seconds). Download immediately after fetching the redirect URL.

### Step 6: Extract and parse

```bash
cd ~/sources-sought-responses/raw/<notice-id>/
unzip -o attachments.zip
ls -la

# Parse PDFs
pdftotext -layout SSN_*_PWS.pdf - | head -500
pdftotext -layout RFI_*_Synopsis.pdf -
```

## Individual File Download

To download individual files instead of the zip, the API pattern is similar but uses `/resources/download/file?resourceId=<id>`. The zip is more convenient for multiple attachments.

## Why Curl Alone Doesn't Work

Direct curl to the SAM.gov API returns HTTP 200 with `content-length: 0` — an empty body. The API server-side (istio-envoy + CloudFront) seems to require client-side JavaScript execution context (cookies, headers set by the SPA) that curl can't replicate. The browser-based interception bypasses this by piggybacking on the authenticated browser session.

**⚠️ Individual file download endpoint returns 0-byte.** The `/api/prod/file/opps/v3/opportunities/{oppId}/resources/{resourceId}` endpoint returns HTTP 200 with `content-length: 0` when called from curl OR browser fetch without an authenticated SAM.gov session. The `/api/prod/s3/opps/v3/...` variant behaves identically (200, 0 bytes). The resources LIST API (`/api/prod/opps/v3/opportunities/{oppId}/resources?api_key=null`) works fine without auth and returns attachment metadata including resource IDs — but the download itself is gated. **Use the zip endpoint (`/resources/download/zip`), not individual file endpoints.** The zip path returns a JSON redirect with a presigned S3 URL that works without authentication. If the zip endpoint also fails, do not burn more than 3-4 attempts on PDF access — cross-reference with OrangeSlices/GovTribe/USASpending and deliver with what you have.

## Fallback: Whole-Page pdftotext

If the API interception fails (e.g., SAM.gov changes their API), the snapshot-based text extraction from the SAM.gov description field is a sufficient fallback for the Synopsis. The PWS/SOW can often be found as a PDF in the zip — if the zip download works but individual PDF parsing fails, use `pdftotext -layout` locally.

## Credential Notes

- No SAM.gov API key is needed (`api_key=null` works)
- No login needed (the endpoint serves public attachments without auth)
- The browser session provides the necessary cookies for the API call
- The S3 URL is fully public (AWS Signature V4 presigned URL)