from z3 import *

solver = Solver()

# Variables: number of each type selected
fn = Int('fn')  # French novels (0-3)
rn = Int('rn')  # Russian novels (0-3)
fp = Int('fp')  # French plays (0-2)
rp = Int('rp')  # Russian play (0-1)

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Constraint 1: Total selected between 5 and 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# Constraint 2: No more than 4 French works
solver.add(fn + fp <= 4)

# Constraint 3: At least 3 but no more than 4 novels
solver.add(fn + rn >= 3, fn + rn <= 4)

# Constraint 4: At least as many French novels as Russian novels
solver.add(fn >= rn)

# Constraint 5: If both French plays selected, Russian play not selected
solver.add(Implies(fp == 2, rp == 0))

# Define each option's constraints
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