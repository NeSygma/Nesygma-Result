from z3 import *

solver = Solver()

# Declare Boolean variables
fn1, fn2, fn3 = Bools('fn1 fn2 fn3')
rn1, rn2, rn3 = Bools('rn1 rn2 rn3')
fp1, fp2 = Bools('fp1 fp2')
rp1 = Bool('rp1')

# Base constraints
total = Sum([fn1, fn2, fn3, rn1, rn2, rn3, fp1, fp2, rp1])
solver.add(total >= 5)
solver.add(total <= 6)

# French works <= 4
solver.add(Sum([fn1, fn2, fn3, fp1, fp2]) <= 4)

# Novels count between 3 and 4
novels = Sum([fn1, fn2, fn3, rn1, rn2, rn3])
solver.add(novels >= 3)
solver.add(novels <= 4)

# French novels >= Russian novels
solver.add(Sum([fn1, fn2, fn3]) >= Sum([rn1, rn2, rn3]))

# Implication: if both French plays selected then Russian play not selected
solver.add(Implies(And(fp1, fp2), Not(rp1)))

# Option constraints
opt_a_constr = And(Not(rn1), Not(rn2), Not(rn3))
opt_b_constr = (Sum([fn1, fn2, fn3]) == 1)
opt_c_constr = And(fp1, fp2, rp1)
opt_d_constr = And(rn1, rn2, rn3)
opt_e_constr = And(fn1, fn2, fn3, fp1, fp2)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")