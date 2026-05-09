# Cross-BU Routing Rules

When does a startup get a `Cross-BU ✓` badge in the verdict, and to which
Group function does it route?

A capability gets the **Cross-BU ✓** badge if it satisfies BOTH:
1. Applies to ≥3 of the 7 Vedanta BUs at a recognisable use-case level
2. Would be more efficiently procured at Group / Centre level than as
   per-BU CCDs (because the spec is similar across BUs, or vendor mgmt
   benefits from consolidation, or risk needs central oversight)

The badge format in verdict cell is:
`Cross-BU ✓ ([Group function name])`

Use **generic Group function names** only — never named individuals.

---

## Capability → Group Function mapping

| If capability is… | Cross-BU function = |
|---|---|
| Product/material traceability, anti-counterfeit, supply-chain integrity (LBMA, ingot authentication, lot tracking) | **Group Procurement** |
| Vendor management, contract AI, CLM, EPC contract review, procurement template standardisation | **Group Procurement** |
| Cybersecurity, post-quantum crypto, data protection, IT GRC, vendor security | **Group CISO** |
| Drone inspection (generic across stockyard, stack, pipeline, perimeter) | **Group CTO / Digital** |
| TSF / tailings / ash pond / red mud / overburden monitoring | **Group Sustainability** |
| Decarbonisation tech (RE storage, green H2, carbon capture, biomass, energy efficiency) | **Group Sustainability** |
| Water management, ZLD, recycling, biodiversity | **Group Sustainability** |
| Air quality, emissions monitoring, dust suppression | **Group Sustainability** |
| ERP/SAP/MES integration, plant data lakes, Industry 4.0 horizontal | **Group CTO / Digital** |
| GxP / ISO 9001/14001/45001 / statutory compliance automation | **Group Quality / Compliance** |
| Embedded software / sensor firmware / edge AI dev tools | **Group CTO / Digital** |
| Plant-worker safety: PPE, fatigue, gas detection (cross-BU HSE) | **Group Sustainability** (HSE under SD) |
| Workforce skilling, vocational, technician training | **Group HR / L&D** |

---

## What does NOT get Cross-BU

- **Single-BU specialisation**: e.g. RLE roaster optimisation = HZL only, not Cross-BU
- **Site-specific physical asset**: e.g. Mangala MPT = Cairn only
- **Generic "could fit any industrial company"**: must show concrete BU-specific use cases for ≥3 BUs

If you find yourself tagging Cross-BU just because the capability is "broad", challenge yourself: what is the actual use case at HZL Rampura Agucha vs ESL Bokaro vs Cairn Barmer? If you can't name three concrete use cases, it's not Cross-BU — it's just non-industrial.

---

## Examples

**OneARVO (anti-counterfeit traceability)** — `Cross-BU ✓ (Group Procurement)`
- HZL Pantnagar silver LBMA chain-of-custody
- HZL zinc ingot LBMA
- ESL steel ingot dispatch authentication
- BALCO/VAL-J aluminium ingot authentication
→ 4 named BU use cases, similar spec → Group Procurement should drive

**Synergy Quantum (post-quantum crypto)** — `Cross-BU ✓ (Group CISO)`
- All BUs need it eventually
- Spec is identical across BUs
- Risk needs central oversight (board-level theme)
→ Group CISO should drive

**ClimMaTech (flood/TSF monitoring)** — `Cross-BU ✓ (Group Sustainability)`
- HZL TSFs (4 sites, GISTM)
- IOB pit-water monsoon (Karnataka, Liberia)
- BALCO/VAL ash & red mud ponds
- ESL slag dumps
→ 4+ BUs, GISTM is board-level → Group Sustainability

**CraftifAI (embedded AI dev tools)** — `Cross-BU ✓ (Group CTO / Digital)`
- All BUs have IIoT/sensor firmware projects
- Horizontal dev tool, not industrial use case
→ Group CTO / Digital

**Xterra Robotics (quadruped inspection)** — `Cross-BU —`
- Strong fit at HZL underground + IOB pit
- But VAL/BALCO/ESL is "possible" not "strong"
- Better to engage as 2-BU pilot than Group-procured platform
→ Single-route ✅ rather than Cross-BU
