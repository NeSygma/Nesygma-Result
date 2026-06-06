from z3 import *

# Define variables for counts
# French novels: 0-3, Russian novels: 0-3, French plays: 0-2, Russian play: 0-1
fn = Int('French_novels')  # French novels
rn = Int('Russian_novels')  # Russian novels
fp = Int('French_plays')   # French plays
rp = Int('Russian_play')   # Russian play

solver = Solver()

# Base constraints from problem statement
# Total works selected: 5-6
solver.add(fn + rn + fp + rp >= 5)
solver.add(fn + rn + fp + rp <= 6)

# No more than 4 French works (French novels + French plays)
solver.add(fn + fp <= 4)

# At least 3 but no more than 4 novels (French novels + Russian novels)
solver.add(fn + rn >= 3)
solver.add(fn + rn <= 4)

# At least as many French novels as Russian novels
solver.add(fn >= rn)

# If both French plays are selected, then Russian play is not selected
# This is: (fp == 2) => (rp == 0)
solver.add(Implies(fp == 2, rp == 0))

# Domain constraints (can't select more than available)
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Additional condition: The selection includes exactly 3 French novels
solver.add(fn == 3)

# Now evaluate each answer choice
# Each choice represents the "remaining works" after selecting 3 French novels
# So we need to check if adding that choice to the 3 French novels satisfies all constraints

found_options = []

# Option A: one Russian novel
# This means: fn=3, rn=1, fp=0, rp=0
opt_a_constr = And(fn == 3, rn == 1, fp == 0, rp == 0)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: two French plays
# This means: fn=3, rn=0, fp=2, rp=0
opt_b_constr = And(fn == 3, rn == 0, fp == 2, rp == 0)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: one Russian novel, one Russian play
# This means: fn=3, rn=1, fp=0, rp=1
opt_c_constr = And(fn == 3, rn == 1, fp == 0, rp == 1)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: one Russian novel, two French plays
# This means: fn=3, rn=1, fp=2, rp=0
opt_d_constr = And(fn == 3, rn == 1, fp == 2, rp == 0)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: two Russian novels, one French play
# This means: fn=3, rn=2, fp=1, rp=0
opt_e_constr = And(fn == 3, rn == 2, fp == 1, rp == 0)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")