from z3 import *

solver = Solver()

# Declare variables with domains
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

# Base constraints
# 1. Total selected: 5 ≤ total ≤ 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# 2. No more than 4 French works
solver.add(fn + fp <= 4)

# 3. At least 3 but no more than 4 novels
solver.add(fn + rn >= 3, fn + rn <= 4)

# 4. At least as many French novels as Russian novels
solver.add(fn >= rn)

# 5. If both French plays are selected, then Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Domain constraints (based on available works)
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Answer choices as constraints
# (A) one French novel, two Russian novels, one French play, one Russian play
opt_a = And(fn == 1, rn == 2, fp == 1, rp == 1)

# (B) two French novels, one Russian novel, two French plays, one Russian play
opt_b = And(fn == 2, rn == 1, fp == 2, rp == 1)

# (C) two French novels, two Russian novels, two French plays
opt_c = And(fn == 2, rn == 2, fp == 2, rp == 0)

# (D) three French novels, one Russian novel, two French plays
opt_d = And(fn == 3, rn == 1, fp == 2, rp == 0)

# (E) three French novels, two Russian novels, one Russian play
opt_e = And(fn == 3, rn == 2, fp == 0, rp == 1)

# Evaluate each option using the exact skeleton
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