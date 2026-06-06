from z3 import *

# Declare variables
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

solver = Solver()

# Base constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Total works between 5 and 6
solver.add(fn + rn + fp + rp >= 5, fn + rn + fp + rp <= 6)

# No more than four French works
solver.add(fn + fp <= 4)

# Novels between 3 and 4
solver.add(fn + rn >= 3, fn + rn <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays selected then Russian play not selected
solver.add(Or(fp != 2, rp == 0))

# Define option constraints
opt_a_constr = And(fn == 1, rn == 2, fp == 1, rp == 1)
opt_b_constr = And(fn == 2, rn == 1, fp == 2, rp == 1)
opt_c_constr = And(fn == 2, rn == 2, fp == 2, rp == 0)
opt_d_constr = And(fn == 3, rn == 1, fp == 2, rp == 0)
opt_e_constr = And(fn == 3, rn == 2, fp == 0, rp == 1)

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