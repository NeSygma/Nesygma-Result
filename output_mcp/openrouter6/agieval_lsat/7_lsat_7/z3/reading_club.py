from z3 import *

solver = Solver()

# Declare variables
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

# Bounds
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Base constraints
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)          # at least 5 and at most 6 works
solver.add(fn + fp <= 4)                    # no more than 4 French works
solver.add(fn + rn >= 3, fn + rn <= 4)      # at least 3 but no more than 4 novels
solver.add(fn >= rn)                        # at least as many French novels as Russian novels
solver.add(Implies(fp == 2, rp == 0))       # if both French plays selected, Russian play not selected

# Options
options = [
    ("A", And(fn == 1, rn == 2, fp == 1, rp == 1)),
    ("B", And(fn == 2, rn == 1, fp == 2, rp == 1)),
    ("C", And(fn == 2, rn == 2, fp == 2, rp == 0)),
    ("D", And(fn == 3, rn == 1, fp == 2, rp == 0)),
    ("E", And(fn == 3, rn == 2, fp == 0, rp == 1))
]

found_options = []
for letter, constr in options:
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