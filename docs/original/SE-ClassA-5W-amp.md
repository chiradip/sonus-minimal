# Sonus Minimal — 5 W Single-Ended Class A Amplifier

**Topology:** single-rail, single-ended Class A, two N-MOSFETs per channel (Pass *Amp Camp Amp* lineage), low global feedback, capacitor-coupled output.
**Design intent:** one dominant coloration — a smoothly-decaying **2nd-harmonic** envelope — and the *absence* of everything that sounds hard (crossover region, high-order products, hum, subsonic rumble). Clean digital stays clean; analog masters get body and rounded transients without their hiss being scrubbed.

> Read the two non-negotiables first (§7) before sourcing parts. The whole premise dies on a low-sensitivity speaker or an undersized heatsink.

---

## 1. Operating point (the part that makes it Class A)

For **5 W into 8 Ω**:

| Quantity | Value | Derivation |
|---|---|---|
| Peak output voltage | 8.94 V | √(2·P·R) = √(2·5·8) |
| Peak load current | 1.12 A | V_pk / R |
| **Standing bias current I_bias** | **1.4 A** | ≥ peak load current, + ~25 % margin |
| Max *Class-A* power | ~7 W | (I_bias)²·R/2 = 1.4²·8/2 |

Single-ended Class A leaves Class A when load current exceeds the standing bias. At 1.4 A bias you stay in Class A up to ~7 W into 8 Ω, so "5 W or similar" is comfortably inside the clean envelope. Above that it soft-clips on the 2nd harmonic rather than hard-clipping — which is exactly the "round" failure mode you want.

**Rail:** **+24 V** single supply. Output node idles at **~12 V** (mid-rail) for symmetric swing of roughly ±10–11 V before clip.

---

## 2. Per-channel schematic (2 × N-MOSFET)

```
                       +24V (clean rail)
                        │
                        ├──────────────┐
                        │              │ D
                  R_g2 ┌┴┐         ┌───┤ Q2  IRFP240   (upper: source-follower / current top)
                  100Ω │ │ gate    │   │ G
            bias  ─────►│ │◄─ Vbias │   S
            ref         └┬┘         │   │
                         │          ├───┴── R_s2 0.47Ω/3W ──┐
                         │          │                        │
                         │     OUT_NODE (~12V) ──────────────┼──► C_out ──► SPKR (8Ω)
                         │          │                        │     10mF + 1µF film
   IN ─C_in─┬─R_gs─►gate │ D        │                        │
   2.2µF    │       ┌────┴┐    ┌────┴┐                       │
            │  R_in │ Q1  │    │     │                       │
            │  47k  │IRFP │    │     │                       │
            │  to   │ 240 │ (lower: common-source gain)      │
            │  bias └──┬──┘                                  │
            │       G  │ S                                   │
            │          ├── R_s1 0.47Ω/3W ───────────────── GND(star)
            │          │
            └── R_fb ──┘   feedback: OUT_NODE → Q1 gate  (sets gain ~13 dB & lowers Zout)
                R_fb ≈ 47k  with R_in 47k  →  see §4
```

**Net summary (for your markdown→netlist pipeline):**

```
C_in   IN          Q1.gate        2.2uF film
R_in   Q1.gate     VBIAS          47k
R_gs   IN          Q1.gate        220R   (gate stopper, optional on input)
R_fb   OUT_NODE    Q1.gate        47k    (global feedback)
Q1     gate=Q1g drain=OUT_NODE source=S1    IRFP240
R_s1   Q1.source   GND_STAR       0.47R 3W
Q2     gate=VBIAS2 drain=+24V source=OUT_NODE  IRFP240
R_g2   VBIAS2      Q2.gate        100R   (gate stopper)
R_s2   Q2.source   OUT_NODE       0.47R 3W   (current sense / degeneration)
C_out  OUT_NODE    SPKR+          10000uF + 1uF film bypass
R_dc   SPKR+       GND            100R    (bleeds C_out, defines DC)
VBIAS  divider/zener from +24V, trimmable — sets I_bias via Q-gate voltages
```

The two 0.47 Ω source resistors are your **bias-measurement points**: 1.4 A × 0.47 Ω = **0.66 V**. You set bias by trimming `VBIAS` until you read 0.66 V across `R_s2` with a DMM. (Re-check warm; it drifts as the sink heats.)

---

## 3. Why these devices

- **IRFP240** (N-channel, 200 V, 20 A, TO-247): the canonical First-Watt device. Rugged, linear in this current range, cheap, easy to source, large tab for heatsinking. **Match the two FETs in a channel** for Vgs at 1.4 A (sort a handful with a bench supply + the DMM) — matching is what keeps the operating point and the 2nd-harmonic character consistent channel-to-channel.
- Two of the *same* device (not complementary) is deliberate: this is single-ended, not push-pull. There is no complementary pair and therefore no crossover.

---

## 4. Gain and feedback

Closed-loop gain ≈ 1 + R_fb/R_in ≈ 1 + 47k/47k ≈ **×2 of the input-stage gain**, netting roughly **+13 dB** overall after the common-source stage's contribution. That gives full output (~6.3 V RMS) from ~1.4 V RMS in — a hair above the 2 V RMS a typical DAC delivers, so you'll run at modest, very-clean levels with a 2 V source. If your DAC stage is lower (1 V), drop R_in to ~30k to raise gain.

**Feedback philosophy:** just enough to (a) set gain predictably, (b) pull output impedance down to a sane value for damping (~target Zout < 1 Ω, damping factor ~10+). *Not* so much that it scrubs the 2nd harmonic into high-order hash. This is the single knob that trades "transparent" against "round" — leave it light. Verify the resulting THD spectrum on the bench (§8) and nudge R_fb if you want more/less coloration.

---

## 5. Power supply — capacitance multiplier (the warmth-vs-hum decision)

A single-ended stage has poor PSRR, so rail ripple lands straight on the output. **That** is the source of hum and subsonic garbage — not the music. We use a **cap multiplier** (soft, ultra-quiet rail) rather than a hard regulator (more parts, more "active" character).

```
Toroid 18–20V/150–200VA ─► bridge (Schottky) ─► C_res 22mF ─┬─► R_cm 220Ω ─┬─► Q_cm base
                                                             │              └─ C_cm 2200µF ─ GND
                                                             │
                                                   Q_cm (NPN, e.g. MJL21194 or MJE15030)
                                                   C=raw+, E=+24V rail, on heatsink
                                                             │
                                                        +24V clean rail ──► both channels
```

| Item | Value | Note |
|---|---|---|
| Transformer | 18–20 V RMS sec, 150–200 VA | 20 V·1.414 − 1.4 (bridge) ≈ 27 V raw → 24 V after multiplier dropout |
| Bridge | Schottky, ≥10 A | lower switching noise than standard silicon |
| C_res reservoir | 22,000 µF / 35 V | ripple ΔV = I/(2·f·C) = 3/(2·100·0.022) ≈ 0.7 V |
| R_cm / C_cm | 220 Ω / 2200 µF | τ ≈ 0.48 s → rail ripple attenuated ~40–60 dB to µV-class |
| Q_cm | NPN power, on sink | drops ~2 V at 3 A → ~6 W, **heatsink it** |
| Bias draw | ~1.4 A × 2 ch ≈ 2.8 A | + losses → size transformer for ~3 A continuous |

Per-channel **local rail bypass**: 0.1 µF film + 470 µF electrolytic right at each Q2 drain. Choke-input (CLC) is a valid iron-based alternative if you prefer it to the transistor; the multiplier is fewer parts and silent.

---

## 6. Output coupling cap — the one approximation, handled

Single rail means a series output cap. Sized for **−3 dB at ~2 Hz into 8 Ω**:

C_out = 1 / (2π · f · R) = 1 / (2π · 2 · 8) ≈ **10,000 µF**

Use a good 10 mF / 35 V electrolytic, **bypassed with a 1 µF film**. Its corner is well below audio; in practice it contributes a faint, pleasant bottom-end roundness and — critically — blocks DC and subsonic energy from the speaker. The 100 Ω bleeder defines the speaker-side DC and prevents a turn-off thump path.

> **Want to delete this cap entirely?** Go dual-rail (±24 V) and DC-couple the output, with a DC servo (one low-offset op-amp integrator trimming Q1's gate reference). That removes the electrolytic from the signal path at the cost of a second rail + the servo. It measures cleaner; whether it *sounds* better is genuinely arguable. Recommend building the single-rail version first, then A/B if curious.

---

## 7. Two non-negotiables

1. **Speaker sensitivity ≥ 92 dB/W/m, ideally 95+.** 5–7 W is a *lot* on a 96 dB horn or efficient full-range (Fostex et al.) and *nothing* on an 85 dB bookshelf. The entire warm-low-power premise depends on this.
2. **Heatsink.** Per channel ≈ 24 V × 1.4 A ≈ **34 W standing** (Class A draws full power at idle). Target **≤ 0.5–0.6 °C/W per channel** (or one large shared extrusion ~0.3 °C/W). Keep MOSFET case < 65 °C. This, not the circuit, is the dominant mechanical design driver. Mica or silpad insulators + thermal compound under each tab; the tabs are at *drain* potential — isolate them.

---

## 8. Bench bring-up (your RIGOL + Saleae + DMM)

1. **Smoke-test the PSU alone** (amp disconnected): confirm 24 V clean rail, scope the rail for ripple — expect µV–low-mV. Confirm Q_cm dropout ~2 V.
2. **First power-up via current limit / bulb tester.** No input, no speaker. Watch rail current ramp as caps charge.
3. **Set bias:** trim VBIAS until **0.66 V across R_s2** (= 1.4 A). Let it warm 20–30 min, re-trim. Confirm both channels track.
4. **Set DC operating point:** OUT_NODE should sit ~12 V. Adjust if a channel is skewed (device matching matters here).
5. **Oscillation check (do this before connecting a speaker):** scope OUT_NODE at full bandwidth, no input. Any MHz fuzz → increase gate-stopper R (100→220→470 Ω). This is why the stoppers are there.
6. **THD spectrum:** drive ~1 kHz at ~1 W into a dummy load, FFT the output. You're looking for a **2nd-harmonic-dominant** spectrum decaying monotonically — H2 well above H3, H3 above H4, no rising high-order tail. If H3 is creeping up or it sounds hard, you have *too much* feedback or an oscillation; lighten R_fb or fix stability. This spectrum *is* the design goal made measurable.
7. **Square wave 1 kHz + 10 kHz:** clean corners, no ringing, no tilt. Tilt at LF = output cap interaction (fine if corner is ~2 Hz).

---

## 9. Board outline for CNC isolation-milling

Single-sided FR4, isolation-routed (your pipeline). Keep the board to small-signal + sense parts; the big iron lives off-board.

**Zoning (left→right signal flow):**
- **Input zone:** RCA/terminal → C_in → R_in/R_gs → Q1 gate. Short, tight, away from the power loop. Feedback trace (R_fb) returns here — keep it short and direct from OUT_NODE.
- **Active zone:** Q1 and Q2 mount at the **board edge / on the heatsink** with short flying leads so tabs reach the sink. Source resistors (R_s1, R_s2) on-board, close to their FETs (they're sense points — keep DMM-probeable).
- **Power zone:** rail entry, local bypass (470 µF + 0.1 µF film), OUT_NODE takeoff to the off-board C_out terminals.

**Grounding — single star:**
- One **star ground point** at the reservoir-cap negative.
- Separate returns brought to the star: (a) input/signal ground, (b) feedback ground, (c) R_s1 source return, (d) output-cap/speaker return, (e) PSU ground. Do **not** daisy-chain the high-current source/output return through the input ground — that's how you inject hum into a single-ended stage.

**Copper / isolation-mill specifics:**
- Leave **wide pours**; mill only isolation gaps (≥0.4 mm gap for hand-soldering tolerance). The bias path (rail → Q2 → source R → OUT_NODE) carries 1.4 A continuous — keep it as **broad copper / ≥2.5 mm equivalent**, or reinforce with bus wire tinned onto the pour.
- C_out (10 mF) and the transformer/reservoir are **off-board**; the board exposes labeled terminals/pads for them.
- Add 3–4 probe pads tied to OUT_NODE, R_s2 top, VBIAS, and rail for fast bench access.

---

## 10. BOM & where the money actually matters

**Spend here (audible):**
- C_in 2.2 µF — quality film (polypropylene). Single most "in-the-path" cap.
- VBIAS reference — stable/low-noise (good zener + RC, or a small reference). Bias-point noise = output noise here.
- C_out 10 mF + film bypass — decent electrolytic; the bypass film is cheap insurance.
- PSU reservoir + multiplier caps — low-ESR, generously rated.
- IRFP240 ×4, **matched in pairs**.

**Don't overspend (inaudible):**
- Source resistors (just need accuracy + power rating: 0.47 Ω 3 W, 1 %).
- Feedback/bias resistors (1 % metal film, ordinary).
- Connectors, chassis hardware, the heatsink-mounting screws. Audiophile spend dies here.

**Per channel active count: 2 transistors.** Whole signal path the music sees: one film cap in, one gain FET, one follower FET, one cap out. That is about as few load-bearing components as a real amplifier gets while still meeting the brief.

---

### Build order
PSU (verify clean rail) → one channel on the bench → bias/DC/oscillation/THD → second channel → match → chassis + heatsink + off-board caps → listen. Feed it from your existing low-output-impedance DAC stage on a clean single-ended line input.

---

## 11. Headphone output (300 Ω-class)

Tapped from the **speaker-side of C_out** (DC-blocked, 0 V DC — headphones never see the rail offset). This amp is a fine 250–600 Ω headphone amp; the limiting factor is the noise floor, so high-impedance/low-sensitivity cans (HD600/650/6XX, DT880-600, HD800) are the sweet spot. IEMs and sensitive low-Z cans are a poor match (audible hiss, no usable pot range).

### L-pad (per channel)

```
Node A (post-C_out) ──[jack NC contact]── SPKR+      (speaker, no series R)
Node A ──R1 470Ω── Node B ──► TRS TIP/RING (HP hot)
                     │
                    R2 47Ω
                     │
                    GND
```

| Param | 300 Ω load | Notes |
|---|---|---|
| Attenuation | ~−22 dB | maps ~80 dB SPL listening to mid-pot |
| Source impedance | ~43 Ω | R1∥R2; damping ~7 for 300 Ω |
| Max HP voltage @ full pot | ~0.5 V RMS | ~97 dB on HD650 — safety ceiling |
| R1 / R2 dissipation | <70 mW / <5 mW | ordinary ½ W metal film, NOT boutique |

Attenuation is largely independent of headphone impedance because the shunt R2 dominates the divider — this also tames level for whatever is plugged in.

### Switch (auto-mute)

Switched stereo ¼″ TRS jack (e.g. Neutrik NMJ6HF-S). Its normally-closed contacts sit **in series with the speaker lines**; the L-pad taps **before** the contacts. Plug in → speakers mute; unplug → speakers return. L-pad stays permanently connected so the amp always sees a defined load (~84 Ω with the 100 Ω R_dc bleeder in parallel). Alternative: front-panel DPDT "Speaker/Phones" toggle.

### Optional low-Z / planar setting
Switchable second L-pad: **R1 = 220 Ω / R2 = 10 Ω** → source Z ~10 Ω (damping ~3 for 32 Ω), more attenuation. Use only for low-Z cans; do not use the 43 Ω network's source impedance on multi-driver IEMs (response skew).

### Caution
Only DC-thump risk is at power-on as C_out charges (cap-multiplier soft rail rise mutes most of it). **Plug in after the supply settles; never power-cycle with cans on.**

### BOM additions
| Ref | Qty (stereo) | Value | Rating | Notes |
|---|---|---|---|---|
| R1_hp | 2 | 470 Ω | ½ W metal film 1% | series leg |
| R2_hp | 2 | 47 Ω | ½ W metal film 1% | shunt leg |
| J_hp | 1 | — | switched stereo ¼″ TRS | NC contacts mute speakers |
| (opt) R1b/R2b | 2/2 | 220 Ω / 10 Ω | ½ W | low-Z tap, switch-selected |
