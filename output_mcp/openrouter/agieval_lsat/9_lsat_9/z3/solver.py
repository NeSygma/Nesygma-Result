from z3 import *

solver = Solver()
# Variables for counts
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

# Base domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Given condition: three French novels are selected
solver.add(fn == 3)

# Total works selected between 5 and 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# No more than four French works (French novels + French plays)
solver.add(fn + fp <= 4)

# At least three but no more than four novels (French + Russian novels)
solver.add(fn + rn >= 3, fn + rn <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Define option constraints
opt_a = And(rn == 1, fp == 0, rp == 0)  # one Russian novel
opt_b = And(rn == 0, fp == 2, rp == 0)  # two French plays
opt_c = And(rn == 1, fp == 0, rp == 1)  # one Russian novel, one Russian play
opt_d = And(rn == 1, fp == 2, rp == 0)  # one Russian novel, two French plays
opt_e = And(rn == 2, fp == 1, rp == 0)  # two Russian novels, one French play

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