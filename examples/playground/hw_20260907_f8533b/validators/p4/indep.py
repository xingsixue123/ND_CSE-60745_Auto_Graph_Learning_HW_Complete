from fractions import Fraction as F
# ---- A: independent, written from the page text, not from the worker's model
n=64//8
arr=[90+10*i for i in range(n)]                    # word i arrives
A1=90+(n-1)*10
p=[F(3,10)]+[F(7,10)/(n-1)]*(n-1)
assert sum(p)==1
A2=sum(a*q for a,q in zip(arr,p))
A3=110
print("A n,arr",n,arr); print("A1",A1,"A2",A2,float(A2),"A3",A3)
print("sav",float((A1-A2)/A1)*100,float((A1-A3)/A1)*100)
# brute-force B blank1 over integers instead of sympy
m=32//8
hits=[x for x in range(1,2000) if F(( (x+(m-1)*4) - (sum(F(x+4*i) for i in range(m))/m) ),(x+(m-1)*4))==F(1,5)]
print("B blank1 candidates",hits)
x=hits[0]; To=x+(m-1)*4; Te=sum(F(x+4*i) for i in range(m))/m
print("B To,Te",To,Te,"blank2",F(To-27,To),float(F(To-27,To))*100)
# C cross-checks
print("C uniformL2",sum(a*F(1,n) for a in arr), float((A1-125)/A1)*100)
print("C surcharge",F(20,A1)*100, F(9,To)*100)
print("C ceiling",F(70,160)*100, F(12,30)*100)
print("C breakeven",float(F(A1-110,To-27)))
# alternative CWF reading
print("alt A3", F(3,10)*90+F(7,10)*110, "alt B both", sum(F(x if i==0 else 27) for i in range(m))/m, float((To-F(99,4))/To)*100)
