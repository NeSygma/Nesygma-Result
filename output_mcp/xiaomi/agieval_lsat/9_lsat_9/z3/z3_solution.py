from z3 import *

solver = Solver()

# Define variables for each category of works
# French novels: 3 available, Russian novels: 3 available
# French plays: 2 available, Russian play: 1 available
fn = Int('fn')  # French novels selected
rn = Int('rn')  # Russian novels selected
fp = Int('fp')  # French plays selected
rp = Int('rp')  # Russian play selected

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Total works selected: at least 5, at most 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# No more than four French works are selected
french_total = fn + fp
solver.add(french_total <= 4)

# At least three but no more than four novels are selected
novels_total = fn + rn
solver.add(novels_total >= 3, novels_total <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Given condition: works selected include three French novels
solver.add(fn == 3)

# Now test each option for the remaining works
found_options = []

# Option A: one Russian novel
solver.push()
solver.add(rn == 1, fp == 0, rp == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: two French plays
solver.push()
solver.add(rn == 0, fp == 2, rp == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: one Russian novel, one Russian play
solver.push()
solver.add(rn == 1, fp == 0, rp == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: one Russian novel, two French plays
solver.push()
solver.add(rn == 1, fp == 2, rp == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: two Russian novels, one French play
solver.push()
solver.add(rn == 2, fp == 1, rp == 0)
if solver.check() == sat:
    found_options.append("E")
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