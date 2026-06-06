from z3 import *

solver = Solver()

# Variables: counts of each type selected
fn = Int('fn')  # French novels (0-3)
rn = Int('rn')  # Russian novels (0-3)
fp = Int('fp')  # French plays (0-2)
rp = Int('rp')  # Russian play (0-1)

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Total: at least 5, at most 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# No more than 4 French works
solver.add(fn + fp <= 4)

# At least 3 but no more than 4 novels
solver.add(fn + rn >= 3, fn + rn <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Define option constraints
opt_a = And(rn == 0, fp + rp == 1)
opt_b = And(rn == 1, fp == 2)
opt_c = And(fn == 2, rp == 1)
opt_d = And(fn == 2, fp + rp == 2)
opt_e = And(rn == 2, fp + rp == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: fn={m[fn]}, rn={m[rn]}, fp={m[fp]}, rp={m[rp]}")
    else:
        print(f"Option {letter} is UNSAT")
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