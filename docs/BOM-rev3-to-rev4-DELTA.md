# BOM rev 3 → rev 4 Delta — What to Order, What Not to Stuff, and Why

**Audience:** anyone who already ordered (or is holding stock from) the rev 3 BOM
(`docs/original/SE-ClassA-5W-BOM-3amps-digikey-rev3.csv`).
**Companion files:**

| File | Import it when |
|---|---|
| `BOM-rev4-delta-1-additions.csv` | Always — parts rev 3 did not contain at all |
| `BOM-rev4-delta-2-replacements.csv` | Always — parts that supersede rev 3 items you may already own |
| `BOM-rev4.csv` | Instead of both, if you have ordered **nothing** yet |

Both delta files use the same columns as rev 3/rev 4, so DigiKey's list importer takes them
directly (map *Manufacturer Part Number* and *Quantity*; `Customer Reference` keeps the
schematic refdes). Full engineering derivations live in `LABBOOK.md` §3 (ECR-1…8); this doc
is the ordering-desk summary.

---

## 1. Why the additions exist (delta file 1)

These aren't upgrades — each one covers a failure mode the rev 3 build would have hit.

| Part | Without it… |
|---|---|
| **BD139 (Q_d)** | The MJE15032 alone needs ~56 mA of base current at the 2.8 A load (β ≈ 50). That current through R_cm = 220 Ω drops **~12 V**, and the "+24 V" rail arrives at ~11 V. The amp hums, clips at a watt, and Q_cm cooks. The BD139 raises the composite β to ~5000, shrinking the drop to <0.2 V. *(ECR-1)* |
| **R_be 2.2 k** | The Darlington pair has no defined turn-off path; leakage keeps Q_cm partially on at power-down and the rail floats unpredictably. *(ECR-1)* |
| **D_p 1N5408** | At power-off the reservoir discharges faster than the rail-side capacitance; Q_cm's base-emitter junction gets reverse-biased beyond its rating and degrades silently — the amp gets noisier over months. The diode clamps it. *(ECR-1)* |
| **CL-60 (RT1)** | A 225 VA toroid charging 20 mF from a wall socket draws a multi-tens-of-amps surge. F1 (2 A slow) either nuisance-blows or gets upsized until it protects nothing. The NTC absorbs the surge and fades to ~0.2 Ω warm. *(ECR-1)* |
| **R_z + C_z (Zobel)** | The IRFP150N has higher gm and C_iss than the IRFP240 the design was narrated around. Into an inductive cable with no HF load, the follower can ring or oscillate at MHz — audible as "hard" treble, measurable as an H3-heavy spectrum, occasionally fatal to tweeters. 10 Ω + 100 nF keeps the amp loaded above the audio band. *(ECR-2)* |
| **18 k / 33 k bias-select kit** | IRFP150N threshold spread is 2–4 V. With only the default 22 k, pairs at the edges of the spread run out of trimmer: bias either can't reach 1.40 A or can't come down to it. The select table (LABBOOK Table 4.3) plus these two values covers the full spread — verified numerically. *(ECR-2)* |
| **TO-220 insulator kit (INS2)** | See §2.4 below — the rev 3 kit physically doesn't fit Q_cm. *(ECR-7)* |
| **8 × extra IRFP150N** | Rev 3 ordered exactly 12 = zero sorting headroom. Matching (ΔV_GS ≤ 25 mV within a pair) is what keeps the operating point and the H2 character consistent between channels; you cannot sort 12 parts into 6 adjacent pairs unless the distribution cooperates. 20 parts make Phase A deterministic. |
| **Jig/dummy/compound (TOOL lines)** | Phase A cannot measure V_GS without the 6.8 Ω jig resistor; Phases B/E/F must never see a speaker before a dummy load; mica without compound roughly doubles the case-to-sink thermal resistance. |

## 2. Why the superseded rev 3 parts must NOT be used (delta file 2)

If you hold these from a rev 3 order, move them to the spares bin — do not stuff them.

### 2.1 R_fb = 47 k (rev 3) → 82 k (rev 4)

The amplifier self-biases: OUT_NODE settles where the R_fb : R_in divider makes Q1's gate
voltage equal V_GS + 0.66 V. That arithmetic was done for the IRFP240 (V_GS ≈ 4.5 V at
1.4 A). The BOM, however, ships the **IRFP150N** (V_GS ≈ 3.4 V warm). With 47 k : 47 k the
output settles at 2 × (3.4 + 0.66) ≈ **8.1 V** instead of half-rail (~11 V):

- down-swing clips at ≈ −6.5 V pk → **≈ 2.7 W** into 8 Ω — the 5 W spec is missed by 3 dB;
- clipping is grossly asymmetric, so the "soft H2 clip" story collapses too.

82 k moves the divider ratio to 0.364 and puts OUT_NODE back at ≈ 11 V. A 47 k soldered in
the R_fb position **works electrically and passes every smoke test** — it just quietly builds
a 3 W amplifier. That's what makes it dangerous: nothing fails until Phase F measures power.
*(ECR-2; numeric verification in LABBOOK §3.)*

**Fate of the old parts:** rev 3 ordered 18 × 47 k; 12 are still used (R_in, Rb_top). The
6 spare 47 k are fine parts — keep them as spares, never as R_fb.

### 2.2 Rb_bot = 10 k (rev 3) → 22 k default + select kit (rev 4)

Q2's bias divider (returned to OUT_NODE) must place ≈ V_GS + 0.66 V ≈ 4.1 V across
gate-to-output. With Rb_bot = 10 k and the full 10 k trimmer, the divider reaches at most
(24 − 12) × 20k/67k ≈ 3.6 V — and against the *real* 22.3 V rail even less. Result: **the
trimmer hits its end stop before bias reaches 1.40 A**, for essentially every IRFP150N ever
made. The channel runs starved (0.5–0.9 A), distortion rises, and no amount of trimming
helps because the range itself is wrong. 22 k centres the trimmer at 1.40 A for typical
parts; 18 k/33 k cover the tails of the V_GS distribution. *(ECR-2)*

**Fate of the old parts:** all 6 × 10 k are unused in rev 4. Spares bin.

### 2.3 C_cm = ECA-1VM222, Cb_filt = ECA-1VM101 (rev 3) → Nichicon UPW, 50 V (rev 4)

Three independent reasons:

1. **Never verified.** The rev 3 handoff itself flags both lines "⚠ stock not re-verified" —
   they were placeholders, not selections.
2. **Voltage margin.** They are 35 V parts. C_cm sits on the multiplier base at ≈ 24 V
   steady — 69 % of rated voltage, and worse during a high-mains day or if the load is
   disconnected (raw rises toward 26+ V). Electrolytic lifetime is exponential in stress;
   every other electrolytic in this amp is 50 V for exactly this reason.
3. **Role.** C_cm is the τ-setting element of the ripple filter and Cb_filt is the bootstrap
   that turns Q2 into a current source — both are quality-sensitive positions where a low-Z,
   105 °C-rated series (UPW / EEU-FC) is the appropriate grade. *(ECR-6)*

**Fate of the old parts:** if you already own the Panasonic ECAs they will *function* at
nominal mains — but with thin margin in the two positions least worth economizing (total
upgrade cost ≈ $3). Rev 4 treats them as unsuitable; spares bin for low-voltage projects.

### 2.4 4880SG (qty 15, rev 3) → 12 used + TO-220 kit (rev 4)

The 4880SG is a **TO-247** mica + shoulder-washer kit. Q1/Q2 are TO-247 — 12 kits, correct.
But Q_cm (MJE15032) is a **TO-220**: smaller tab, different hole position. A TO-247 mica
under it leaves the mounting hole misaligned and the washer loose; the usual improvised fix
(drill it, snug it down anyway) cracks mica or leaves a gap — and Q_cm's tab is its
**collector at raw +24 V**. A marginal insulator there is an intermittent rail-to-heatsink
short. Use a proper TO-220 kit. *(ECR-7)*

**Fate of the old parts:** the 3 surplus 4880SG kits are your spare TO-247 insulators for
Phase D remounts — genuinely useful, just not on Q_cm.

## 3. Quantity changes that are neither additions nor replacements

| Line | rev 3 | rev 4 | Note |
|---|---|---|---|
| 47 k (MFR-25FBF52-47K) | 18 | 12 used | no reorder needed; surplus = spares |
| 0.1 µF R82 (R82EC3100DQ70K) | 6 | 12 | the +6 are in the additions file (C_z) |
| HS1 heatsink length | ~8″/ch | **10″/ch** | ECR-5 — if already cut at 8″, keep it only if the Phase F thermal soak passes (sink ≤ 50 °C after 1 h); otherwise re-order |

## 4. Checklist

- ☐ Import `BOM-rev4-delta-1-additions.csv` → order.
- ☐ Import `BOM-rev4-delta-2-replacements.csv` → order.
- ☐ Physically quarantine the superseded parts — 6 × 47 k (the would-be R_fb), 6 × 10 k,
  3 × ECA-1VM222, 6 × ECA-1VM101, 3 × surplus 4880SG — in a bag marked
  **"rev 3 — do not stuff, see DELTA doc"**.
- ☐ Verify `4880MG` availability at cart (any TO-220 mica + bushing kit substitutes).
- ☐ Cross-check final cart against `BOM-rev4.csv`, which remains the single authoritative list.
