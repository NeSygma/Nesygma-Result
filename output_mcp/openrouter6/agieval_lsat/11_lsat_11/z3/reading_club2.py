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
base_constraints = domain + [
    (fn + rn + fp + rp) >= 5, (fn + rn + fp + rp) <= 6,
    fn + fp <= 4,
    (fn + rn) >= 3, (fn + rn) <= 4,
    fn >= rn,
    Or(fp != 2, rp == 0)
]

solver = Solver()
solver.add(base_constraints)

# Define option constraints
opt_a = And(rn == 0, fp + rp == 1)
opt_b = And(rn == 1, fp == 2)
opt_c = And(fn == 2, rp == 1)
opt_d = And(fn == 2, fp + rp == 2)
opt_e = And(rn == 2, fp + rp == 1)

# Evaluate each option for satisfiability
unsat_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == unsat:
        unsat_options.append(letter)
    solver.pop()

# Output result
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple unsatisfiable options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No unsatisfiable options found")