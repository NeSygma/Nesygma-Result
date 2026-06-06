from z3 import *

solver = Solver()
# Decision variables: counts of each type
fn = Int('fn')  # French novels
rn = Int('rn')  # Russian novels
fp = Int('fp')  # French plays
rp = Int('rp')  # Russian play

# Domain constraints
solver.add(fn >= 0, fn <= 3)
solver.add(rn >= 0, rn <= 3)
solver.add(fp >= 0, fp <= 2)
solver.add(rp >= 0, rp <= 1)

# Base constraints
# total works between 5 and 6
total = fn + rn + fp + rp
solver.add(total >= 5, total <= 6)
# No more than four French works
solver.add(fn + fp <= 4)
# Novels between 3 and 4
solver.add(fn + rn >= 3, fn + rn <= 4)
# At least as many French novels as Russian novels
solver.add(fn >= rn)
# If both French plays selected then Russian play not selected
solver.add(Implies(fp == 2, rp == 0))

# Option constraints
opt_a_constr = And(fn >= 1, fp >= 1, fn < 2)  # A: one French novel and one French play, plus NOT D
opt_b_constr = And(fn >= 1, rp >= 1, fn < 2)  # B: one French novel and one Russian play, plus NOT D
opt_c_constr = And(rn >= 1, fp >= 1, fn < 2)  # C: one Russian novel and one French play, plus NOT D
opt_d_constr = And(fn >= 2)                     # D: two French novels (forced)
opt_e_constr = And(rn >= 2, fn < 2)            # E: two Russian novels, plus NOT D

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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