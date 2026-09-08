"""p4 — critical-word first / early restart. Verifies every number in answer.tex.

Run: python3 solve.py
Exact rational arithmetic throughout (Fraction), so no rounding can hide an error.
"""
from fractions import Fraction as F

WORD = 8  # Bytes


def arrival_times(t_first, t_extra, n):
    """Arrival time of word i (0-indexed, normal order, no reordering)."""
    return [t_first + i * t_extra for i in range(n)]


def expectation(times, probs):
    assert sum(probs) == 1, sum(probs)
    return sum(t * p for t, p in zip(times, probs))


print("=" * 66)
print("QUESTION A  —  L2: 64-Byte block, 8-Byte word")
print("=" * 66)
nA = 64 // WORD
t_first_A, t_extra_A, t_cwf_A = 90, 10, 110
print(f"words per block n = 64/8 = {nA}")

timesA = arrival_times(t_first_A, t_extra_A, nA)
print(f"arrival of word i (no reordering) = 90 + 10*i -> {timesA}")

# reference distribution: word 0 -> 30%, remaining n-1 share 70% equally
p0 = F(30, 100)
prest = (1 - p0) / (nA - 1)
probsA = [p0] + [prest] * (nA - 1)
print(f"P(word 0) = {p0} ; P(word i>0) = 0.70/{nA-1} = {prest} = {float(prest):.4f}")

# (1) neither: wait for the whole block
A1 = timesA[-1]
print(f"\n(1) neither        = 90 + (n-1)*10 = 90 + {nA-1}*10 = {A1} CCs  (independent of position)")

# (2) early restart only
A2 = expectation(timesA, probsA)
terms = " + ".join(f"{float(p):.2f}*{t}" for p, t in zip(probsA, timesA))
print(f"(2) early restart  = {terms}")
print(f"                   = {A2} = {float(A2)} CCs")
tail = sum(timesA[1:])
print(f"    check: 0.30*90 + 0.10*({'+'.join(map(str,timesA[1:]))}) "
      f"= 27 + 0.10*{tail} = {27 + F(1,10)*tail}")

# (3) both: critical word delivered first, flat cost
A3 = t_cwf_A
print(f"(3) both           = {A3} CCs  (flat; distribution irrelevant)")

sav2 = (A1 - A2) / A1
sav3 = (A1 - A3) / A1
print(f"\nsaving vs (1):  early restart {float(sav2)*100:.2f}%   both {float(sav3)*100:.2f}%")

# side calculations quoted in Question C
uniform = expectation(timesA, [F(1, nA)] * nA)
print(f"[C] if the distribution were uniform, (2) would be {uniform} CCs "
      f"-> saving {float((A1-uniform)/A1)*100:.3f}%")
print(f"[C] CWF surcharge at L2 = 110-90 = 20 CCs = {float(F(20,A1))*100:.2f}% of the block time")
print(f"[C] ideal (free CWF) saving at L2 = (160-90)/160 = {float(F(A1-90,A1))*100:.2f}%")

print()
print("=" * 66)
print("QUESTION B  —  L1: 32-Byte block, 8-Byte word, uniform references")
print("=" * 66)
nB = 32 // WORD
t_extra_B, t_cwf_B = 4, 27
print(f"words per block n = 32/8 = {nB}")

# back-solve the unknown first-word latency x from the given 20% ER reduction.
# T_orig(x)  = x + (n-1)*t_extra
# T_er(x)    = mean_i (x + i*t_extra) = x + t_extra*(n-1)/2
# reduction  = (T_orig - T_er)/T_orig = t_extra*(n-1)/2 / (x + (n-1)*t_extra) = 1/5
import sympy as sp

x = sp.Symbol('x', positive=True)
T_orig = x + (nB - 1) * t_extra_B
T_er = x + sp.Rational(t_extra_B * (nB - 1), 2)
sol = sp.solve(sp.Eq((T_orig - T_er) / T_orig, sp.Rational(20, 100)), x)
assert len(sol) == 1
xv = sol[0]
print(f"T_orig(x) = x + {nB-1}*{t_extra_B} = {sp.expand(T_orig)}")
print(f"T_er(x)   = x + {t_extra_B}*({nB-1})/2 = {sp.expand(T_er)}   (uniform 1/{nB})")
print(f"solve (T_orig - T_er)/T_orig = 20%  ->  x = {xv}")
assert xv == 18 and xv.is_integer, xv

To, Te = int(T_orig.subs(x, xv)), int(T_er.subs(x, xv))
print(f"  => original (whole block) = {To} CCs ; early restart only = {Te} CCs")
print(f"  => check ER reduction = ({To}-{Te})/{To} = {F(To-Te, To)} = {float(F(To-Te,To))*100:.0f}%")

# explicit per-word check of T_er rather than trusting the closed form
timesB = arrival_times(int(xv), t_extra_B, nB)
Te_chk = expectation(timesB, [F(1, nB)] * nB)
print(f"  => per-word check: arrivals {timesB}, mean = {Te_chk} (matches {Te})")
assert Te_chk == Te

B2 = F(To - t_cwf_B, To)
print(f"\nboth = {t_cwf_B} CCs (flat)  ->  reduction = ({To}-{t_cwf_B})/{To} = {B2} = {float(B2)*100:.0f}%")
assert (B2 * 100).denominator == 1, "second blank is not an integer"
print(f"\nBLANK 1 = {xv} CCs      BLANK 2 = {int(B2*100)}%")

# the interpretation cross-check recorded in notes.md
mixed = expectation([18] + [27] * (nB - 1), [F(1, nB)] * nB)
print(f"\n[interpretation check] if CWF were a no-op for word 0, 'both' would average "
      f"{mixed} CCs -> reduction {float((To-mixed)/To)*100:.1f}% (NOT an integer) "
      f"=> the flat reading is the intended one")

print()
print("=" * 66)
print("QUESTION C  —  side-by-side")
print("=" * 66)
print(f"{'':<22}{'L2 (A)':>12}{'L1 (B)':>12}")
print(f"{'words/block':<22}{nA:>12}{nB:>12}")
print(f"{'neither':<22}{str(A1)+' CC':>12}{str(To)+' CC':>12}")
print(f"{'early restart only':<22}{str(float(A2))+' CC':>12}{str(Te)+' CC':>12}")
print(f"{'both':<22}{str(A3)+' CC':>12}{str(t_cwf_B)+' CC':>12}")
print(f"{'saving, ER only':<22}{float(sav2)*100:>11.2f}%{float(F(To-Te,To))*100:>11.0f}%")
print(f"{'saving, both':<22}{float(sav3)*100:>11.2f}%{float(B2)*100:>11.0f}%")
print(f"{'CWF surcharge':<22}{'+20 CC':>12}{'+9 CC':>12}")
print(f"{'  as % of block time':<22}{float(F(20,A1))*100:>11.2f}%{float(F(9,To))*100:>11.0f}%")
print(f"\nAt L1, adding CWF on top of ER makes it WORSE: {Te} -> {t_cwf_B} CCs.")
print(f"At L2, adding CWF on top of ER helps: {float(A2)} -> {A3} CCs.")
