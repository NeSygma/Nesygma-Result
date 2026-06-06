from z3 import *

solver = Solver()

# Variables: number of each type of work selected
fn = Int('fn')  # French novels (max 3)
rn = Int('rn')  # Russian novels (max 3)
fp = Int('fp')  # French plays (max 2)
rp = Int('rp')  # Russian play (max 1)

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Total works: at least 5, at most 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# No more than 4 French works
french = fn + fp
solver.add(french <= 4)

# At least 3 but no more than 4 novels
novels = fn + rn
solver.add(novels >= 3, novels <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Define each option as a constraint
opt_a = And(fn == 1, rn == 2, fp == 1, rp == 1)
opt_b = And(fn == 2, rn == 1, fp == 2, rp == 1)
opt_c = And(fn == 2, rn == 2, fp == 2, rp == 0)
opt_d = And(fn == 3, rn == 1, fp == 2, rp == 0)
opt_e = And(fn == 3, rn == 2, fp == 0, rp == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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