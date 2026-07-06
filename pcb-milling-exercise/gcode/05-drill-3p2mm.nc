; JIG-1 rev B - drill 3.2 mm (slot T4)
; Makera Carvera - copper side UP - output pre-mirrored (do NOT mirror again)
; X0 Y0 = bottom-left of blank, Z0 = top of copper
; ATC slot map: T1 iso bit / T2 1.0mm / T3 1.6mm / T4 3.175mm / T5 2mm endmill
G21
G90
G94
G0 Z5.0
T4 M6
M3 S9000
G4 P2
; peck to -1.85 in 3 steps, feed 60
G0 X65.0 Y5
G1 Z-0.617 F60
G0 Z1.0
G1 Z-1.233 F60
G0 Z1.0
G1 Z-1.85 F60
G0 Z1.0
G0 Z5.0
G0 X5.0 Y5
G1 Z-0.617 F60
G0 Z1.0
G1 Z-1.233 F60
G0 Z1.0
G1 Z-1.85 F60
G0 Z1.0
G0 Z5.0
G0 X65.0 Y35
G1 Z-0.617 F60
G0 Z1.0
G1 Z-1.233 F60
G0 Z1.0
G1 Z-1.85 F60
G0 Z1.0
G0 Z5.0
G0 X5.0 Y35
G1 Z-0.617 F60
G0 Z1.0
G1 Z-1.233 F60
G0 Z1.0
G1 Z-1.85 F60
G0 Z1.0
G0 Z5.0
M5
G0 Z10.0
G0 X0 Y0
M30
