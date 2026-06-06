from z3 import *
# Variables
h = Bool('h')
a = Bool('a')
o = Bool('o')
c = Bool('c')
carb = Bool('carb')
one = Bool('one')
# Premises
prem = []
prem.append(Implies(h, o))
prem.append(Implies(a, h))
prem.append(Implies(o, c))
prem.append(Implies(o, carb))
prem.append(Implies(c, Not(one)))
# biconditional: (c & one) or (~c & ~one)
prem.append(Or(And(c, one), And(Not(c), Not(one))))
# Conclusion: (one or carb) -> (~c and ~a)
concl = Implies(Or(one, carb), And(Not(c), Not(a)))
# Check entailment
s = Solver()
for p in prem:
    s.add(p)
# Check if premises and not conclusion unsat
s1 = Solver()
for p in prem:
    s1.add(p)
s1.add(Not(concl))
res1 = s1.check()
print('prem & not concl:', res1)
# Check if premises and conclusion unsat
s2 = Solver()
for p in prem:
    s2.add(p)
s2.add(concl)
res2 = s2.check()
print('prem & concl:', res2)
# Also check if premises alone unsat
s3 = Solver()
for p in prem:
    s3.add(p)
print('prem alone:', s3.check())