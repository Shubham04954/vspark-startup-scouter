# Colour Rules — exact hex codes & openpyxl pattern

Apply colour fills explicitly per cell based on the **first emoji** in
the cell's text content. Never inherit from previous row.

## Hex codes

| Emoji | Verdict / Fit type | Hex | RGB |
|---|---|---|---|
| ✅ | Strong / Yes / Pass | `FF92D050` | green |
| ⚠️ | Possible / Exploratory | `FFFFFF00` | amber/yellow |
| ❌ | No Fit / Not Recommended | `FFFF0000` | red |
| 🚩 | Not a Startup / Severe flag | `FFFF0000` | red |
| 🔍 | Insufficient Data / To Evaluate | `FFFF0000` | red |

## Where to apply

In `New_Startup_Scouter` sheet (Variant B):

- **M-S** (the 7 BU columns): emoji-based fill per cell
- **T** (Verdict): emoji-based fill — first emoji in the verdict text

In `Analyzed Startups` sheet: no fill colour applied — keep header/data
row default formatting from template.

## Python pattern (openpyxl)

```python
from openpyxl.styles import PatternFill

GREEN = PatternFill(start_color='FF92D050', end_color='FF92D050', fill_type='solid')
AMBER = PatternFill(start_color='FFFFFF00', end_color='FFFFFF00', fill_type='solid')
RED   = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')

def apply_fill_for_cell(cell):
    """Apply colour based on first emoji in cell value."""
    v = str(cell.value or '')[:3]   # first emoji + space
    if v.startswith('✅'):
        cell.fill = GREEN
    elif v.startswith('⚠️'):
        cell.fill = AMBER
    elif v.startswith('❌') or v.startswith('🚩') or v.startswith('🔍'):
        cell.fill = RED
    # else: leave default

# Apply to BU + verdict columns (Variant B = cols 13-20)
for col in range(13, 21):
    apply_fill_for_cell(ws.cell(row=r, column=col))
```

## Common bug to avoid

When you do `ws.insert_rows(N)` followed by copying formatting from a
previous row (`copy(src.fill)`), the **fill colour is inherited from
the source row**. If the source row was all-red ❌ and the new row has
⚠️ Possible cells, the new ⚠️ cells end up red.

**Always** apply the emoji-based fill explicitly **after** copying row
formatting, never rely on inherited fill.

## Variant detection

Variant A (older Ventures_Tracker): BU columns L-R (12-18), Verdict S (19)
Variant B (newer): BU columns M-S (13-19), Verdict T (20)

Detect by reading row 4 headers — find which column contains "BALCO"
text, that's the start of BU columns. HZL is 4 columns to the right of
BALCO. Verdict is the column immediately after IOB.
