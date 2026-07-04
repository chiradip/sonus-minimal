# Sonus Minimal — SE Class A MOSFET Amplifier — Build Handoff

Authoritative state of the project for refinement. The rev3 BOM (below / attached CSV) supersedes all earlier parts lists. Part numbers were stock-checked on DigiKey on 2026-06-26; re-verify at cart.

**Scope for refinement:** validate the cap-multiplier operating point, confirm the IRFP150N device swap against the original gain/stability targets, finalize the two unverified electrolytics, and lock heatsink length. Generate downstream artifacts as needed (LTspice deck, PCB, revised build doc).

---

## 1. Target

- Single-ended Class A MOSFET power amp, Pass First-Watt / ACA lineage.
- ~5 W/channel into 8 Ω, single-rail. Stereo (2 channels) + one PSU per chassis.
- Quantity in this BOM: **3 complete stereo amplifiers.**
- Pairs best with high-sensitivity speakers (≥ 92 dB/W/m).

## 2. Architecture

### Per channel (signal path)
Single-rail single-ended Class A. **Q1 = common-source gain (bottom), Q2 = source-follower (top).** Output is capacitor-coupled at OUT_NODE. Light global feedback. Rail topology: `+24V → Q2 → R_s2 → OUT_NODE → Q1 → R_s1 → GND`; output left, input right.

| Node | Value | Function |
|---|---|---|
| Rail | +24 V | Single clean rail (from PSU below) |
| Standing bias | 1.4 A | Class A idle current per channel |
| OUT_NODE idle | ~12 V | ≈ half rail |
| Q1, Q2 | IRFP150NPBF | Gain + follower (2 per channel) |
| R_s1, R_s2 | 0.47 Ω 3 W | Source degeneration + bias sense (0.66 V = 1.4 A) |
| C_in | 2.2 µF film | Input coupling (only in-path cap) |
| R_in | 47 k | Input load / Z |
| R_gs | 220 Ω | Q1 gate stopper |
| R_g2 | 100 Ω | Q2 gate stopper |
| R_fb | 47 k | Global feedback |
| Rb_top / Rb_bot | 47 k / 10 k | Bias divider |
| RV_bias | 10 k 25-turn | Bias fine-trim |
| Cb_filt / Cb_byp | 100 µF / 1 µF | Bias-node filter + bypass |
| C_out (+ C_out_byp) | 10000 µF (+ 1 µF film) | Output coupling (~2 Hz into 8 Ω) |
| R_dc | 100 Ω | Output bleeder / DC reference |
| C_rail (+ C_rail_byp) | 470 µF (+ 0.1 µF film) | Local rail bulk + HF bypass |

Standing dissipation ≈ 34 W/channel → heatsink target ≤ 0.5 °C/W per channel.

### PSU (one per stereo amp)
`T1 (dual 18 VAC toroid) → BR1 (bridge) → reservoir → capacitance multiplier → +24 V`

| Node | Value | Function |
|---|---|---|
| T1 | dual 18 VAC, 200–225 VA | Mains transformer |
| BR1 | 600 V / 35 A bridge | Rectifier |
| C_res | 2 × 10000 µF / 50 V ∥ (~20000 µF) | Reservoir (paralleled for low ESR) |
| Q_cm | MJE15032G (NPN, TO-220) | Cap-multiplier pass device (~2 V drop, ~6 W — heatsink it) |
| R_cm | 220 Ω 2 W | Multiplier base feed |
| C_cm | 2200 µF | Multiplier base hold |
| R_bleed | 4.7 k 2 W | Reservoir safety bleeder |
| F1 / J_mains | 2 A slow / IEC C14 fused+switched | Mains entry |

**Note:** the IRFP150N (signal MOSFET) and MJE15032G (PSU pass BJT) are different devices for different jobs — not interchangeable.

## 3. BOM — 3 stereo amplifiers (rev3)

Qty = total to order for 3 amps. Alternates are substitutes, not additional orders.

| Ref | MPN | Qty (3 amps) | /amp | Description | Alt / Notes |
|---|---|---|---|---|---|
| Q1,Q2 | IRFP150NPBF | 12 | 4 | MOSFET N-ch 100 V 42 A TO-247 | IRFP250NPBF / IXYS IRFP250. Match Vgs in pairs; buy ~16–20 to sort. |
| Q_cm | MJE15032G | 3 | 1 | BJT NPN 250 V 8 A TO-220 | BD243CG / KSC2073. Heatsink it. |
| BR1 | KBPC3506-G | 3 | 1 | Bridge 600 V 35 A | GBPC3506W-G. Schottky optional. |
| R_in,R_fb,Rb_top | MFR-25FBF52-47K | 18 | 6 | 47 k 1% 0.25 W MF | RNF14FTD47K0 |
| Rb_bot | MFR-25FBF52-10K | 6 | 2 | 10 k 1% 0.25 W MF | RNF14FTD10K0 |
| R_gs | MFR-25FBF52-220R | 6 | 2 | 220 Ω 1% 0.25 W MF | RNF14FTD220R |
| R_g2 | MFR-25FBF52-100R | 6 | 2 | 100 Ω 1% 0.25 W MF | RNF14FTD100R |
| R_s1,R_s2 | **0.47AECT-ND** | 12 | 4 | 0.47 Ω 3 W metal-oxide, non-ind | **Import in DigiKey-P/N field, not MPN.** Alt: Ohmite AG5 5 W. |
| R_dc | FMP200JR-52-100R | 6 | 2 | 100 Ω 2 W MF | FMP300JR-52-100R |
| R_cm | FMP200JR-52-220R | 3 | 1 | 220 Ω 2 W MF | FMP100JR-52-220R |
| R_bleed | FMP200JR-52-4K7 | 3 | 1 | 4.7 k 2 W MF | FMP300JR-52-4K7 |
| C_in | MKS2C042201K00JC00 | 6 | 2 | 2.2 µF 63 V film | Kemet R82 / WIMA MKP |
| C_out_byp,Cb_byp | R82EC4100DQ70K | 12 | 4 | 1 µF 100 V film (Kemet R82) | R82EC4100DQ70J |
| C_rail_byp | R82EC3100DQ70K | 6 | 2 | 0.1 µF 100 V film (Kemet R82) | R82EC3100DQ70J |
| C_out | 50USC10000MEFCSN25X50 | 6 | 2 | 10000 µF 50 V snap-in (Rubycon) | Nichicon LLR1H103MHSC |
| C_res | 50USC10000MEFCSN25X50 | 6 | 2 | 10000 µF 50 V snap-in — reservoir | **Same MPN as C_out → combine to one line, qty 12.** |
| C_cm | ECA-1VM222 | 3 | 1 | 2200 µF 35 V radial | ⚠ stock not re-verified — see Open Items |
| Cb_filt | ECA-1VM101 | 6 | 2 | 100 µF 35 V radial | ⚠ stock not re-verified — see Open Items |
| C_rail | 50PK470MEFC10X20 | 6 | 2 | 470 µF 50 V radial (Rubycon) | Nichicon UPW1H471MPD |
| RV_bias | 3296W-1-103LF | 6 | 2 | 10 k 25-turn trimpot (Bourns) | 3296Y-1-103LF |
| F1 | 0218002.MXP | 3 | 1 | 2 A slow 5×20 mm fuse | 0218002.HXP |
| INS | 4880SG | 15 | 5 | TO-247 mica + shoulder washer | Tabs = DRAIN. Verify kit contents. |
| J_in | RCJ-031 | 6 | 2 | RCA jack, chassis (CUI) | Amphenol ACJR. Verify footprint. |
| J_spk | 7019 | 6 | 2 | Dual red+black binding post (Keystone) | Pomona 6883. One per channel. |
| J_mains | 719W-UEL3BR51 | 3 | 1 | IEC C14 inlet, fused+switched | 723W-BEL3BR51A |
| T1 | 1182G18 | 3 | 1 | Toroid 225 VA dual 18 VAC (Hammond) | Antek AS-2218 (direct, cheaper) |
| HS1 | HeatsinkUSA 10.080″ | 6 | 2 | Heatsink extrusion, cut ~8″/ch | See Open Items — cut-to-length item |

### Ordering / import notes
- **0.47AECT-ND** is a DigiKey house part number — map it to the *DigiKey Part Number* field, not the MPN field, or it won't match.
- **C_out and C_res are the same MPN** (50USC10000MEFCSN25X50); the importer will show two lines — merge to one line, qty 12, or leave split.
- **T1:** Hammond 1182G18 is stocked at DigiKey/Mouser (one-stop). Antek AS-2218 is the cheaper DIY favorite but is **direct-order only (antekinc.com)** and will never appear in a distributor search.
- **HS1:** no drop-in distributor SKU exists at ≤0.5 °C/W — it's a cut-to-length item. Easiest is HeatsinkUSA direct; distributor routes are a Wakefield 1-ft extrusion stick (Mouser) or a Boyd cut-to-length quote (DigiKey).
- After import, only T1 and HS1 won't auto-match — handle those two manually.
- Stock fluctuates; confirm availability at the cart.

## 4. Open items to refine

1. **Cap-multiplier rail accuracy (priority).** With R_cm = 220 Ω feeding the MJE15032G base (β ≈ 50–100 at multi-amp load), base current = I_load/β and the drop across R_cm is I_b·220. At ~2.8 A draw and low β this drop can be large enough to collapse the +24 V rail. Verify the operating point: confirm actual load current seen by the multiplier, β at that current, resulting rail voltage and Q_cm dissipation; adjust R_cm / C_cm or pass-device choice if needed.
2. **MOSFET swap validation.** Original design narrative was framed around the IRFP240 (200 V, gm ≈ 3.2 S). IRFP150N is 100 V with higher gm and Ciss. Confirm gate-bias voltage, closed-loop gain (R_fb), and HF stability (R_gs/R_g2) still meet targets; re-trim bias. 100 V rating is ample for the 24 V rail.
3. **Reservoir sizing.** 2 × 10000 µF (~20000 µF) reservoir at ~2.8 A — confirm ripple trough stays above (24 V + multiplier drop) so the rail doesn't sag. Add parallel caps if marginal.
4. **Output corner.** 10000 µF into 8 Ω ≈ 2 Hz (≈4 Hz into 4 Ω). Confirm acceptable. Output cap sees ~12 V DC, rated 50 V — margin fine.
5. **Heatsink.** Confirm the chosen HeatsinkUSA length actually achieves ≤0.5 °C/W at ~34 W/channel (≈17 °C rise), or relax the target (≤1 °C/W → warmer but acceptable for Class A).
6. **Unverified electrolytics.** C_cm (2200 µF/35 V) and Cb_filt (100 µF/35 V) are Panasonic ECA placeholders whose stock wasn't re-checked — lock to confirmed in-stock parts (Rubycon PK / Nichicon UPW), ideally 50 V to match the rest.
7. **Mechanical fit.** Verify the TO-247 insulator kit contents, RCA footprint, and binding-post hole size against the chosen chassis.
8. **Rectifier noise.** Standard Si bridge (KBPC) relies on the multiplier to clean ripple; add a snubber or switch to Schottky if rectifier hash appears.

## 5. Files

- **`SE-ClassA-5W-BOM-3amps-digikey-rev3.csv`** — authoritative parts list (matches the BOM above).
- `02_channel_schematic.png`, `03_power_supply.png`, `01_system_block.png`, `04_physical_layout.png`, `05_build_sequence.png` — topology, PSU, layout, and bring-up visuals. Device *labels* on these predate rev3; treat this handoff's BOM as authoritative for part numbers.
- `SE-ClassA-5W-amp.md` — original design write-up (topology rationale + derived values).

Earlier BOM CSVs (`…rev2.csv`, `…digikey.csv`, `SE-ClassA-5W-BOM.csv`) are superseded — ignore.
