from z3 import *

# Decision variables: 0 = not assigned, 1 = Silva, 2 = Thorne
names = ['Frost','Gonzalez','Heideck','Knutson','Lai','Mays']
vars = {n: Int(n) for n in names}

base = Solver()
# domain
for v in vars.values():
    base.add(Or(v==0, v==1, v==2))
# at least two each
silva = Sum([If(v==1,1,0) for v in vars.values()])
thorne = Sum([If(v==2,1,0) for v in vars.values()])
base.add(silva >= 2, thorne >= 2)
# Frost with Heideck same ceremony non-zero
F=vars['Frost']; H=vars['Heideck']
base.add(F==H, F!=0)
# Lai and Mays both assigned must be different ceremonies
L=vars['Lai']; M=vars['Mays']
base.add(Not(And(L!=0, M!=0, L==M)))
# Gonzalez to Silva => Lai to Thorne
G=vars['Gonzalez']
base.add(Implies(G==1, L==2))
# original constraint
K=vars['Knutson']
orig = Implies(K != 2, And(H == 2, M == 2))

# options definitions
opt_a = Implies(K == 1, Not(And(H == 1, M == 1)))
opt_b = Implies(K == 1, L == 1)
opt_c = Implies(K != 2, And(F == 2, M == 2))
opt_d = Implies(K != 2, Not(And(H != 0, L != 0, H == L)))
opt_e = Implies(And(H != 2, M != 2), K == 2)
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

equiv = []
for letter, opt in options:
    # check base+orig+Not(opt) unsat
    s1 = Solver()
    s1.add(base.assertions())
    s1.add(orig)
    s1.add(Not(opt))
    res1 = s1.check()
    # check base+opt+Not(orig) unsat
    s2 = Solver()
    s2.add(base.assertions())
    s2.add(opt)
    s2.add(Not(orig))
    res2 = s2.check()
    if res1 == unsat and res2 == unsat:
        equiv.append(letter)

if len(equiv) == 1:
    print("STATUS: sat")
    print(f"answer:{equiv[0]}")
else:
    print("STATUS: unsat")
    print(f"equiv options: {equiv}")