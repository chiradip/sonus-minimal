; JIG-1 rev B - 01 isolation (slot T1: 0.2mm-tip V-bit or 0.2mm corn mill)
; Makera Carvera - copper side UP - output pre-mirrored (do NOT mirror again)
; X0 Y0 = bottom-left of blank, Z0 = top of copper
; ATC slot map: T1 iso bit / T2 1.0mm / T3 1.6mm / T4 3.175mm / T5 2mm endmill
G21
G90
G94
G0 Z5.0
T1 M6
M3 S12000
G4 P2
; depth -0.2 mm, feed 300, two passes per island
; island VIN+ offset 0.15
G0 X66.15 Y18.85
G1 Z-0.2 F100
G1 X53.85 Y18.85 F300
G1 X53.85 Y29.15 F300
G1 X66.15 Y29.15 F300
G1 X66.15 Y18.85 F300
G0 Z5.0
; island VIN+ offset 0.4
G0 X66.4 Y18.6
G1 Z-0.2 F100
G1 X53.6 Y18.6 F300
G1 X53.6 Y29.4 F300
G1 X66.4 Y29.4 F300
G1 X66.4 Y18.6 F300
G0 Z5.0
; island DG offset 0.15
G0 X16.15 Y9.85
G1 Z-0.2 F100
G1 X5.85 Y9.85 F300
G1 X5.85 Y29.15 F300
G1 X16.15 Y29.15 F300
G1 X16.15 Y9.85 F300
G0 Z5.0
; island DG offset 0.4
G0 X16.4 Y9.6
G1 Z-0.2 F100
G1 X5.6 Y9.6 F300
G1 X5.6 Y29.4 F300
G1 X16.4 Y29.4 F300
G1 X16.4 Y9.6 F300
G0 Z5.0
M5
G0 Z10.0
G0 X0 Y0
M30
