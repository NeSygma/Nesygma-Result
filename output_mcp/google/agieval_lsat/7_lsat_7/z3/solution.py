from z3 import *

# Define variables for the number of each type of work selected
fn = Int('fn') # French novels
rn = Int('rn') # Russian novels
fp = Int('fp') # French plays
rp = Int('rp') # Russian plays

solver = Solver()

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Problem constraints
# 1. Total selected: 5 or 6
solver.add(fn + rn + fp + rp >= 5)
solver.add(fn + rn + fp + rp <= 6)

# 2. No more than four French works are selected
solver.add(fn + fp <= 4)

# 3. At least three but no more than four novels are selected
solver.add(fn + rn >= 3)
solver.add(fn + rn <= 4)

# 4. At least as many French novels as Russian novels are selected
solver.add(fn >= rn)

# 5. If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Test each option
options = [
    ("A", fn == 1, rn == 2, fp == 1, rp == 1),
    ("B", fn == 2, rn == 1, fp == 2, rp == 1),
    ("C", fn == 2, rn == 2, fp == 2, rp == 0),
    ("D", fn == 3, rn == 1, fp == 2, rp == 0),
    ("E", fn == 3, rn == 2, fp == 0, rp == 1)
]

found_options = []
for letter, c_fn, c_rn, c_fp, c_rp in options:
    solver.push()
    solver.add(c_fn, c_rn, c_fp, c_rp)
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