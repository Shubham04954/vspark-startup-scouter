"""
scouter_engine.py — Gemini-powered scouting engine.

Takes a startup name (or deck text, or other input) and returns a fully
populated row-dict matching the format expected by write_scouter.py and
write_analyzed.py.

Uses Gemini 2.5 Flash with the google_search grounding tool so the model
has real-time web access. The rubric is loaded from the rubric/ folder
and stitched into the system prompt at startup.

Returns two dicts per startup:
  - scouter_row: the 19-column breakdown for New_Startup_Scouter sheet
  - analyzed_row: the 7-column executive line for Analyzed Startups sheet
"""

import os
import json
import re
from pathlib import Path
from typing import Optional

import google.generativeai as genai


RUBRIC_DIR = Path(__file__).parent.parent / "rubric"


def load_rubric_context() -> str:
    """Concatenate all rubric files into a single context block."""
    sections = []
    files_in_order = [
        "bu_profiles.md",
        "credibility_flags.md",
        "cross_bu_routing.md",
        "csr_esg_routing.md",
        "rubric_examples.md",
        "colour_rules.md",
    ]
    for fname in files_in_order:
        path = RUBRIC_DIR / fname
        if path.exists():
            sections.append(f"=== {fname} ===\n\n{path.read_text(encoding='utf-8')}")
    return "\n\n---\n\n".join(sections)


SYSTEM_PROMPT = """You are scouting startups for the Vedanta Spark (V-Spark) engagement at Accenture Strategy IMU. Your output: a structured assessment of one startup, in JSON, ready to be written into the Ventures_Tracker workbook.

# Your job

For the given startup, you must:

1. **Verify identity** — search MCA, Tracxn, company website, LinkedIn, news. If zero web footprint, return `insufficient_data: true`. If multiple companies match the name, return `ambiguous: true` with the candidates.

2. **Apply is-this-a-startup filter** — reject NGOs, accelerators, consulting firms, university labs, govt bodies, established corporates (>15 yrs OR >₹100 Cr revenue), franchise/agency. Mark these as 🚩 Not a Startup.

3. **Run credibility audit** — flag founder/MCA mismatches, implausible revenue-to-customer ratios, pivot incoherence, partner logo duplication, registry-agent emails, date inconsistencies, self-claimed credentials.

4. **BU-fit assessment** — for each of the 7 Vedanta BUs (BALCO, VAL-L, VAL-J, ESL, HZL, Cairn, IOB), output ✅ Strong / ⚠️ Possible / ❌ No Fit + concise one-liner naming the specific use case at a named site or process.

5. **Three routing axes** — independently evaluate Cross-BU fit and CSR/ESG fit. These do NOT elevate non-fits to ⚠️; they just route them.

6. **Verdict synthesis** — lead with three badges (Rating | Cross-BU | CSR/ESG) then ≤40 words rationale.

# Hard rules — non-negotiable

1. **Do not invent** founder names, CINs, funding figures, customers, partnerships. If unverifiable: write "Not surfaced in search" and flag in verdict.
2. **Do not auto-elevate** based on Cross-BU/CSR routability. A consumer D2C is still ❌ for BU ops.
3. **Do not generic-tag** "⚠️ Possible" for all 7 BUs. If all match generically, the startup is non-industrial → ❌.
4. **Do not soften** credibility flags.
5. **Do not include** Kayad (HZL), Cambay (Cairn — PSC rejected Sept 2025), Goa (IOB — SC suspension), Vizag (HZL — suspended Feb 2012) as active sites.
6. **Do not use named individuals** in Engagement Owner. Generic Group function names only.
7. **Do not invent URLs.** Every URL written into Website (E) and LinkedIn (F) MUST come from a search result you actually saw:
    - Website: `https://<root domain>` only, single URL
    - LinkedIn: ONE URL only — Company page if surfaced > Founder if not > BLANK if neither
    - LinkedIn slugs do NOT match company names. Bubble Me's company page is `bubbleme-india`, not `bubbleme`. If you didn't see the URL in search, leave blank.

# Length caps (hard)

- `capabilities`: ≤25 words
- BU cells (`balco`, `val_l`, `val_j`, `esl`, `hzl`, `cairn`, `iob`): ≤18 words each
- `verdict`: ≤40 words AFTER the badge line
- `analyzed_action`: ≤35 words
- `analyzed_rationale`: ≤40 words

# Output format

Return EXACTLY this JSON, nothing else (no markdown fences, no prose):

```json
{
  "insufficient_data": false,
  "ambiguous": false,
  "ambiguous_candidates": [],
  "scouter_row": {
    "name": "Startup Name",
    "indian": "✅ Yes",
    "website": "https://startup.com",
    "linkedin": "https://linkedin.com/company/startup",
    "founded": "2023, MCA CIN: U...",
    "location": "City, State",
    "funding": "Funding history + ecosystem backing + flags",
    "founders": "Names + pedigree, MCA-verified",
    "team_size": "Small / Mid / 10-15",
    "capabilities": "One-liner, ≤25 words",
    "balco": "❌ No Fit",
    "val_l": "❌ No Fit",
    "val_j": "❌ No Fit",
    "esl": "❌ No Fit",
    "hzl": "✅ Strong — specific use case at named site",
    "cairn": "❌ No Fit",
    "iob": "❌ No Fit",
    "verdict": "✅ STRONG | Cross-BU — | CSR/ESG —\\n40-word rationale here"
  },
  "analyzed_row": {
    "tier": "P1 – Immediate",
    "company": "Startup Name",
    "bu": "HZL / IOB",
    "action": "Pilot at <site> for <use case>. <Validate condition>.",
    "owner": "HZL Mines",
    "rationale": "Why this tier + key context, ≤40 words"
  }
}
```

# Canonical Priority Tiers (use exactly these)

- `P1 – Immediate`
- `P1 – Immediate (Strategic)`
- `P2 – BU-specific`
- `P2 – Conditional BU Evaluation`
- `P2 – Platform / Enabler (Conditional)`
- `P3 – Conditional / Procurement-led`
- `Deprioritise (CSR / Central only)`
- `Deprioritise`

# Canonical Engagement Owners (generic only)

BU: `HZL Mines`, `HZL Smelters`, `HZL Mines + Smelters`, `BALCO`, `ESL`, `Cairn`, `IOB`, `VAL-L`, `VAL-J`
V-Spark: `V-Spark / Data Platform`, `Energy Mgmt`, `R&D`, `Knowledge Hub`, `BU Ops / CSR`
Group: `Group Procurement`, `Group Legal`, `Group CISO`, `Group Sustainability`, `Group CTO / Digital`, `Group HR / L&D`, `Group OHC`, `Group Quality / Compliance`, `Foundation / CSR`

If `insufficient_data: true` or `ambiguous: true`, set `scouter_row` and `analyzed_row` to `null`.

# Reference context

The following sections give you the BU profiles, credibility flag patterns, routing rules, examples, and colour rules. Use them as the authoritative source for your assessment.

---

"""


def configure_gemini(api_key: str):
    """Configure Gemini client with the given API key."""
    genai.configure(api_key=api_key)


def get_model():
    """Return a Gemini model configured with system prompt + grounding."""
    rubric = load_rubric_context()
    full_system = SYSTEM_PROMPT + rubric

    # Use 2.5 Flash for cost / quota friendliness; switch to 2.5-pro if needed
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=full_system,
        # google_search tool gives real-time web access
        tools="google_search_retrieval",
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,  # low temp for consistency
            response_mime_type="application/json",
        ),
    )
    return model


def parse_json_response(text: str) -> dict:
    """Parse Gemini's response — strip code fences if any, parse JSON."""
    # Strip ```json ... ``` fences if present
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*$", "", text.strip())
    text = text.strip()
    return json.loads(text)


def scout_startup(
    name: str,
    api_key: str,
    extra_context: Optional[str] = None,
) -> dict:
    """Scout a single startup. Returns the parsed JSON response.

    Args:
        name: Startup name to scout.
        api_key: Gemini API key.
        extra_context: Optional extra info (e.g. user-provided URL, deck text).

    Returns:
        dict with keys: insufficient_data, ambiguous, scouter_row, analyzed_row
    """
    configure_gemini(api_key)
    model = get_model()

    user_prompt = f"Scout this startup for V-Spark: **{name}**"
    if extra_context:
        user_prompt += f"\n\nAdditional context provided by user:\n{extra_context}"

    user_prompt += (
        "\n\nReturn the JSON exactly as specified. No prose. No markdown fences. "
        "Just the JSON object."
    )

    response = model.generate_content(user_prompt)
    text = response.text

    try:
        result = parse_json_response(text)
    except json.JSONDecodeError as e:
        # Save the raw response for debugging; return insufficient_data
        return {
            "insufficient_data": True,
            "ambiguous": False,
            "ambiguous_candidates": [],
            "scouter_row": None,
            "analyzed_row": None,
            "_raw_response": text[:500],
            "_error": f"JSON parse error: {e}",
        }

    return result


def scout_from_deck_text(
    deck_text: str,
    api_key: str,
) -> dict:
    """Scout a startup using extracted deck text as primary source.

    The model is instructed to cross-check claims via web search but use the
    deck as the canonical product/team description.
    """
    configure_gemini(api_key)
    model = get_model()

    user_prompt = (
        "I have a pitch deck for a startup. Use this deck text as the primary "
        "source for product, team, traction. Cross-check via web search for "
        "credibility flags (MCA, funding, founder LinkedIn, customer claims). "
        "Then return the standard JSON.\n\n"
        f"--- DECK TEXT BEGINS ---\n{deck_text}\n--- DECK TEXT ENDS ---\n\n"
        "Return the JSON exactly as specified. No prose. No markdown fences."
    )

    response = model.generate_content(user_prompt)
    try:
        return parse_json_response(response.text)
    except json.JSONDecodeError as e:
        return {
            "insufficient_data": True,
            "ambiguous": False,
            "ambiguous_candidates": [],
            "scouter_row": None,
            "analyzed_row": None,
            "_raw_response": response.text[:500],
            "_error": f"JSON parse error: {e}",
        }


def extract_names_from_image(image_bytes: bytes, api_key: str) -> dict:
    """Extract startup names from an uploaded infographic / screenshot.

    Returns:
        {
          "names": [{"name": str, "confidence": "high|medium|low", "note": str}, ...]
        }
    """
    configure_gemini(api_key)
    # Use vision-capable model
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        "Look at this image. It contains startup names and/or logos (e.g. an Inc42 infographic, "
        "LinkedIn post, slide deck page, or similar). List every startup name you can identify.\n\n"
        "For each name, classify confidence:\n"
        "- high: name is clearly readable, no doubt\n"
        "- medium: best-effort read but logo is small / partially obscured\n"
        "- low: cannot read clearly (covered, blurred, unreadable font)\n\n"
        "Return STRICTLY this JSON (no markdown, no prose):\n"
        "{\"names\": [{\"name\": \"...\", \"confidence\": \"high|medium|low\", \"note\": \"...\"}]}"
    )

    response = model.generate_content(
        [
            {"mime_type": "image/png", "data": image_bytes},
            prompt,
        ],
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    try:
        return parse_json_response(response.text)
    except json.JSONDecodeError:
        return {"names": [], "_error": "Could not parse vision response"}
