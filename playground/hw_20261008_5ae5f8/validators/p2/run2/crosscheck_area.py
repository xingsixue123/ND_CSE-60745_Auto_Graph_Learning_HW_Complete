#!/usr/bin/env python3
"""
Consistency check on the 1 TB footprint quoted in answer.tex.

WHAT THIS IS NOT. An earlier version of this file claimed the two routes below
"share only the process node" and that their agreement showed the area did not rest
on my array-efficiency assumption. That was wrong, and the validator was right to
call it: the published ~32 Mib/mm^2 density is itself derived from the same
0.021 um^2 cell by assuming ~30% assist-circuit overhead -- which is exactly my own
70% efficiency constant. The two routes are the same assumption written two ways, so
their agreement is near arithmetic identity, not independent corroboration. The check
below is reported with that correction applied, and the inversion at the bottom makes
the circularity explicit rather than hiding it.

WHAT IT IS GOOD FOR. It still confirms one real thing: that my 70% efficiency
constant is numerically the same assumption the published density uses, i.e. that I
have not mis-stated the industry convention.

WHAT THE ANSWER ACTUALLY QUOTES. 1.68e5 mm^2, the bit-cells-only figure, which
carries NO efficiency assumption at all -- it is just (bits x cell area). That is why
the delivered number needs no corroboration from this script: it is a strict lower
bound on area, and both overhead-inclusive routes are larger.
"""
BITCELL_UM2 = 0.021
ARRAY_EFF = 0.70
MIB_PER_MM2 = 32.0          # published usable cache density, N5, overhead included
TB_BITS = 1e12 * 8

bottom_up_mm2 = TB_BITS * BITCELL_UM2 / ARRAY_EFF / 1e6
top_down_mm2 = (TB_BITS / 2**20) / MIB_PER_MM2
cells_only_mm2 = TB_BITS * BITCELL_UM2 / 1e6      # <-- the figure quoted in answer.tex

print(__doc__)
print("=" * 72)
print(f"bottom-up (cell size + 70% eff)  : {bottom_up_mm2:12,.0f} mm^2")
print(f"top-down  (32 Mib/mm^2 published): {top_down_mm2:12,.0f} mm^2")
print(f"difference                       : "
      f"{abs(bottom_up_mm2-top_down_mm2)/top_down_mm2*100:11.1f} %")
print()
print("Why that agreement is NOT evidence -- invert both to an effective per-bit area:")
print(f"  bottom-up : {BITCELL_UM2}/{ARRAY_EFF} = {BITCELL_UM2/ARRAY_EFF:.4f} um^2/bit")
print(f"  top-down  : 1e6/(32*2^20)   = {1e6/(32*2**20):.4f} um^2/bit")
print(f"  ratio     : {(BITCELL_UM2/ARRAY_EFF)/(1e6/(32*2**20)):.4f}")
print("  Same cell, same ~30% overhead. The residual is 1 MiB vs 1e6 rounding,")
print("  not an independent measurement agreeing with mine.")
print()
print("=" * 72)
print(f"QUOTED IN ANSWER (cells only)    : {cells_only_mm2:12,.0f} mm^2"
      f"  = {cells_only_mm2:.3e}")
print(f"  -> side {cells_only_mm2**0.5:,.0f} mm, "
      f"{cells_only_mm2/(3.14159265*150**2):.1f} x a 300 mm wafer")
print()
print("The quoted figure is the smallest of the three and assumption-free (bits x")
print("cell area only). Both overhead-inclusive routes are larger, so the argument,")
print("which needs a LOWER bound on size, stays conservative either way.")
