---
name: openrouter-image-gen
description: Generate images through OpenRouter API when the configured image_generate tool fails or is unavailable. Covers model discovery, chat-completions-based image generation, base64 extraction, and known-working models.
---

# OpenRouter Image Generation

Fallback pattern for generating images when `image_generate` hits billing limits, quota errors, or provider issues. Uses OpenRouter's chat completions API with `modalities: ["image"]` directly via curl/Python.

## When to Use

- `image_generate` returns a 400/402/429 billing or quota error
- User specifically asks to use an OpenRouter model for image gen
- You need image output from a non-default model (e.g. x-ai/grok-imagine, google/gemini-3.1-flash-image)

## Prerequisites

- `OPENROUTER_API_KEY` set in environment or `.zshrc`
- The key must have credit for the model you're targeting

## Model Discovery

Find image-capable models:

```bash
curl -s "https://openrouter.ai/api/v1/models?output_modalities=image" \
  -H "Authorization: Bearer $OPENR...EY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in data.get('data', []):
    name = m.get('id','?')
    pricing = m.get('pricing', {})
    cost = pricing.get('image', '?')
    mods = m.get('architecture', {}).get('output_modalities', [])
    print(f'{name} | image cost: {cost} | output: {mods}')
"
```

Known-working image-generation models (verified June 2026):

| Model | Cost/image | Output Modality | Notes |
|-------|-----------|-----------------|-------|
| `x-ai/grok-imagine-image-quality` | $0.01 | `["image"]` | Good for illustrative/artistic — used for tattoo flash |
| `google/gemini-3.1-flash-image` | Free tier | `["image","text"]` | Fast, cheap, supports extended aspect ratios |
| `google/gemini-3-pro-image` | $0.000002 | `["image","text"]` | Higher quality, supports text+image output |
| `openai/gpt-image-2` | varies | `["image"]` | Same as configured `image_gen` tool — same billing limits apply |

## Key: Output Modality Matters

Models fall into two categories — send the WRONG `modalities` value and you get a 404 error:

### Image-Only Output (`["image"]`)
Used by: `x-ai/grok-imagine-image-quality`, `openai/gpt-image-2`, `black-forest-labs/flux.2-klein-4b`

```json
{
  "model": "x-ai/grok-imagine-image-quality",
  "messages": [{"role": "user", "content": "prompt here"}],
  "modalities": ["image"],
  "image_config": {
    "aspect_ratio": "3:4",
    "image_size": "1K"
  }
}
```

### Text+Image Output (`["image", "text"]`)
Used by: `google/gemini-3.1-flash-image`, `google/gemini-3-pro-image`

```json
{
  "model": "google/gemini-3.1-flash-image",
  "messages": [{"role": "user", "content": "prompt here"}],
  "modalities": ["image", "text"],
  "image_config": {
    "aspect_ratio": "1:1",
    "image_size": "1K"
  }
}
```

**Rule:** Send `["image"]` for image-only models, `["image","text"]` for multimodal models. Sending the wrong value returns HTTP 404 with "No endpoints found that support the requested output modalities."

## Extracting and Saving Images

Images come back as base64 data URLs in `response.choices[0].message.images[].image_url.url`:

```python
import json, base64, os, urllib.request

payload = {
    "model": "x-ai/grok-imagine-image-quality",
    "messages": [{"role": "user", "content": prompt}],
    "modalities": ["image"],
    "image_config": {"aspect_ratio": "3:4", "image_size": "1K"}
}

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
)
resp = json.loads(urllib.request.urlopen(req).read().decode())

msg = resp['choices'][0]['message']
url = msg['images'][0]['image_url']['url']  # data:image/jpeg;base64,...
b64 = url.split(',', 1)[1]
raw = base64.b64decode(b64)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'wb') as f:
    f.write(raw)
```

Response structure for verification:

```python
# Keys in response: ['id', 'object', 'created', 'model', 'provider', 'system_fingerprint', 'service_tier', 'choices', 'usage']
# Message keys: ['role', 'content', 'refusal', 'reasoning', 'images']
# Image keys: ['type', 'image_url']
# image_url is a dict: {'url': 'data:image/jpeg;base64,...'}
```

## Flux Models: Images/Generations Endpoint

Models like `black-forest-labs/flux.2-klein-4b` and `black-forest-labs/flux.2-pro` appear in the model list with `output_modalities: ["image"]` but **do NOT work with the chat completions endpoint**. Use the `/v1/images/generations` endpoint instead:

```python
payload2 = {
    "model": "black-forest-labs/flux.2-klein-4b",
    "prompt": prompt,
    "n": 1,
    "size": "1024x1024"
}
req2 = urllib.request.Request(
    "https://openrouter.ai/api/v1/images/generations",
    data=json.dumps(payload2).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
)
resp2 = json.loads(urllib.request.urlopen(req2, timeout=90).read().decode())
if 'data' in resp2 and resp2['data']:
    url = resp2['data'][0].get('url', '')
    if url.startswith('data:'):
        b64 = url.split(',', 1)[1]
        raw = base64.b64decode(b64)
    elif url.startswith('http'):
        raw = urllib.request.urlopen(url).read()
```

**Detection pattern:** When chat completions with `modalities: ["image"]` returns HTTP 404, try images/generations as a fallback — Flux/Stable Diffusion style models use this endpoint.

## Reusable Script

The file `scripts/gen_openrouter_image.py` provides a complete reusable implementation with key extraction, automatic chat-completions → images/generations fallback, base64/HTTP URL handling, and error management.

```bash
python3 ~/.hermes/skills/openrouter-image-gen/scripts/gen_openrouter_image.py \\
  "x-ai/grok-imagine-image-quality" \\
  "your prompt here" \\
  "/path/to/output.jpg"
```

## Post-Generation: File Ownership

After saving images via Python, files are owned by `root:staff` with `-rw-------` perms. Fix before serving via http.server:

```bash
chown amynporb:staff /path/to/images/*.jpg
chmod 644 /path/to/images/*.jpg
```

The http.server daemon returns 403 on 600-permission files.

## Prompt Engineering for Character-Specific Imagery

### The core problem

Diffusion models often don't know obscure characters or specific IP iterations (e.g., BTAS Harley Quinn vs. New 52 vs. Suicide Squad). Referencing the character by name can produce a generic or wrong version. This is especially common with comic/anime characters where the model conflates multiple design iterations.

### The fix: Describe visual elements directly

**Don't rely on the character name alone.** Describe every visual identifier as if the model has never seen the character. The prompt that worked in this session for a recognizable BTAS Harley Quinn:

```
Weak prompt (produces generic output):
"Harley Quinn Queen of Hearts playing card tattoo"

Strong prompt (produces recognizable output):
"Tattoo flash, black and grey. Queen of Hearts playing card. Center portrait of a female jester with: pure white painted face, black domino mask pointed at the temples, bright red lips smirk, vivid blue eyes visible through mask holes. Blonde hair in two puffy pigtails with red ribbon on one side, blue ribbon on the other. On her head is a red and black jester hat with two horns pointing up, each tipped with a gold bell. She wears a classic red and black jester bodysuit covered in diamond patterns. A white ruffled collar. Bold outlines. No color."
```

### Prompt architecture rules (tattoo/illustration focus)

1. **Start with medium:** "Tattoo flash, black and grey" or "Digital art"
2. **State the format:** "Queen of Hearts playing card" or "Full body portrait"
3. **Describe the face** (most critical for recognizable characters): skin color, eye mask shape, lip shape/makeup
4. **Describe hair:** style, color, accessories (color of ties/bands matters)
5. **Describe headwear** (often the most distinctive identifier): hat shape, colors, bells, points
6. **Describe costume:** bodysuit/outfit, pattern (diamonds, stripes, etc.), collar
7. **Describe props/accessories** if relevant (mallet, heart, diamond)
8. **State style constraints:** "Bold black outlines. Pure black and grey shading. No color."
9. **Repeat key constraints at the end** — models attend better to final tokens

### Verification & iteration

After generating, use `vision_analyze` to check the output contains all requested visual elements:

```
Call vision_analyze on the generated image
Ask: "Does this image contain [specific element]? List which requested details are present and which are missing."
```

**This verification step is mandatory when generating character-specific imagery.** If key elements are missing, iterate the prompt — add more detail about the missing element, or remove distracting elements. Do NOT switch to a different image creation approach (SVG drawing, reference-only, text descriptions) unless the user explicitly asks for that. Keep iterating on the image gen prompt. The user will tell you when it's close enough to take to an artist.

### Iterative refinement workflow for creative concepts

When generating multiple concept images for a creative brief (tattoo designs, logos, illustrations):

1. **Generate 3-5 variations** in parallel with slightly different prompts
2. **Check each with vision_analyze** — identify what works and what doesn't
3. **Share the best results** with the user via HTML gallery
4. **Incorporate user feedback into the next round** — if they say "no color" → add "pure black and grey. No color" to every subsequent prompt. If they say "doesn't look like the character" → describe the character's specific visual elements in more detail.
5. **Keep generating until the user says it's right** — this is an iterative process, not a one-shot task

**Important behavioral rule:** NEVER fall back to SVG drawing, ASCII art, text-only descriptions, or hand-drawn schematics as a substitute for image generation when the user asked for images. If image gen models can't produce what the user wants, tell them honestly ("this model can't capture that specific face") and suggest alternatives (different model, reference images, commissioning an artist). Do not silently switch to a different output format.

### Tattoo-specific prompting notes

- **Black and grey:** Say "pure black and grey. No color" twice — once in the aesthetic description and once as a final constraint
- **Bold outlines:** Add "bold black outlines. Clean sharp linework." — tattoo flash needs defined edges
- **Paper background:** "On cream paper. Tattoo flash style." — helps the model produce the right aesthetic
- **Avoid "realistic" or "photo"** for tattoo designs — it triggers photorealism instead of illustration/tattoo flash
- **x-ai/grok-imagine-image-quality** works well for tattoo/illustration styles but struggles with exact character faces — describe the face in detail
- **When the user rejects a round, capture their exact words and embed them in the next prompt** — e.g., "they said it doesn't look like [character]. Add [specific visual elements they mentioned]."

## When Image Generation Fails Entirely

If all image gen models return errors (billing limits, 404s, rate limits) and the user still wants visual output:

1. **Report the blocker honestly** — tell the user which models failed and why
2. **Suggest alternatives** — reference image galleries (real photos/art found via web search), commissioning a human artist, or trying a different API provider
3. **Do NOT produce SVGs, ASCII art, or text descriptions as a substitute** unless the user explicitly asks for them. The user in this session was strongly frustrated by SVG output when they wanted image generation. SVG is a design tool for an artist, not a replacement for visual output.

## Pitfalls

- **x-ai/grok-imagine returns empty imageUrl if modalities is wrong** — use `["image"]` not `["image","text"]` for Grok and Flux models
- **OpenAI billing limits persist** — if OpenAI's own `image_generate` tool fails, `openai/gpt-image-2` on OpenRouter will also fail (same billing)
- **Rate limits** — OpenRouter image models can be rate-limited. Retry with exponential backoff if you get 429
- **Gemini free tier** — `google/gemini-3.1-flash-image` on free tier has low rate limits. Use `google/gemini-3-pro-image` ($0.000002/image) for reliable service
- **Key sourcing** — `OPENROUTER_API_KEY` in `.zshrc` may use `***` masking. Use grep/sed to extract: `grep 'OPENROUTER_API_KEY=' ~/.zshrc | sed 's/.*="//;s/"//'`
- **No text response from image-only models** — `content` will be `None` when you use `["image"]` modality. Only the images array has data
- **HTTP 404 on chat-completions is ambiguous** — could mean wrong modality OR model doesn't support the endpoint. Try images/generations as a second resort
