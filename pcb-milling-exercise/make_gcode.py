#!/usr/bin/env python3
"""
SONUS MINIMAL - pcb-milling-exercise: V_GS jig board (JIG-1, rev B)
G-code generator for Makera Carvera (Smoothieware-flavoured, plain G0/G1 only,
no canned cycles). Regenerate everything with:  python3 make_gcode.py

Coordinate convention
---------------------
* Artwork is designed looking at the COMPONENT side (like Fig. 9/10).
* The blank is milled COPPER SIDE UP, so all output is ALREADY MIRRORED
  about the board's X centre (x' = 70 - x). Do not mirror again in CAM.
* Origin (X0 Y0) = bottom-left corner of the blank, Z0 = top of copper.
* Board: 70 x 40 mm, FR4 single-sided, 1.6 mm thick.
"""

import os

BOARD_W, BOARD_H = 70.0, 40.0
THICK = 1.6

SAFE_Z = 5.0
ISO_Z = -0.20          # V-bit isolation depth (test-cut first!)
DRILL_Z = -1.85        # through + 0.25 into spoilboard
CUT_Z = -1.75          # cutout through
CUT_DOC = 0.45         # per pass
TAB_TOP = -1.15        # tabs: last ~0.6 mm left in 4 zones
TAB_W = 4.0

F_ISO, F_DRILL, F_CUT, F_PLUNGE = 300, 60, 250, 100
S_ISO, S_DRILL, S_CUT = 12000, 9000, 10000

# ---------------- component-side geometry (mm) ----------------
# islands (copper kept): rectangles (x1,y1,x2,y2)
ISL_VINP = (4.0, 19.0, 16.0, 29.0)    # VIN+ : supply + , R_j left
ISL_DG   = (54.0, 10.0, 64.0, 29.0)   # DG   : R_j right + DUT drain + gate (tied) + TP V+
# everything else = SRC/GND sea (supply -, DUT source, TP V-)

PADS = {
    # R_j pads are DUAL-PURPOSE (1.6 mm): axial TWW10J6R8E solders across them,
    # OR wires run from them to an off-board aluminum-housed 6.8R/10W bolted to
    # the same plate as the DUT heatsink (rev B change - see README).
    1.6: [(8, 24), (62, 24),                            # R_j (axial OR wire-off)
          (12, 27), (12, 12), (44, 12), (58, 13), (62, 13)],  # VIN+, VIN-, SRC, DRAIN, GATE
    1.0: [(59, 19), (59, 16), (26, 12), (30, 12)],     # TP loops V+ / V-
    3.2: [(5, 5), (65, 5), (5, 35), (65, 35)],         # M3 mounting
}

ISO_OFFSETS = [0.15, 0.40]   # two concentric passes -> ~0.5+ mm gap

def MX(x):          # mirror for copper-side-up machining
    return round(BOARD_W - x, 3)

def hdr(out, s, note, tool):
    out += [f"; JIG-1 rev B - {note}",
            "; Makera Carvera - copper side UP - output pre-mirrored (do NOT mirror again)",
            "; X0 Y0 = bottom-left of blank, Z0 = top of copper",
            f"; ATC slot map: T1 iso bit / T2 1.0mm / T3 1.6mm / T4 3.175mm / T5 2mm endmill",
            "G21", "G90", "G94", f"G0 Z{SAFE_Z}",
            f"T{tool} M6",
            f"M3 S{s}", "G4 P2"]
    return out

def ftr(out):
    out += ["M5", f"G0 Z{SAFE_Z + 5}", "G0 X0 Y0", "M30"]
    return "\n".join(out) + "\n"

def rect_path(x1, y1, x2, y2, e):
    """expanded rect corners, mirrored, CCW"""
    pts = [(x1 - e, y1 - e), (x2 + e, y1 - e), (x2 + e, y2 + e), (x1 - e, y2 + e)]
    return [(MX(x), round(y, 3)) for (x, y) in pts]

def isolation():
    out = hdr([], S_ISO, "01 isolation (slot T1: 0.2mm-tip V-bit or 0.2mm corn mill)", 1)
    out.append(f"; depth {ISO_Z} mm, feed {F_ISO}, two passes per island")
    for name, isl in (("VIN+", ISL_VINP), ("DG", ISL_DG)):
        for e in ISO_OFFSETS:
            p = rect_path(*isl, e)
            out.append(f"; island {name} offset {e}")
            out.append(f"G0 X{p[0][0]} Y{p[0][1]}")
            out.append(f"G1 Z{ISO_Z} F{F_PLUNGE}")
            for (x, y) in p[1:] + [p[0]]:
                out.append(f"G1 X{x} Y{y} F{F_ISO}")
            out.append(f"G0 Z{SAFE_Z}")
    return ftr(out)

def drill(dia, tool):
    out = hdr([], S_DRILL, f"drill {dia} mm (slot T{tool})", tool)
    out.append(f"; peck to {DRILL_Z} in 3 steps, feed {F_DRILL}")
    steps = [DRILL_Z / 3, 2 * DRILL_Z / 3, DRILL_Z]
    for (x, y) in PADS[dia]:
        out.append(f"G0 X{MX(x)} Y{y}")
        for z in steps:
            out.append(f"G1 Z{round(z,3)} F{F_DRILL}")
            out.append(f"G0 Z1.0")
        out.append(f"G0 Z{SAFE_Z}")
    return ftr(out)

def cutout():
    out = hdr([], S_CUT, "06 board cutout (slot T5: 2mm endmill) with 4 tabs", 5)
    # perimeter as parameterised loop, CCW from (0,0); mirrored = same rectangle
    corners = [(0, 0), (BOARD_W, 0), (BOARD_W, BOARD_H), (0, BOARD_H)]
    seglens = [BOARD_W, BOARD_H, BOARD_W, BOARD_H]
    total = 2 * (BOARD_W + BOARD_H)
    tabs = [35.0, 90.0, 145.0, 200.0]   # centres along perimeter

    def point(s):
        s %= total
        for i, L in enumerate(seglens):
            if s <= L:
                x0, y0 = corners[i]
                x1, y1 = corners[(i + 1) % 4]
                t = s / L
                return (round(x0 + (x1 - x0) * t, 3), round(y0 + (y1 - y0) * t, 3))
            s -= L

    z = 0.0
    while z > CUT_Z + 0.001:
        z = max(z - CUT_DOC, CUT_Z)
        out.append(f"; pass at Z{z:.2f}")
        # build breakpoints: tab zones only matter when z below TAB_TOP
        events = [0.0]
        if z < TAB_TOP:
            for c in tabs:
                events += [c - TAB_W / 2, c + TAB_W / 2]
        events += [total]
        p0 = point(0)
        out.append(f"G0 X{p0[0]} Y{p0[1]}")
        out.append(f"G1 Z{round(z,3)} F{F_PLUNGE}")
        for i in range(len(events) - 1):
            a, b = events[i], events[i + 1]
            in_tab = z < TAB_TOP and any(abs((a + b) / 2 - c) < TAB_W / 2 for c in tabs)
            zz = TAB_TOP if in_tab else z
            out.append(f"G1 Z{round(zz,3)} F{F_PLUNGE}")
            # walk this span passing through any corners inside it
            s = a
            while s < b - 1e-6:
                nxt = min(b, (int(s // 10) * 10) + 10)  # subdivide every 10mm for corner fidelity
                # ensure we hit exact corners
                for corner_s in (70, 110, 180, total):
                    if s < corner_s < nxt:
                        nxt = corner_s
                p = point(nxt)
                out.append(f"G1 X{p[0]} Y{p[1]} F{F_CUT}")
                s = nxt
        out.append(f"G0 Z{SAFE_Z}")
    return ftr(out)

os.makedirs("gcode", exist_ok=True)
files = {
    "gcode/01-isolation-vbit.nc": isolation(),
    "gcode/02-drill-1p0mm.nc": drill(1.0, 2),
    "gcode/04-drill-1p6mm.nc": drill(1.6, 3),
    "gcode/05-drill-3p2mm.nc": drill(3.2, 4),
    "gcode/06-cutout-2mm.nc": cutout(),
}
for name, content in files.items():
    with open(name, "w") as f:
        f.write(content)
    print(f"{name}: {len(content.splitlines())} lines")
