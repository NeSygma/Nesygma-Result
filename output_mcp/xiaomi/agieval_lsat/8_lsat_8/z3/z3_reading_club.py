from z3 import *

solver = Solver()

# Define variables for each category
# French novels (3 available)
fn = Int('fn')  # number of French novels selected
# Russian novels (3 available)
rn = Int('rn')  # number of Russian novels selected
# French plays (2 available)
fp = Int('fp')  # number of French plays selected
# Russian play (1 available)
rp = Int('rp')  # number of Russian plays selected

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Total works selected: at least 5, at most 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)

# No more than 4 French works are selected
french_total = fn + fp
solver.add(french_total <= 4)

# At least 3 but no more than 4 novels are selected
novels = fn + rn
solver.add(novels >= 3, novels <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp == 2, rp == 0))

# Now test each option
found_options = []

# Option A: No Russian novels are selected
solver.push()
solver.add(rn == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Exactly one French novel is selected
solver.push()
solver.add(fn == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: All three plays are selected
solver.push()
solver.add(fp == 2, rp == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: All three Russian novels are selected
solver.push()
solver.add(rn == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: All five French works are selected
solver.push()
solver.add(fn + fp == 5)
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