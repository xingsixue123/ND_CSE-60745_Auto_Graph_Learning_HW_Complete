#!/usr/bin/env python3
"""
Independent cross-check of the 1 TB footprint quoted in answer.tex.

calc_size_latency.py derives area bottom-up from the bit-cell size (0.021 um^2)
plus a 70% array-efficiency assumption. WikiChip/TSMC publish a *top-down* figure
for the same process: ~32 Mib/mm^2 of usable cache, already including the ~30%
assist-circuit overhead. Those two routes share only the process node, so if they
agree the area figure is not resting on my efficiency guess.
"""
BITCELL_UM2 = 0.021
ARRAY_EFF = 0.70
MIB_PER_MM2 = 32.0          # published usable cache density, N5, overhead included
TB_BITS = 1e12 * 8

# bottom-up: cells, then inflate for periphery
bottom_up_mm2 = TB_BITS * BITCELL_UM2 / ARRAY_EFF / 1e6
# top-down: published usable density
top_down_mm2 = (TB_BITS / 2**20) / MIB_PER_MM2

# the figure actually quoted in the answer: bit cells ONLY (no overhead at all),
# i.e. deliberately the smallest defensible number
cells_only_mm2 = TB_BITS * BITCELL_UM2 / 1e6

print(f"bottom-up (cell size + 70% eff) : {bottom_up_mm2:12,.0f} mm^2")
print(f"top-down  (32 Mib/mm^2 published): {top_down_mm2:12,.0f} mm^2")
print(f"disagreement                     : "
      f"{abs(bottom_up_mm2-top_down_mm2)/top_down_mm2*100:11.1f} %")
print()
print(f"QUOTED IN ANSWER (cells only)    : {cells_only_mm2:12,.0f} mm^2"
      f"  = {cells_only_mm2:.3e}")
print(f"  -> side {cells_only_mm2**0.5:,.0f} mm, "
      f"{cells_only_mm2/(3.14159265*150**2):.1f} x a 300 mm wafer")
print()
print("The quoted number is the SMALLEST of the three, so both independent routes")
print("to the real area are larger. The argument only needs a lower bound, so")
print("quoting the smallest keeps the conclusion conservative.")
