# V-Spark Startup Scouter

A web tool for scouting startups for the **Vedanta Spark (V-Spark)** engagement at Accenture Strategy IMU.

Drops a startup name (or image/deck/Excel/tracker) → returns a populated `Ventures_Tracker.xlsx` workbook with:
- **`New_Startup_Scouter`** — detailed 19-column breakdown (founders, funding, BU fit per Vedanta site, credibility flags, verdict with badges)
- **`Analyzed Startups`** — concise 7-column executive output (priority tier, recommended action, engagement owner, rationale)

Built on **Gemini 2.5 Flash** with `google_search` grounding for real-time web research, deployed on **Streamlit Community Cloud**.

---

## Quick start (deployment)

### Step 1 — Get a Gemini API key (free tier)

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with a Google account
3. Click **Create API key** → choose "Create API key in new project" if you don't have one
4. Copy the key (starts with `AIza...`)
5. Free-tier limits: ~10 requests/minute, ~1500/day on Flash. Plenty for V-Spark volume.

### Step 2 — Push this repo to GitHub

1. Create a new GitHub repo: `vspark-startup-scouter`
2. Push these files:
   ```
   git init
   git add .
   git commit -m "initial commit"
   git remote add origin https://github.com/<your-username>/vspark-startup-scouter.git
   git push -u origin main
   ```

### Step 3 — Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io
2. Sign in with the same GitHub account
3. Click **New app**
4. Select repo `vspark-startup-scouter`, branch `main`, file `app.py`
5. Under **Advanced settings → Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "AIza...your-key-here..."
   ```
6. Click **Deploy**
7. Wait ~2 minutes; you'll get a URL like `https://vspark-startup-scouter.streamlit.app`

### Step 4 — Test

1. Open your app URL
2. Enter `xTerra Robotics` in the textbox
3. Click "Run scouting"
4. Verify: progress shows search, summary counters update, downloadable .xlsx appears
5. Open the downloaded file: should have Xterra row in both sheets, P1 – Immediate, HZL/IOB

---

## Local development

```bash
git clone https://github.com/<your-username>/vspark-startup-scouter.git
cd vspark-startup-scouter
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
export GEMINI_API_KEY="AIza..."
streamlit run app.py
```

Visit http://localhost:8501

---

## Architecture

```
┌──────────────────────────────┐
│  app.py (Streamlit UI)       │
│  - Mode picker               │
│  - Tracker upload (optional) │
│  - Progress / counters       │
│  - Download                  │
└─────────────┬────────────────┘
              │
   ┌──────────┴───────────┐
   │                      │
   ▼                      ▼
scouter_engine.py   scripts/write_*.py
(Gemini calls)      (openpyxl writes)
   │                      │
   ├──> rubric/*.md       ├──> assets/template.xlsx
   │   (system prompt)    │
   │                      │
   ▼                      ▼
Gemini 2.5 Flash    New_Startup_Scouter +
+ google_search     Analyzed Startups sheets
```

### Files

| File | Role |
|---|---|
| `app.py` | Streamlit UI, orchestrates the flow |
| `scouter_engine.py` | Wraps Gemini API calls; handles single-name / image / deck inputs |
| `scripts/write_scouter.py` | Writes detailed rows into `New_Startup_Scouter` |
| `scripts/write_analyzed.py` | Writes concise rows into `Analyzed Startups` |
| `rubric/*.md` | The V-Spark scouting rubric — loaded into Gemini's system prompt |
| `assets/ventures_tracker_template.xlsx` | Blank template used when no tracker uploaded |
| `requirements.txt` | Python dependencies |

---

## Updating the rubric

When Vedanta site list changes, BU pain points evolve, or new credibility patterns emerge:

1. Edit the relevant file in `rubric/`:
   - `bu_profiles.md` — Vedanta sites + operational pain points
   - `cross_bu_routing.md` — Group function routing
   - `csr_esg_routing.md` — Foundation / ESG routing
   - `credibility_flags.md` — audit checklist
   - `rubric_examples.md` — worked examples
   - `colour_rules.md` — formatting rules
2. Commit and push to GitHub
3. Streamlit auto-redeploys in ~30 seconds — no manual action needed

---

## Cost & quota

**Free tier**: Gemini 2.5 Flash gives ~1500 free requests/day. Each scout = 1 request. So 1500 scouts/day free, which is several months of V-Spark volume.

**If you exceed quota**: Gemini falls back to billing if you've added a payment method. ~$0.025 per scout at paid rates. 100 scouts = $2.50.

**Streamlit hosting**: Free forever for this app size. App sleeps after 7 days of inactivity, wakes in ~30 seconds.

---

## What's NOT included (by design)

- No login / auth — public URL access
- No history / past-scouts page — every session is fresh
- No in-app editing of the tracker — output is downloaded as Excel
- No retry-individual-row UI — re-run the failing startup separately
- No persistent storage — all processing in-memory; downloaded file is the only artifact

---

## Support

Built by Shubham (Accenture Strategy IMU intern, V-Spark engagement, IIM Ahmedabad PGP).

For rubric / scouting issues: edit `rubric/*.md` and push.
For UI / engine issues: edit `app.py` or `scouter_engine.py` and push.
