# Deployment guide — V-Spark Startup Scouter

End-to-end steps to get your web app live. ~30 minutes total. No prior experience with Streamlit / Gemini needed.

---

## What you'll have at the end

A web URL like `https://vspark-startup-scouter.streamlit.app` that anyone (you, Sumit, Nitin, future interns) can open in a browser. No installation, no Claude account needed. Type a startup name → get a populated `Ventures_Tracker.xlsx`.

---

## Prerequisites

You need three free accounts. If you don't already have them:

1. **GitHub account** — https://github.com (free, ~2 minutes to create)
2. **Google account** — for the Gemini API key (you almost certainly have one)
3. **Streamlit Community Cloud account** — https://share.streamlit.io (sign in with the GitHub account from step 1, ~30 seconds)

---

## Step 1 — Get a Gemini API key (3 minutes)

1. Open https://aistudio.google.com/app/apikey in a new tab
2. Sign in with your Google account
3. Click the **Create API key** button (top-right)
4. If prompted, choose **"Create API key in new project"**
5. A key starting with `AIza...` will appear. **Copy it now** and paste into a Notes app — you'll need it in step 4
6. (Free tier limits: 1,500 requests/day on Flash. You won't hit this with V-Spark volume.)

---

## Step 2 — Push the bundle to GitHub (10 minutes)

The bundle is the `vspark-webapp.zip` file that came with this conversation.

### Option A: Use GitHub web UI (easiest, no command line)

1. Download `vspark-webapp.zip` from the chat outputs
2. Unzip it locally — you'll get a `vspark-webapp/` folder with files inside
3. Go to https://github.com → click **+** (top-right) → **New repository**
4. Repository name: `vspark-startup-scouter`
5. Visibility: **Public** (Streamlit Community Cloud free tier requires public repos)
6. ✅ Check "Add a README file" — uncheck this if it's already in the bundle (it is)
7. Click **Create repository**
8. On the new empty repo page, click **uploading an existing file** (it's a link in the welcome text)
9. Drag every file/folder from your unzipped `vspark-webapp/` folder into the upload area:
   - `app.py`
   - `scouter_engine.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `rubric/` folder (with all 6 .md files inside)
   - `scripts/` folder (with both .py files inside)
   - `assets/` folder (with template.xlsx inside)
10. Scroll down → write commit message: `initial deploy` → click **Commit changes**
11. Wait ~30 seconds for upload to finish. Refresh the repo page; you should see all files listed

### Option B: Use git command line (faster if you're comfortable)

```bash
unzip vspark-webapp.zip
cd vspark-webapp
git init
git add .
git commit -m "initial deploy"
gh repo create vspark-startup-scouter --public --source=. --push
# (or manually create the repo on github.com and: git remote add origin <url> && git push -u origin main)
```

---

## Step 3 — Deploy on Streamlit Community Cloud (5 minutes)

1. Open https://share.streamlit.io
2. Click **Sign in with GitHub** (top-right) — authorise Streamlit to access your repos
3. Click the big blue **Create app** button (or "New app")
4. Select **Deploy a public app from GitHub**
5. Fill the form:
   - **Repository**: `<your-username>/vspark-startup-scouter`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: leave default OR customise (e.g. `vspark-scouter` → gives you `vspark-scouter.streamlit.app`)

6. **Don't click Deploy yet.** Click **Advanced settings...** at the bottom

7. Under **Secrets**, paste exactly this (replacing `AIza...` with the key you copied in step 1):
   ```toml
   GEMINI_API_KEY = "AIzaSy...your-actual-key-here..."
   ```
   (Keep the quotes around the key. The line starts with `GEMINI_API_KEY = `, no leading whitespace.)

8. Click **Save** in the secrets popup

9. Click **Deploy!**

10. Wait. The app builds — takes 2-5 minutes the first time (installs Python packages). You'll see a log streaming on the right. When it says `You can now view your Streamlit app...`, you're live.

---

## Step 4 — Test (5 minutes)

Your app URL is now live. Test it.

### Test 1: Single startup by name

1. Open the URL in a new tab
2. Step 1: leave "Type names" selected, enter `xTerra Robotics` in the textbox
3. Step 2: skip (no tracker upload)
4. Click **Run scouting**
5. Wait ~20 seconds; you should see:
   - Progress: `⏳ xTerra Robotics — searching...` then `✅ xTerra Robotics — P1 – Immediate`
   - Summary: `Scouted 1/1 · P1: 1 · P2: 0 · P3: 0 · Skip/?: 0`
   - Green "Done. Added 1 entries..." message
   - Download button appears
6. Click **Download Ventures_Tracker.xlsx**
7. Open the file. Verify:
   - **`New_Startup_Scouter`** sheet has 1 row with Xterra populated across all 19 columns, ✅ green on HZL and IOB cells
   - **`Analyzed Startups`** sheet has 1 row with Tier `P1 – Immediate`, BU `HZL / IOB`, Owner `HZL Mines`
   - Website cell is a clickable hyperlink (blue, underlined)
   - LinkedIn cell is a clickable hyperlink

If all that works → ✓ deployment is good.

### Test 2: Image upload

1. New session in the app
2. Step 1: switch to **Upload image**
3. Drag in the Inc42 "30 Startups To Watch" infographic from earlier
4. Wait for name extraction
5. Confirm the names you want scouted by ticking checkboxes
6. Click **Run scouting**
7. Watch progress. Should take ~10-15 seconds per startup. Batch of 10 = ~2 minutes.
8. Download and verify

### Test 3: Append to your live tracker

1. New session
2. Step 1: enter a couple of names
3. Step 2: drag in your real `Ventures_Tracker.xlsx` (the one with all your existing entries)
4. Click Run
5. Download. Verify your existing 68+ entries are still there + new ones appended at the bottom of both sheets

---

## Step 5 — Share the URL

Once you're happy with the output:

- Send the URL to Sumit / Nitin / your team
- They open it in any browser (no login, no install)
- They scout startups themselves OR send you the URL when they want one done

Bookmark it. The URL is permanent unless you change the app name in Streamlit settings.

---

## Step 6 — Maintaining the app

When something needs updating (Vedanta site list changes, new credibility pattern, BU profile drift):

1. Open your GitHub repo in a browser
2. Navigate to the file you want to edit (e.g. `rubric/bu_profiles.md`)
3. Click the pencil icon (top-right of the file viewer) to edit in-browser
4. Make changes
5. Scroll down → write commit message → **Commit changes**
6. Streamlit detects the change automatically and redeploys in ~30 seconds. No manual action needed.

---

## Troubleshooting

### "Failed to install requirements" during deploy

- Streamlit Cloud got tripped up. Edit `requirements.txt` and pin a working version. Common fix: change `streamlit>=1.30.0` to `streamlit==1.39.0`.
- Push the change → auto-redeploys.

### "GEMINI_API_KEY not configured"

- The secret didn't save properly. In Streamlit dashboard → your app → **⋮ menu → Settings → Secrets** → re-paste:
  ```toml
  GEMINI_API_KEY = "AIzaSy..."
  ```
- Click Save. The app reboots automatically.

### "JSONDecodeError" when scouting

- Gemini occasionally returns malformed JSON. The app tries to recover. If it persists for one specific startup:
  - That startup might have ambiguous data
  - Try giving it more context: type `Xterra Robotics by IIT Kanpur` instead of just `Xterra Robotics`

### App is slow / sleeping

- After 7 days of inactivity, free-tier Streamlit apps go to sleep
- First visit after sleep takes ~30 seconds to wake up. Just wait
- Once awake, it stays awake while in use

### Quota exceeded

- 1500 requests/day on free tier. If you hit this:
  - Wait until next day (resets at midnight UTC)
  - OR add a payment method to your Google Cloud project ($2-3/month at V-Spark volume)

### Image extraction returns wrong names

- Inc42-style infographics are usually fine
- LinkedIn screenshots with text overlays / cursor artifacts can confuse the model
- Use the confirmation checkboxes to fix any wrong reads before scouting

### Output workbook columns are blank when opened

- This was a bug in earlier versions; should be fixed in this one
- If it recurs: right-click row 5 in Excel → Unhide
- Tell me so I can patch the writer script

---

## Future enhancements (not in v1)

When you have time, things worth adding:
- **Login/allowlist** so only verified users can scout (prevents quota abuse if URL leaks)
- **Past scouts history** stored in a lightweight DB (SQLite or Streamlit's session state)
- **Inc42 / VentureBeat RSS scraper** that auto-pulls new lists weekly
- **Slack integration** that pings you when a new ✅ Strong scout is found
- **Cost dashboard** showing Gemini token usage / monthly cost

For any of these, just tell me what you want and I'll send a follow-up bundle.
