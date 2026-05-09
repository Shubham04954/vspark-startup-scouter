"""
V-Spark Startup Scouter — Streamlit web app.

Single-page tool that takes any of {name | image | deck PDF | excel | live tracker}
and returns a populated Ventures_Tracker.xlsx workbook with two sheets:
  - New_Startup_Scouter: detailed 19-column breakdown
  - Analyzed Startups: concise 7-column executive output

Uses Gemini 2.5 Flash with google_search grounding for live web research.
"""

import io
import sys
import shutil
import tempfile
from pathlib import Path

import streamlit as st

# Path setup so we can import from scripts/
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scouter_engine import scout_startup, scout_from_deck_text, extract_names_from_image
from scripts.write_scouter import append_to_scouter
from scripts.write_analyzed import append_to_analyzed


# ---------- Setup ----------

st.set_page_config(
    page_title="V-Spark Startup Scouter",
    page_icon="🔍",
    layout="centered",
)

# Get API key from secrets (Streamlit Cloud) or env
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        import os
        return os.environ.get("GEMINI_API_KEY", "")


TEMPLATE_PATH = Path(__file__).parent / "assets" / "ventures_tracker_template.xlsx"


# ---------- Header ----------

st.title("V-Spark Startup Scouter")
st.caption("Vedanta Spark engagement · Accenture Strategy IMU")

# ---------- Validate API key early ----------

api_key = get_api_key()
if not api_key:
    st.error(
        "**Gemini API key not configured.** Set `GEMINI_API_KEY` in Streamlit secrets "
        "(Settings → Secrets) before using this app."
    )
    st.stop()


# ---------- Step 1: Input mode ----------

st.subheader("Step 1 · What do you want to scout?")

mode = st.radio(
    "Input mode",
    options=["Type names", "Upload image (Inc42 / LinkedIn / slide)", "Upload deck (PDF)", "Upload list (Excel/CSV)"],
    horizontal=True,
    label_visibility="collapsed",
)

names_input = ""
image_input = None
deck_input = None
excel_input = None

if mode == "Type names":
    names_input = st.text_area(
        "Enter startup names, one per line",
        placeholder="Xterra Robotics\nBubble Me\nClimMaTech",
        height=120,
        label_visibility="collapsed",
    )

elif mode == "Upload image (Inc42 / LinkedIn / slide)":
    image_input = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )
    if image_input:
        st.image(image_input, use_container_width=True)

elif mode == "Upload deck (PDF)":
    deck_input = st.file_uploader(
        "Upload a pitch deck",
        type=["pdf"],
        label_visibility="collapsed",
    )

elif mode == "Upload list (Excel/CSV)":
    excel_input = st.file_uploader(
        "Upload an Excel or CSV with startup names",
        type=["xlsx", "csv"],
        label_visibility="collapsed",
    )


# ---------- Step 2: Optional tracker upload ----------

st.subheader("Step 2 · Where should the output go?")
st.caption("Optional · skip to use the blank template")

tracker_file = st.file_uploader(
    "Drop your live Ventures_Tracker.xlsx here",
    type=["xlsx"],
    label_visibility="collapsed",
)


# ---------- Helper: Resolve startup list from selected input mode ----------

def resolve_startup_list():
    """Return list of startup names to scout, plus extra context per name if any."""
    items = []  # list of {"name": str, "context": str|None, "deck_text": str|None}

    if mode == "Type names":
        if not names_input.strip():
            return []
        for line in names_input.strip().split("\n"):
            line = line.strip()
            if line:
                items.append({"name": line, "context": None, "deck_text": None})

    elif mode == "Upload image (Inc42 / LinkedIn / slide)":
        if not image_input:
            return []
        # Extract names from image first
        with st.spinner("Reading image for startup names..."):
            img_bytes = image_input.getvalue()
            extraction = extract_names_from_image(img_bytes, api_key)
            names = extraction.get("names", [])

        if not names:
            st.warning("Couldn't extract any startup names from the image.")
            return []

        # Show extracted names with confidence; ask user to confirm
        st.write("**Extracted names — please confirm before scouting:**")
        confirmed = []
        for n in names:
            label = f"{n['name']} ({n['confidence']})"
            if n.get("note"):
                label += f" — {n['note']}"
            default = n["confidence"] in ("high", "medium")
            if st.checkbox(label, value=default, key=f"img_{n['name']}"):
                confirmed.append({"name": n["name"], "context": None, "deck_text": None})
        items = confirmed

    elif mode == "Upload deck (PDF)":
        if not deck_input:
            return []
        # Extract text from PDF
        with st.spinner("Extracting deck text..."):
            try:
                from pypdf import PdfReader
                reader = PdfReader(io.BytesIO(deck_input.getvalue()))
                deck_text = "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                st.error(f"Could not read PDF: {e}")
                return []

        if not deck_text.strip():
            st.warning("Deck appears to be empty or image-only — text extraction failed.")
            return []

        items.append({
            "name": "(deck-based scout)",
            "context": None,
            "deck_text": deck_text,
        })

    elif mode == "Upload list (Excel/CSV)":
        if not excel_input:
            return []
        try:
            import pandas as pd
            if excel_input.name.endswith(".csv"):
                df = pd.read_csv(excel_input)
            else:
                df = pd.read_excel(excel_input)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            return []

        # Find name column (heuristic: column with 'name' or 'startup' or 'company' in header)
        name_col = None
        for col in df.columns:
            if any(k in str(col).lower() for k in ["name", "startup", "company"]):
                name_col = col
                break
        if name_col is None:
            name_col = df.columns[0]

        for _, row in df.iterrows():
            v = row[name_col]
            if pd.notna(v) and str(v).strip():
                items.append({"name": str(v).strip(), "context": None, "deck_text": None})

    return items


# ---------- Step 3: Run button ----------

st.write("")
run_clicked = st.button("🔍 Run scouting", type="primary", use_container_width=True)


# ---------- Execution ----------

if run_clicked:
    items = resolve_startup_list()

    if not items:
        st.warning("Nothing to scout. Add startup names or upload a file in Step 1.")
        st.stop()

    # Prepare working tracker
    if tracker_file:
        # User uploaded their live tracker
        working_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        with open(working_path, "wb") as f:
            f.write(tracker_file.getvalue())
    else:
        # Use blank template
        working_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        shutil.copy(TEMPLATE_PATH, working_path)

    # Progress UI
    progress_box = st.empty()
    summary_box = st.empty()

    counts = {"P1": 0, "P2": 0, "P3": 0, "Deprioritise": 0, "InsufficientData": 0, "Skipped": 0}
    scouted_rows = []  # list of (scouter_row, analyzed_row) ready for batch write
    log_lines = []

    for idx, item in enumerate(items):
        log_lines.append(f"⏳ {item['name']} — searching...")
        progress_box.markdown("\n".join(f"- {l}" for l in log_lines[-10:]))

        try:
            if item.get("deck_text"):
                result = scout_from_deck_text(item["deck_text"], api_key)
            else:
                result = scout_startup(item["name"], api_key, extra_context=item.get("context"))
        except Exception as e:
            log_lines[-1] = f"❌ {item['name']} — error: {str(e)[:80]}"
            counts["Skipped"] += 1
            progress_box.markdown("\n".join(f"- {l}" for l in log_lines[-10:]))
            continue

        if result.get("insufficient_data"):
            log_lines[-1] = f"🔍 {item['name']} — insufficient data, skipped"
            counts["InsufficientData"] += 1
            progress_box.markdown("\n".join(f"- {l}" for l in log_lines[-10:]))
            continue

        if result.get("ambiguous"):
            candidates = result.get("ambiguous_candidates", [])
            log_lines[-1] = f"⚠️ {item['name']} — ambiguous: {', '.join(candidates[:3])}"
            counts["Skipped"] += 1
            progress_box.markdown("\n".join(f"- {l}" for l in log_lines[-10:]))
            continue

        scouter_row = result.get("scouter_row")
        analyzed_row = result.get("analyzed_row")
        if not scouter_row or not analyzed_row:
            log_lines[-1] = f"❌ {item['name']} — incomplete response"
            counts["Skipped"] += 1
            progress_box.markdown("\n".join(f"- {l}" for l in log_lines[-10:]))
            continue

        # Tier counter
        tier = analyzed_row.get("tier", "")
        if tier.startswith("P1"):
            counts["P1"] += 1
        elif tier.startswith("P2"):
            counts["P2"] += 1
        elif tier.startswith("P3"):
            counts["P3"] += 1
        else:
            counts["Deprioritise"] += 1

        scouted_rows.append((scouter_row, analyzed_row))
        log_lines[-1] = f"✅ {scouter_row.get('name', item['name'])} — {tier}"
        progress_box.markdown("\n".join(f"- {l}" for l in log_lines[-10:]))

        # Update summary counts after each row
        with summary_box.container():
            cols = st.columns(5)
            cols[0].metric("Scouted", f"{idx+1}/{len(items)}")
            cols[1].metric("P1", counts["P1"])
            cols[2].metric("P2", counts["P2"])
            cols[3].metric("P3", counts["P3"])
            cols[4].metric("Skip/?", counts["Deprioritise"] + counts["InsufficientData"] + counts["Skipped"])

    # Write all rows in one batch
    if scouted_rows:
        scouter_dicts = [r[0] for r in scouted_rows]
        analyzed_dicts = [r[1] for r in scouted_rows]

        try:
            append_to_scouter(working_path, scouter_dicts)
            append_to_analyzed(working_path, analyzed_dicts)
        except Exception as e:
            st.error(f"Failed to write workbook: {e}")
            st.stop()

        # Provide download
        with open(working_path, "rb") as f:
            data = f.read()

        st.success(
            f"Done. Added **{len(scouted_rows)}** entries to both sheets. "
            f"Distribution: {counts['P1']} P1 · {counts['P2']} P2 · "
            f"{counts['P3']} P3 · {counts['Deprioritise']} Deprioritise"
        )

        st.download_button(
            "⬇️ Download Ventures_Tracker.xlsx",
            data=data,
            file_name="Ventures_Tracker.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary",
        )
    else:
        st.warning("No scouted rows to write.")
