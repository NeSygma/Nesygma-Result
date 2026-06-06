from z3 import *

# Declare selection variables
fn = [Bool(f'fn_{i}') for i in range(3)]  # French novels
rn = [Bool(f'rn_{i}') for i in range(3)]  # Russian novels
fp = [Bool(f'fp_{i}') for i in range(2)]  # French plays
rp = Bool('rp')  # Russian play

all_vars = fn + rn + fp + [rp]

# Helper to sum Bool selections as Int
def bool_sum(lst):
    return Sum([If(v, 1, 0) for v in lst])

# Base constraints
solver = Solver()

# Total selected between 5 and 6
solver.add(bool_sum(all_vars) >= 5)
solver.add(bool_sum(all_vars) <= 6)

# No more than 4 French works (French novels + French plays)
solver.add(bool_sum(fn + fp) <= 4)

# Novels count between 3 and 4
solver.add(bool_sum(fn + rn) >= 3)
solver.add(bool_sum(fn + rn) <= 4)

# At least as many French novels as Russian novels
solver.add(bool_sum(fn) >= bool_sum(rn))

# If both French plays selected then Russian play not selected
solver.add(Implies(And(fp[0], fp[1]), Not(rp)))

# Precompute sums for options
sum_fn = bool_sum(fn)
sum_rn = bool_sum(rn)
sum_fp = bool_sum(fp)

# Define option constraints
opt_a_constr = (sum_rn == 0)  # No Russian novels
opt_b_constr = (sum_fn == 1)  # Exactly one French novel
opt_c_constr = And(fp[0], fp[1], rp)  # All three plays selected
opt_d_constr = (sum_rn == 3)  # All three Russian novels selected
opt_e_constr = And(sum_fn == 3, sum_fp == 2)  # All five French works selected

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