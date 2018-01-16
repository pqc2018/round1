#authors Daniel J. Bernstein and Tanja Lange

import octonions
import ref
import sys

p = ref.modulo
print ref.message
print ref.times

print "eve observes public parameters and alice's public key:"
print 'oa =',ref.oa
print 'ob =',ref.ob
print 'rA =',ref.rA

def modprecip(x):
 x %= p
 if x == 0: raise Exception('dividing by 0')
 return pow(x,p-2,p)

def octonionrecip(x):
 xnormsq = sum(xi**2 for xi in x) % p
 xconj = (x[0],-x[1],-x[2],-x[3],-x[4],-x[5],-x[6],-x[7])
 return octonions.scale(xconj,modprecip(xnormsq),p)

try:
 rArecip = octonionrecip(ref.rA)
except:
 raise Exception('public key is not invertible, skipping this case for simplicity')

try:
 obrecip = octonionrecip(ref.ob)
except:
 raise Exception('ob is not invertible, should have caught from rA test')
assert octonions.multiply(obrecip,ref.ob,p) == (1,0,0,0,0,0,0,0)

# goal: write rA as x*ob*y for some x,y in \F_p[oa]
# this forces x to be in \F_p + oa\F_p
# wlog take x to be 1 or in \F_p + oa 
for i in range(p):
 for j in [0,1]:
   if j == 0 and i != 1: continue
   x0 = (i,0,0,0,0,0,0,0)
   x1 = octonions.scale(ref.oa,j,p)
   x = octonions.summ(x0,x1,p)
   try:
     xrecip = octonionrecip(x)
   except:
     continue
   t = octonions.multiply(xrecip,ref.rA,p)
   # goal: write t as ob*y for some y in \Z[oa]
   y = octonions.multiply(obrecip,t,p)
   if octonions.multiply(y,ref.oa,p) == octonions.multiply(ref.oa,y,p):
     print "eve's secret key:",x,y
     print "now eve looks at bob's ciphertext (DH public key):"
     print 'rB =',ref.rB
     k = octonions.multiply(x,octonions.multiply(ref.rB,y,p),p)
     print "eve's session key =",k
     print 'now peek at secrets to verify attack worked:'
     print "alice's session key =",ref.k1
     print "bob's session key =",ref.k2
     sys.exit(0)
