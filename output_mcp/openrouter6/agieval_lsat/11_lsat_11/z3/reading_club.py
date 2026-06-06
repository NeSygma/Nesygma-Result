from z3 import *

# Declare variables
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

# Domain constraints
domain = [
    fn >= 0, fn <= 3,
    rn >= 0, rn <= 3,
    fp >= 0, fp <= 2,
    rp >= 0, rp <= 1
]

# Base constraints
total = fn + rn + fp + rp
base_constraints = domain + [
    total >= 5, total <= 6,          # at least five and at most six works
    fn + fp <= 4,                    # no more than four French works
    fn + rn >= 3, fn + rn <= 4,      # at least three but no more than four novels
    fn >= rn,                        # at least as many French novels as Russian novels
    Or(fp != 2, rp == 0)             # if both French plays selected, Russian play not selected
]

# Create solver
solver = Solver()
solver.add(base_constraints)

# Define option constraints
opt_a = And(rn == 0, fp + rp == 1)
opt_b = And(rn == 1, fp == 2)
opt_c = And(fn == 2, rp == 1)
opt_d = And(fn == 2, fp + rp == 2)
opt_e = And(rn == 2, fp + rp == 1)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")