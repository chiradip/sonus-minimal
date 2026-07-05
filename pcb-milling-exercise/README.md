# PCB Milling Exercise — JIG-1 (V_GS Matching Jig Board)

**The warm-up board for the Makera Carvera.** This is LABBOOK Fig. 4 — the MOSFET
matching jig — rebuilt as a single-sided milled PCB. It is deliberately the simplest
possible real board (3 nets, 11 holes, one resistor) while rehearsing *every* operation
the PSU board (Fig. 10) and channel boards (Fig. 9) will need:

| Skill practiced | Where it's used later |
|---|---|
| Isolation milling, ~0.5 mm gaps, sea + islands | Fig. 9/10 net islands |
| Two drill sizes + wire pads + TP loops | every board |
| Board cutout with tabs | every board |
| Mirroring convention (copper-up, pre-mirrored G-code) | every board |
| Buzz-out then live acceptance test | Phase B/C gates |

And it isn't a throwaway: the finished board runs **Phase A** — all 20 IRFP150N
measurements go through it.

## The circuit (see LABBOOK Fig. 4 for the schematic)

```
12 V supply (+) ──[VIN+ pad]──► R_j 6.8 Ω 10 W ──► DG island ──► DUT drain
                                                       │  (drain–gate tied in copper
                                                       │   = "diode-connected")
                                                       └──► DUT gate
DUT source ──► [SRC pad] ──► GND sea ──► [VIN− pad] ──► supply (−)
DMM: clips on TP V+ (DG) and TP V− (sea) → reading = V_GS at ≈1.2 A
```

Improvement over the clip-lead jig: the gate–drain jumper is **copper**, so one flying
lead and one intermittent-clip failure mode disappear. The DUT stays off-board on a
scrap heatsink — it dissipates ~4.5 W and R_j itself runs at ~10.6 W (at its rating:
readings are 60–90 s bursts, then power off).

## Board artwork

![JIG-1 copper plan, component side](jig-copper-plan.svg)

![JIG-1 as-machined view with toolpaths](jig-milling-view.svg)

## Files

| File | Tool | What it does |
|---|---|---|
| `make_gcode.py` | — | regenerates all G-code (`python3 make_gcode.py`) |
| `gcode/01-isolation-vbit.nc` | 30° V-bit, 0.1 mm tip | 2 concentric outlines per island, Z −0.20 |
| `gcode/02-drill-1p0mm.nc` | 1.0 mm drill | 4 × TP loop holes |
| `gcode/03-drill-1p2mm.nc` | 1.2 mm drill | 2 × R_j lead holes |
| `gcode/04-drill-1p6mm.nc` | 1.6 mm drill | 5 × wire pads (VIN±, SRC, DRAIN, GATE) |
| `gcode/05-drill-3p2mm.nc` | 3.2 mm drill | 4 × M3 mounting holes |
| `gcode/06-cutout-2mm.nc` | 2 mm endmill | outline, 4 passes, 4 tabs (4 mm × ~0.6 mm) |

G-code facts: metric, absolute (G21/G90), plain G0/G1 only (no canned cycles — safe for
the Carvera's Smoothieware-family controller), spindle M3/M5, ends M30.
**All coordinates are pre-mirrored for copper-side-up machining. Never mirror again.**
One WCS for all six files: X0 Y0 at the blank's bottom-left, Z0 on the copper.

## Bill of materials (everything is already in your orders)

| Item | Source status |
|---|---|
| R_j — Ohmite TWW10J6R8E, 6.8 Ω 10 W | DigiKey delta order (×3) |
| FR4 blank, single-sided, 1.6 mm, ≥80 × 50 mm | delta-4 consumables |
| Bus wire (TP loops), hookup wire + alligator clips (DUT + supply leads) | delta-4 / bench |
| 12 V ≥1.5 A supply, DMM | bench |

⚠ **One measurement to confirm on the physical part** (the only assumption I couldn't
verify from stock on hand): R_j pad pitch is **54 mm**, sized for the datasheet body of
44.5 × 8 mm. When the TWW10J6R8E arrives, measure the body — if it's over 47 mm, edit
`PADS[1.2]` in `make_gcode.py` and regenerate before drilling.

## Carvera run sequence

1. **Stock down**: tape (or tape+CA) the blank to the spoilboard, copper **up**. Press
   flat — V-bit depth errors equal flatness errors.
2. **Zero**: X/Y at the blank's bottom-left corner; Z on the copper surface (probe or
   paper). Same WCS for every file.
3. **Test cut** (mandatory first time): run the first few lines of `01-isolation` over a
   sacrificial corner, measure the groove — target ≈0.2 mm wide, clean copper edges.
   Groove too wide → raise Z by 0.05; doesn't break through → lower by 0.05.
4. Run files **01 → 06** in order, changing tools between files (speeds/feeds are in
   each file header: 12 k/9 k/10 k rpm; 300/60/250 mm/min).
5. **Free the board**: cut the 4 tabs with flush cutters, file smooth. Vacuum all FR4
   dust — wear a mask; fiberglass fines are nasty.

## Acceptance (do all three before calling it done)

1. **Buzz-out (unstuffed)**: VIN+↔DG open · VIN+↔sea open · DG↔sea open.
2. **Stuff & buzz again**: solder R_j (3–5 mm proud) + TP loops + supply/DUT leads.
   Now VIN+↔DG must read ≈6.8 Ω, everything↔sea still open.
3. **Live test = LABBOOK Phase A, step A-2/A-3**: clip a DUT on its heatsink, 12 V on,
   60 s settle, read V_GS on the TP loops — expect 3.1–4.1 V at ≈1.2 A. First device
   measured = board commissioned = milling workflow proven for Fig. 10.

*JIG-1 rev A · 2026-07-05 · part of the Sonus Minimal build package.*
