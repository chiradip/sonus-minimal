# Part Tracking — procurement log

Running log of where parts actually came from, when the source differs from the BOM's
assumption (DigiKey), and anything that affects build quality. Add a row whenever an order
is placed or received; reference it from the unit logs in LABBOOK Appendix A.

| Date | Part / Ref | Qty | Source (actual) | Why not DigiKey | Status | Notes |
|---|---|---|---|---|---|---|
| 2026-07-04 | **IRFP150NPBF** (Q1, Q2) | 20 | **Amazon** | Out of stock on DigiKey at order time | ordered | ⚠ see authenticity note below |
| 2026-07-04 | **TOOL R_dummy** (BOM: Arcol HS50 8R J) | **8** (4 × 2-pc packs) | **Amazon** — "Chanzon 2pcs Wirewound Aluminum Shell Resistor 8 Ω 50W ±5% 8R" | Substitute brand, convenience | ordered | Acceptable; 8 pcs enables a 2×2 array per channel — see dummy-load note below |

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

## Order status snapshot

| Order | Source | Placed | Received | Checked in (Phase A-1) |
|---|---|---|---|---|
| Main BOM rev 4 | DigiKey | | | |
| IRFP150N ×20 | Amazon | 2026-07-04 | | |
| T1 toroids ×3 | DigiKey/Mouser (Hammond) or Antek direct | | | |
| HS1 heatsinks ×6 | HeatsinkUSA (direct) | | | |
