from z3 import *

# Variables
fn = Int('fn') # French novels (0-3)
rn = Int('rn') # Russian novels (0-3)
fp = Int('fp') # French plays (0-2)
rp = Int('rp') # Russian play (0-1)

solver = Solver()

# Constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# 1. Total selected: 5 or 6
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

# Options
# (A) one French novel and one French play (fn >= 1 and fp >= 1)
# (B) one French novel and one Russian play (fn >= 1 and rp >= 1)
# (C) one Russian novel and one French play (rn >= 1 and fp >= 1)
# (D) two French novels (fn >= 2)
# (E) two Russian novels (rn >= 2)

options = [
    ("A", And(fn >= 1, fp >= 1)),
    ("B", And(fn >= 1, rp >= 1)),
    ("C", And(rn >= 1, fp >= 1)),
    ("D", fn >= 2),
    ("E", rn >= 2)
]

# We want to find which option is true for ALL valid selections.
# This means for a given option O, there is NO valid selection where Not(O) is true.
# So we check if Not(O) is unsatisfiable.

valid_options = []
for letter, cond in options:
    solver.push()
    solver.add(Not(cond))
    if solver.check() == unsat:
        valid_options.append(letter)
    solver.pop()

print(f"STATUS: sat")
print(f"Valid options: {valid_options}")