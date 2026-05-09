# Credibility Flags — Mandatory Audit Checklist

Every startup goes through this audit. Findings surface directly in:
- Funding cell (column I) — for funding/recognition flags, prefixed with 🚩
- Founders cell (column J) — for identity flags
- Capabilities cell (column L) — for product/pivot flags
- Verdict cell (column T) — for material flags affecting rating

**Do NOT soften flags.** If verifiable claim is missing, write "Not surfaced
in search" or "Self-claimed only — not independently verified."

---

## 1. Founder identity verification

- [ ] Founder name(s) on company website match LinkedIn profiles?
- [ ] Founders listed as MCA directors? (cross-check CIN's director list)
- [ ] Co-founder discrepancies between Tracxn/Internshala and MCA?
  - **Precedent**: YellowSense — Shilpi Gupta tagged Co-Founder on
    Tracxn/Internshala/her LinkedIn but NOT on MCA director list
- [ ] Founder bios reasonable for product complexity?
  - **Precedent**: SnapBooks — LinkedIn says "Quant Risk Analyst, Final
    Year" but deck says "Quantitative Associate" (title inflation)
- [ ] Solo founder for an enterprise B2B product? (flag — not necessarily
  fatal but worth noting)

## 2. Funding claims

- [ ] Funding figures verifiable on Tracxn or news?
- [ ] Self-claimed valuations (e.g., "$11.71M") with no third-party round?
  - **Precedent**: Finigenie — self-reported valuation, Tracxn unfunded
- [ ] Govt grant claims (DPIIT, MeitY, KTech, RBIH) verifiable?
  - **Precedent**: SophyXis — "RBIH incubation" claim, no RBIH-side
    confirmation; flag as "self-claimed only"
- [ ] Accelerator backing real? (YC public, NVIDIA Inception public,
  state TBI verifiable)
- [ ] MCA paid-up capital reasonable for claimed scale?
  - **Precedent**: TanPrish ₹10K paid-up vs claimed pan-India ambition
    = early-stage signal (not negative, just sizing)

## 3. Customer / partner claims

- [ ] Customer logos identifiable / readable?
  - **Precedent**: YellowSense — partner logos duplicated
    (img-1 through img-6 repeated 4 times), unreadable
- [ ] Number of claimed customers arithmetically plausible vs revenue?
  - **Precedent**: YellowSense — ₹3.56L FY25 revenue vs "50+ enterprise
    clients" = arithmetically implausible
- [ ] Named customers verifiable on customer's own websites or press?
- [ ] "Trusted by industry leaders" with no named entities = flag

## 4. Team-vs-product surface area

- [ ] Team size proportionate to claimed product portfolio?
  - **Precedent**: YellowSense — ~8 engineers delivering 14 product SKUs
    incl naval defense = implausible
  - **Precedent**: SophyXis — 2-person founding team, 4 unrelated
    verticals (finance, agri, legal, contracts) = execution risk
- [ ] CTO or technical lead named? (esp. for AI/deeptech claims)
- [ ] Research claims backed by named researcher with publication history?

## 5. Date / temporal consistency

- [ ] CIN incorporation year vs site "Founded" year vs blog post dates
  consistent?
  - **Precedent**: SophyXis — site says founded 2024, CIN is 2026, blog
    posts dated Nov 2025 / Jul 2025 predate Pvt Ltd registration
- [ ] Recent activity on website / LinkedIn? (dormant signals)
- [ ] Site copyright year recent?
  - **Precedent**: Datamatrix.AI — site copyright 2021, MCA recent
    (signal: services brand-rebadged)

## 6. Contact / registry hygiene

- [ ] Registered email = company domain (`@startupname.com`) or
  generic gmail / registry-agent gmail?
  - **Precedent**: YellowSense — `rateindiaconsultants@gmail.com`
    (registry agent, not company)
  - **Precedent**: Diagno+ — `@gmail.com` for "India's Largest" claim
- [ ] Registered office at residential address? (early-stage signal,
  not necessarily negative — note for context)
- [ ] DNS / website resolvable and live?
  - **Precedent**: Impech Solutions — website DNS fails

## 7. Pivot signals

- [ ] Current website pitch matches Tracxn / Internshala / press history?
- [ ] If pivoted: does the pivot story make sense?
  - **Precedent (severe)**: YellowSense pivoted from GenAI
    maid/cook/nanny marketplace to "deep-tech 14-product portfolio
    incl naval defense" — pivot incoherent
- [ ] If multiple positionings present: separate pages, or just
  legacy pages still live? (zipp.ai legacy CMMS/EAM/SCADA page still
  live alongside pharma GxP pivot — engine industry-agnostic)

## 8. Brand ambiguity

- [ ] Multiple companies share the brand name?
  - **Precedent**: Datamatrix.AI — 3+ unrelated MCA entities
- [ ] If yes: which is the one being scouted? Verify before writing.

## 8b. URL verification — write only links you actually saw, ONE link per cell

- [ ] Every URL in the Website column (E) was SEEN in a search result during this run
- [ ] Website URL is the **root** (e.g. `https://xterrarobotics.com`), not a subpath like `/svan-m2/` you didn't actually visit
- [ ] Website URL includes `https://` prefix and is set as a hyperlink (clickable)
- [ ] LinkedIn column (F) has **exactly ONE URL** — Excel needs single URL for the cell to be clickable
- [ ] LinkedIn priority: (1) company page if surfaced → (2) founder page if no company → (3) blank
- [ ] LinkedIn URL was SEEN in search, not guessed from the company name
  - Bubble Me → `bubbleme-india` (not `bubbleme`)
  - xTerra Robotics → no company page surfaced, fall back to founder URL
- [ ] If neither company nor founder URL surfaced, leave LinkedIn cell **blank** — never write `Search: <query>`, `Not surfaced in search`, or multiple URLs

## 9. Self-claims requiring caveat
- [ ] "World-class research team publishing at top AI conferences" —
  but no named researcher, no venue attribution → flag
- [ ] "Patents granted" — verify on Indian Patent Office portal
- [ ] "Published research" — verify venue (peer-reviewed? Workshop?
  Self-published?)
- [ ] "AI-powered" or "agentic AI" — is the AI core to the product
  or marketing veneer over rule-based logic?

---

## How flags appear in output cells

**Funding cell (I)**:
```
🚩 Unfunded / bootstrapped — MCA ₹1L authorized & paid-up; no VC/angel on
Tracxn despite 2.5 yrs. DIPP-138388 + Udyam UDYAM-KR-03-0293956. Revenue
FY25 ₹3.56L (effectively pre-revenue). Registry contact email
"rateindiaconsultants@gmail.com" — registry-agent address.
```

**Founders cell (J)**:
```
Prakhar Goyal (CEO, IIT Bombay, 15+ yrs); Komal Goyal (COO). MCA directors:
Prakhar + Komal (husband-wife). Shilpi Gupta tagged "Co-Founder" on Tracxn /
Internshala / LinkedIn but NOT MCA director (flag). ~8 people, mostly
backend + 1 intern. No CTO, no AI research head.
```

**Capabilities cell (L)**:
```
🚩 MAJOR PIVOT. (A) ORIGINAL: 2023 GenAI maid/cook/nanny marketplace; Tracxn
competitors DriveU, Snabbit, ChefKart. (B) CURRENT SITE: "deep-tech" with 14
products — Industrial Fault, Fraud, Clean Rooms, TTS, Encryption, eTappal,
Compliance, Face Liveness, Naval Defense, Nutrition AI, TASCO.
```

**Verdict cell (T)**:
```
❌ Not Recommended | Cross-BU — | CSR/ESG —
SEVERE CREDIBILITY FLAGS. 🚩 Pivot from maid-marketplace to 14-product
deep-tech portfolio. ₹3.56L FY25 vs "50+ enterprise clients" implausible.
Unfunded 2.5+ yrs. ~8-person team can't deliver 14 products incl naval
defense. PARK.
```
