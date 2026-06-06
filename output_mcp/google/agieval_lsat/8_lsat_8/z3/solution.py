from z3 import *

solver = Solver()

# Variables
fn = Int('fn') # French novels (0-3)
rn = Int('rn') # Russian novels (0-3)
fp = Int('fp') # French plays (0-2)
rp = Int('rp') # Russian play (0-1)

# Domains
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Constraints
# 1. Total selected is 5 or 6
total = fn + rn + fp + rp
solver.add(Or(total == 5, total == 6))

# 2. No more than four French works
solver.add(fn + fp <= 4)

# 3. At least three but no more than four novels
solver.add(fn + rn >= 3, fn + rn <= 4)

# 4. At least as many French novels as Russian novels
solver.add(fn >= rn)

# 5. If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Answer Choices
options = [
    ("A", rn == 0),
    ("B", fn == 1),
    ("C", And(fp == 2, rp == 1)),
    ("D", rn == 3),
    ("E", And(fn == 3, fp == 2))
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