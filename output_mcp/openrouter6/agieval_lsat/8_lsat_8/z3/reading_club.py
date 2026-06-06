from z3 import *

solver = Solver()

# Variables
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Base constraints
# 1. Total selected between 5 and 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# 2. No more than four French works
solver.add(fn + fp <= 4)

# 3. At least three but no more than four novels
solver.add(fn + rn >= 3, fn + rn <= 4)

# 4. At least as many French novels as Russian novels
solver.add(fn >= rn)

# 5. If both French plays selected, then Russian play not selected
# (fp == 2) => (rp == 0)
solver.add(Or(fp != 2, rp == 0))

# Answer choices
choices = [
    ("A", rn == 0),
    ("B", fn == 1),
    ("C", And(fp == 2, rp == 1)),
    ("D", rn == 3),
    ("E", And(fn == 3, fp == 2))
]

found_options = []
for letter, constr in choices:
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