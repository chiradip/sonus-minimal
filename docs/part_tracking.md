# Part Tracking — procurement log

Running log of where parts actually came from, when the source differs from the BOM's
assumption (DigiKey), and anything that affects build quality. Add a row whenever an order
is placed or received; reference it from the unit logs in LABBOOK Appendix A.

| Date | Part / Ref | Qty | Source (actual) | Why not DigiKey | Status | Notes |
|---|---|---|---|---|---|---|
| 2026-07-04 | **IRFP150NPBF** (Q1, Q2) | 20 | **Amazon** | Out of stock on DigiKey at order time | ordered | ⚠ see authenticity note below |

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
