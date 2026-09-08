"""Exact verification of Problem 1, Questions B, C, D (CSE 60321 HW2).

Uses Fraction throughout so no result depends on binary floating point.
Run:  python3 verify.py
"""
from fractions import Fraction as F

# ---------------------------------------------------------------- constants
BLOCK      = 128          # Bytes per block, all caches
L2_SIZE    = 512 * 1024   # Bytes (1KB = 2^10 B per the assignment's unit convention)
WAYS       = 4
ADDR_BITS  = 64
HT_L1, HT_L2, HT_L3 = 1, 10, 50            # CCs
MR_L1, MR_L2, MR_L3 = F(5,100), F(40,100), F(20,100)   # local miss rates
EXTRA_CC   = 10           # CCs per *additional* bus transfer
CLOCK_GHZ  = F(2)         # -> 1 CC = 0.5 ns
NS_PER_CC  = 1 / CLOCK_GHZ

def log2int(n):
    assert n > 0 and (n & (n - 1)) == 0, f"{n} is not a power of two"
    return n.bit_length() - 1

def p_l3(M, bus_bytes):
    """L3 miss penalty in CCs. The 'initial' time M already covers the FIRST
    transfer, so only (transfers - 1) additional transfers are charged."""
    transfers = F(BLOCK, bus_bytes)
    assert transfers.denominator == 1, "block must be a whole number of transfers"
    return M + EXTRA_CC * (int(transfers) - 1)

def amat(M, bus_bytes):
    """Nested AMAT: a miss penalty is charged ON TOP OF that level's hit time."""
    return HT_L1 + MR_L1 * (HT_L2 + MR_L2 * (HT_L3 + MR_L3 * p_l3(M, bus_bytes)))

# ---------------------------------------------------------------- Question B
offset = log2int(BLOCK)                       # byte addressable within the block
blocks = L2_SIZE // BLOCK
sets   = blocks // WAYS
index  = log2int(sets)
tag    = ADDR_BITS - index - offset
print("=== Question B ===")
print(f"  block = {BLOCK} B          -> offset = {offset} bits")
print(f"  blocks = {L2_SIZE}/{BLOCK} = {blocks}")
print(f"  sets   = {blocks}/{WAYS} = {sets} = 2^{index} -> index = {index} bits")
print(f"  tag    = {ADDR_BITS} - {index} - {offset} = {tag} bits")
assert tag + index + offset == ADDR_BITS
print(f"  check: {tag} + {index} + {offset} = {tag+index+offset} = {ADDR_BITS}  OK")
# 64-bit word size must NOT shrink the offset:
assert offset == log2int(BLOCK), "byte-addressable entries => offset addresses bytes"

# ---------------------------------------------------------------- Question C
# Solve amat(M, 16) <= 4 for M, by unwinding the nesting exactly.
BUDGET = F(4)
t1 = (BUDGET - HT_L1) / MR_L1            # allowed P_L1
t2 = (t1 - HT_L2) / MR_L2                # allowed P_L2
t3 = (t2 - HT_L3) / MR_L3                # allowed P_L3
additional_16 = BLOCK // 16 - 1
M_max = t3 - EXTRA_CC * additional_16
print("\n=== Question C ===")
print(f"  transfers on a 16 B bus = {BLOCK}/16 = {BLOCK//16}, additional = {additional_16}")
print(f"  P_L1 <= ({BUDGET} - {HT_L1})/{MR_L1} = {t1} CC")
print(f"  P_L2 <= ({t1} - {HT_L2})/{MR_L2} = {t2} CC")
print(f"  P_L3 <= ({t2} - {HT_L3})/{MR_L3} = {t3} CC")
print(f"  M    <= {t3} - {EXTRA_CC}*{additional_16} = {M_max} CC")
print(f"  M    <= {M_max} CC * {NS_PER_CC} ns/CC = {float(M_max*NS_PER_CC)} ns")
# independent back-substitution check
assert amat(M_max, 16) == BUDGET, amat(M_max, 16)
print(f"  back-substitution: AMAT(M={M_max}, 16 B bus) = {amat(M_max,16)} CC  == 4  OK")
assert amat(M_max + 1, 16) > BUDGET   # the bound is tight

# ---------------------------------------------------------------- Question D
additional_32 = BLOCK // 32 - 1
pd = p_l3(M_max, 32)
ad = amat(M_max, 32)
print("\n=== Question D ===")
print(f"  transfers on a 32 B bus = {BLOCK}/32 = {BLOCK//32}, additional = {additional_32}")
print(f"  P_L3 = {M_max} + {EXTRA_CC}*{additional_32} = {pd} CC")
print(f"  P_L2 = {HT_L3} + {MR_L3}*{pd} = {HT_L3 + MR_L3*pd} CC")
print(f"  P_L1 = {HT_L2} + {MR_L2}*{HT_L3+MR_L3*pd} = {HT_L2 + MR_L2*(HT_L3+MR_L3*pd)} CC")
print(f"  AMAT = {HT_L1} + {MR_L1}*{HT_L2+MR_L2*(HT_L3+MR_L3*pd)} = {ad} CC = {float(ad)} CC")
print(f"  sanity: 32 B bus is faster than 16 B bus? {ad} < {amat(M_max,16)} -> {ad < amat(M_max,16)}")
