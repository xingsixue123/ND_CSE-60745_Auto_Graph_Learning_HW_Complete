import math
# Independent re-derivation, SI throughout, no shared code with worker scripts.
cell_m2 = 0.021e-12          # 0.021 um^2 -> m^2
bits    = 8 * 10**12         # 1 TB decimal
A_m2    = bits * cell_m2
side_m  = math.sqrt(A_m2)
c       = 299792458.0
rt_s    = 2*side_m/c
waf_m2  = math.pi*(0.150**2)
print("area        = %.6e m^2 = %.6e mm^2" % (A_m2, A_m2*1e6))
print("side        = %.4f m = %.3f mm" % (side_m, side_m*1e3))
print("wafers      = %.4f" % (A_m2/waf_m2))
print("round trip  = %.4f ns" % (rt_s*1e9))
print("cycles@4GHz = %.4f" % (rt_s*4e9))
# sanity: binary TB variant, and a 'what if cell were 10x smaller'
for lbl,b,cm in [("2^40 bytes", 8*2**40, cell_m2), ("cell/10", bits, cell_m2/10)]:
    a=b*cm; s=math.sqrt(a)
    print("  %-11s area=%.3e mm^2 side=%.1f mm rt=%.2f ns cyc=%.1f" % (lbl,a*1e6,s*1e3,2*s/c*1e9,2*s/c*4e9))
