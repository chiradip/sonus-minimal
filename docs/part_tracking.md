# Part Tracking — procurement log

> **Scope (2026-07-04): building 2 units (SM-001, SM-002).** Quantities across all orders
> were deliberately sized for 3 amps as an attrition buffer for perfboard/breadboard
> experimentation. Third-unit-only hardware (toroid #3, heatsink pair #3, IEC #3, bridge #3)
> is shelf stock, not waste — a third build remains possible without re-planning.

Running log of where parts actually came from, when the source differs from the BOM's
assumption (DigiKey), and anything that affects build quality. Add a row whenever an order
is placed or received; reference it from the unit logs in LABBOOK Appendix A.

| Date | Part / Ref | Qty | Source (actual) | Why not DigiKey | Status | Notes |
|---|---|---|---|---|---|---|
| 2026-06-26 | **MAIN BASE ORDER** (rev-3 BOM, 26 lines) | — | **DigiKey** invoice 128236717, $876.94, shipped complete | — | received | Substitutions: **IRFP150PBF (Vishay) ×12 — the original IRFP150, NOT the 150N** (see FET note); PNP300JR-73-0R47 for R_s (fine); TDK B32529D0225J189 for C_in (fine). Superseded rev-3 parts arrived (10k×50, ECA-1VM222×10, ECA-1VM101×50) → quarantine bag. **Gaps found in audit — see GAPS section.** |
| 2026-07-04 | **IRFP150NPBF** (Q1, Q2) | 20 | **Amazon** | Out of stock on DigiKey at order time | ordered | ⚠ see authenticity note below |
| 2026-07-04 | **TOOL R_dummy** (BOM: Arcol HS50 8R J) | **8** (4 × 2-pc packs) | **Amazon** — "Chanzon 2pcs Wirewound Aluminum Shell Resistor 8 Ω 50W ±5% 8R" | Substitute brand, convenience | ordered | Acceptable; 8 pcs enables a 2×2 array per channel — see dummy-load note below |
| 2026-07-04 | **DigiKey delta order** (delta-1 + delta-2, 14 lines) | see note | **DigiKey** cart 2026-07-04T213235 | — | cart exported / ordered | BD13916STU×10, 2K2×100, 1N5408×10 (Diotec), CL-60×10, 10R×10, C_z 0.1µF×10, 33K×10, 4880MG×5, TWW10J6R8E×3, 120-2×2, **82K×100, 22K×100, UPW1H222MHD×10, UPW1H101MPD×20**. ≈$115. All in stock, no backorder. Closes delta-2; 4880MG + both UPW MPNs now verified real/stocked (ECR-6/7 flags resolved). |
| 2026-07-04 | **Rb_bot select 18 k** (BOM: MFR-25FBF52-18K) | 100 (6 max used) | **Amazon** — "Chanzon 100pcs 1/4W 18K Ω Metal Film Fixed Resistor ±1% MF Through Hole" | Substitute brand, bulk pack | ordered | Spec-equivalent (18 k ¼ W 1 % MF). DMM-verify a sample on arrival (17.82–18.18 k). Conditional stock: stuffed only for FET pairs with V_GS < 3.15 V (Table 4.3). Bag + label the ~94 spares — do NOT let loose resistors near the build. |

## ⚠ Note on the Amazon-sourced IRFP150N

Amazon marketplace is a known channel for **counterfeit / remarked power MOSFETs**, and the
IRFP150N is a frequently faked part. This is manageable here because the build already
includes the screening step:

1. **Phase A (Fig. 4 jig) doubles as an authenticity screen.** Genuine IRFP150N at ≈1.2 A
   should read V_GS ≈ 3.1–4.1 V, and 20 parts from one lot should cluster within a few
   hundred mV. Red flags: readings far outside that window, a scatter spanning >1 V,
   devices that won't hold a stable reading after the 60 s settle, or cases that heat much
   faster than ~4.5 W warrants (undersized die).
2. **Check the physicals on arrival:** consistent laser marking (not ink), matching lot
   codes, clean un-tinned leads, magnet test on the tab (should be non-magnetic copper,
   not steel).
3. **If the lot fails screening**, return it and re-order — IRFP250NPBF / IXYS IRFP250
   (BOM alternates) from an authorized distributor (DigiKey, Mouser, Arrow) are drop-in;
   Table 4.3 bias selection absorbs their slightly different V_GS.
4. Record the per-device V_GS values in LABBOOK Table A.2 as usual — that table is the
   permanent record of this lot's quality.

## Note on the Chanzon 8 Ω 50 W dummy loads

Fine substitution — this is a bench tool, not an in-circuit part, and any aluminum-shell
wirewound of the same rating does the job (it stands in for the Arcol HS50 8R J).
**Eight pieces were ordered (4 × 2-pc packs), which is better than the BOM's two:**

1. **Build two 2×2 arrays** (two in series, two such strings in parallel): still 8 Ω, but
   rated 200 W per array with the heat spread over four housings. One array per channel —
   this comfortably covers every test in the book, including the Phase B PSU load test
   (~62 W: a single 50 W resistor would have needed derating gymnastics).
2. **The 50 W/pc rating still assumes a heatsink.** Bolt each array to a scrap heatsink or
   aluminum plate with thermal compound; free-air these housings are good for ~20 W each.
3. **Verify on arrival:** DMM each piece — expect 7.6–8.4 Ω (±5 %).
   Record: R1 ____ R2 ____ R3 ____ R4 ____ R5 ____ R6 ____ R7 ____ R8 ____ Ω.
   Wirewound = inductive; irrelevant for DC bias and 1 kHz THD work, just don't interpret
   >20 kHz square-wave results into it.

Rule of thumb going forward: **actives and anything safety-critical (MOSFETs, BJTs, bridge,
fuse, IEC inlet, mains parts) prefer authorized distributors**; passives from Amazon are a
smaller risk but still worth the same arrival check.


## 🚩 GAPS found auditing invoice 128236717 (2026-07-04) — order before Phase D

1. **TO-247 insulators: NONE on hand — BUILD BLOCKER.** The invoice description proves
   4880SG is a **TO-220** Thermasil pad (rev-3 mislabeled it TO-247; its "verify kit
   contents" flag is hereby cashed in). 4880MG (delta order) is also TO-220. Q1/Q2 are
   TO-247: **need 12 TO-247/TO-3P insulator pads.** RESOLVED MPN (verified on DigiKey
   2026-07-04): **Bergquist SP400-0.007-00-104** — listed TO-218/220/247, 25.4x19.05 mm,
   in stock (7,002), \$0.25. Alternates: Fischer WK 247, Wakefield WTI7R1F0-1.00X0.75.
   Bushings only if the FET's mounting hole shows metal (IRFP150N holes are plastic-lined).
   Both 4880 numbers confirmed TO-220 on their product pages. Upside: Q_cm's TO-220
   insulators are now 15-deep.
2. ~~Keystone 7019 binding posts: 4 of 6.~~ **RESOLVED by scope change (2 units):**
   4 posts = exactly 2 amps. No reorder.
3. ~~Hammond 1182G18 toroids: 2 of 3 on this invoice.~~ **RESOLVED 2026-07-04:** the
   third toroid was ordered separately (see snapshot table).

Order file for gap 1: **`BOM-rev4-delta-3-gaps.csv`** (12× TO-247 pads + bushings).
Verify the TO-247 package filter at cart — do not trust 4880-series numbering.

## Note on the two FET types now in stock

- 12 × **IRFP150PBF** (Vishay, genuine via DigiKey) — original IRFP150.
- 20 × **IRFP150NPBF** (Amazon) — the BOM part, authenticity to be screened in Phase A.

Either type works (bias select absorbs the V_GS difference; both 100 V / 40 A class).
Rules: **never mix types within a channel pair**; prefer one type across both amps
for consistent channel character. Plan: screen the Amazon N-lot first — if clean, build
with it and keep the Vishay dozen as certified backup; if dirty, the Vishay 12 covers all
six pairs with zero sorting headroom (pair adjacent values and accept up to 40 mV).

## Order status snapshot

| Order | Source | Placed | Received | Checked in (Phase A-1) |
|---|---|---|---|---|
| Main base order (rev-3, inv. 128236717) | DigiKey | 2026-06-26 | 2026-06-xx ✓ | |
| Delta-1 + delta-2 (14 lines) | DigiKey | 2026-07-04 | | |
| Delta-3 gap (12× TO-247 insulator kits) | DigiKey | | | |
| IRFP150N ×20 | Amazon | 2026-07-04 | | |
| 18 k ×100 (select kit) | Amazon | 2026-07-04 | | |
| Dummy loads 8 Ω ×8 | Amazon | 2026-07-04 | | |
| T1 toroid ×1 (third; 2 came in base order) | separate order | 2026-07-04 | | |
| HS1 heatsinks ×6 | HeatsinkUSA (direct) | 2026-07-04 | | |
