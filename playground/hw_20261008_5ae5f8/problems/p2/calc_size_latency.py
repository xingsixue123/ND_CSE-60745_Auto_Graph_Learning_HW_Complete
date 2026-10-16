#!/usr/bin/env python3
"""
Supporting magnitudes for Ex. 3.2.

Question: if we built one giant memory out of "the fastest materials available",
as big as some terabytes, would that remove the need for a memory hierarchy?

The answer rests on the claim that CAPACITY ITSELF COSTS LATENCY, independent of
what the cells are made of, because a signal has to physically cross the array.
This script puts numbers on that claim so the answer does not assert any figure
that was not computed.

Everything below is arithmetic on three published/physical constants; nothing is
simulated and nothing is fitted.
"""

# ---------------------------------------------------------------- constants
# 6T SRAM bit-cell area. SRAM is the fastest RAM *technology* manufacturable at
# scale, which is why it stands in for "the fastest material available".
#
# CAREFUL (validator defect 1.1): within SRAM, 0.021 um^2 is the TSMC N5
# HIGH-DENSITY cell -- the *densest*, not the *fastest*. The same source lists a
# HIGH-PERFORMANCE variant at 0.025 um^2, which is the faster flavour. Do not call
# 0.021 "the fastest cell"; an earlier draft of answer.tex did and it was false.
#
# Using the DENSEST cell is nonetheless the right choice here, because the argument
# needs a LOWER bound on physical size: the densest cell gives the smallest array,
# hence the smallest crossing time. The genuinely faster cell is 19% larger, so it
# yields a worse floor (2.0e5 mm^2, 447 mm, 2.98 ns, ~12 cycles). Quoting the dense
# cell therefore concedes the most ground possible to the question's premise.
SRAM_BITCELL_UM2 = 0.021

# Fraction of array area that is actual bit cells. Decoders, word-line drivers,
# sense amplifiers, buses and redundancy take the rest. 100% is impossible; 70%
# is generous for a very large array. Report both so the floor is unarguable.
ARRAY_EFFICIENCY = 0.70

C_M_PER_S = 2.99792458e8      # speed of light in vacuum: a hard physical floor
CLOCK_GHZ = 4.0               # representative modern CPU core clock
WAFER_DIAM_MM = 300.0         # standard production wafer

TB_BYTES = 1e12               # "as big as some terabytes" -> 1 TB is the LOWER bound


def footprint(capacity_bytes, efficiency=1.0):
    """Returns (area_mm2, side_mm) for a square array of this capacity."""
    bits = capacity_bytes * 8
    area_um2 = bits * SRAM_BITCELL_UM2 / efficiency
    area_mm2 = area_um2 / 1e6          # 1 mm^2 = 1e6 um^2
    side_mm = area_mm2 ** 0.5
    return area_mm2, side_mm


def light_time_ns(distance_mm):
    return (distance_mm / 1000.0) / C_M_PER_S * 1e9


def report(label, capacity_bytes, efficiency):
    area_mm2, side_mm = footprint(capacity_bytes, efficiency)
    # A request must travel in (address -> decoder -> cell) and the data back out.
    # Half the side length each way is the *average*; use the full side as the
    # worst-case one-way distance and twice it for the round trip.
    one_way_ns = light_time_ns(side_mm)
    round_trip_ns = 2 * one_way_ns
    print(f"  {label}")
    print(f"    cell area ........... {area_mm2:,.0f} mm^2"
          f"  ({area_mm2 / (3.141592653589793 * (WAFER_DIAM_MM/2)**2):.2f}"
          f" x a {WAFER_DIAM_MM:.0f} mm wafer)")
    print(f"    square side ......... {side_mm:,.0f} mm  ({side_mm/1000:.2f} m)")
    print(f"    light, one way ...... {one_way_ns:.2f} ns")
    print(f"    light, round trip ... {round_trip_ns:.2f} ns"
          f"  = {round_trip_ns * CLOCK_GHZ:.0f} cycles at {CLOCK_GHZ:.0f} GHz")
    return side_mm, round_trip_ns


print(__doc__)
print("=" * 72)
print(f"1) Physical size of a 1 TB array of the DENSEST real memory cells")
print(f"   (bit cell = {SRAM_BITCELL_UM2} um^2, 1 TB = {TB_BYTES:.0e} bytes"
      f" = {TB_BYTES*8:.1e} bits)")
print()
side_ideal, rt_ideal = report("bit cells only (array efficiency 100%, impossible):",
                              TB_BYTES, 1.0)
print()
side_real, rt_real = report(f"with periphery (array efficiency "
                            f"{ARRAY_EFFICIENCY:.0%}, generous):",
                            TB_BYTES, ARRAY_EFFICIENCY)

print()
print("=" * 72)
print("2) Latency floor vs. capacity: same cell, same material, only size changes.")
print("   A square array's side goes as sqrt(capacity), so the speed-of-light")
print("   round trip does too. This is the whole argument in one table.")
print()
print(f"   {'capacity':>12}  {'side (mm)':>10}  {'c round trip':>13}"
      f"  {'cycles @ ' + str(int(CLOCK_GHZ)) + 'GHz':>15}")
for name, cap in [("32 KB  (L1)", 32 * 1024),
                  ("1 MB   (L2)", 1024 ** 2),
                  ("32 MB  (L3)", 32 * 1024 ** 2),
                  ("1 GB", 1024 ** 3),
                  ("1 TB", int(TB_BYTES))]:
    _, side = footprint(cap, ARRAY_EFFICIENCY)
    rt = 2 * light_time_ns(side)
    print(f"   {name:>12}  {side:>10,.2f}  {rt:>10.3f} ns  {rt*CLOCK_GHZ:>15.1f}")

_, s_l1 = footprint(32 * 1024, ARRAY_EFFICIENCY)
_, s_tb = footprint(TB_BYTES, ARRAY_EFFICIENCY)
print()
print(f"   ratio 1 TB : 32 KB  side = {s_tb/s_l1:,.0f}x"
      f"   (= sqrt({TB_BYTES/(32*1024):,.0f}) = {(TB_BYTES/(32*1024))**0.5:,.0f})")

print()
print("=" * 72)
print("3) The number the answer actually quotes.")
print(f"   A 1 TB array of the densest available cells is at least"
      f" ~{side_ideal/1000:.1f} m across.")
print(f"   Crossing it and returning takes >= {rt_ideal:.1f} ns IN VACUUM,"
      f" i.e. >= {rt_ideal*CLOCK_GHZ:.0f} clock")
print(f"   cycles at {CLOCK_GHZ:.0f} GHz, before a single transistor switches.")
print(f"   Real on-chip signalling is several times slower than c (RC-loaded wires,")
print(f"   repeater stages), so this is a floor, not an estimate.")
print()
print(f"   For comparison, a real L3 cache answers in ~40 cycles. So the giant")
print(f"   device's *physical lower bound* is already in L3 territory"
      f" ({rt_ideal*CLOCK_GHZ:.0f} cycles),")
print(f"   and nothing about the choice of material can move it.")
