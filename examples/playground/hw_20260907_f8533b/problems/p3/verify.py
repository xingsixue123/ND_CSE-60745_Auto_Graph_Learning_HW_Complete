"""p3 verification: way-prediction AMAT threshold.

Solves symbolically (exact rationals, no float drift), then confirms with an
independent numeric sweep. Every number quoted in answer.tex comes from here.

Run:  python3 verify.py
"""
import sympy as sp

# ---- given ----------------------------------------------------------------
t_base   = sp.Rational(11, 10)   # 1.1 ns  baseline (4-way) access time
t_hit    = sp.Rational(1)        # 1.0 ns  way-predict, prediction succeeds
t_extra  = sp.Rational(11, 10)   # 1.1 ns  ADDITIONAL when prediction fails
miss_rate = sp.Rational(1, 100)  # 1%
penalty   = sp.Integer(50)       # 50 ns additional miss penalty
reduction = sp.Rational(5, 100)  # must reduce AMAT by at least 5%

t_worst = t_hit + t_extra        # "additional" => delta, not replacement

# ---- Question A -----------------------------------------------------------
print("== Question A ==")
print(f"  best  case access = {t_hit} ns")
print(f"  worst case access = {t_hit} + {t_extra} = {t_worst} ns")

# ---- Question B -----------------------------------------------------------
a = sp.Symbol('a', positive=True)

amat_base = t_base + miss_rate * penalty
amat_wp   = (a * t_hit + (1 - a) * t_worst) + miss_rate * penalty
target    = (1 - reduction) * amat_base

print("\n== Question B ==")
print(f"  AMAT_base      = {t_base} + {miss_rate}*{penalty} = {amat_base} ns")
print(f"  AMAT_wp(a)     = {sp.simplify(sp.expand(amat_wp))} ns")
print(f"  target (<=95%) = 0.95 * {amat_base} = {target} ns  ({float(target)})")

sol = sp.solve(sp.Le(amat_wp, target), a)
print(f"  constraint solution: {sol}")

# threshold: solve the equality
a_min = sp.solve(sp.Eq(amat_wp, target), a)[0]
print(f"\n  a_min (exact)   = {a_min} = {sp.nsimplify(a_min)}")
print(f"  a_min (decimal) = {sp.N(a_min, 12)}")
print(f"  a_min (percent) = {sp.N(a_min * 100, 12)} %")

# sanity: AMAT exactly at threshold, and the reduction it achieves
amat_at = sp.simplify(amat_wp.subs(a, a_min))
print(f"  AMAT_wp(a_min)  = {amat_at} ns  (target {target}) -> "
      f"{'MATCH' if sp.simplify(amat_at - target) == 0 else 'MISMATCH'}")
print(f"  reduction at a_min = {sp.N((1 - amat_at/amat_base)*100, 10)} %")

# ---- rounding: threshold must be rounded UP -------------------------------
pct = sp.N(a_min * 100, 20)
up2 = sp.ceiling(a_min * 100 * 100) / 100     # 2 dp, rounded up
dn2 = sp.floor(a_min * 100 * 100) / 100
print(f"\n  rounded UP  to 2dp: {float(up2)} %")
print(f"  rounded DOWN to 2dp: {float(dn2)} %  <- would VIOLATE the constraint")
for label, p in (("98.18%", sp.Rational(9818, 10000)),
                 ("98.19%", sp.Rational(9819, 10000))):
    v = sp.simplify(amat_wp.subs(a, p))
    ok = sp.simplify(v - target) <= 0
    print(f"    a={label}: AMAT={sp.N(v,10)} ns  <= {float(target)}? {bool(ok)}")

# ---- independent numeric cross-check (no sympy solve) ---------------------
print("\n== numeric sweep cross-check ==")
best = None
for i in range(1000001):                       # a in steps of 1e-6
    av = i / 1000000.0
    amat = (av * 1.0 + (1 - av) * 2.1) + 0.01 * 50
    if amat <= 0.95 * 1.6 + 1e-12:
        best = av
        break
print(f"  smallest a on a 1e-6 grid meeting the bound: {best}")
print(f"  sympy threshold:                             {float(a_min)}")
print(f"  agree to 1e-6? {abs(best - float(a_min)) <= 1e-6}")
