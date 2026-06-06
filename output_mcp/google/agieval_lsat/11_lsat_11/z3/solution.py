from z3 import *

# Variables
fn_sel = Int('fn_sel')
rn_sel = Int('rn_sel')
fp_sel = Int('fp_sel')
rp_sel = Int('rp_sel')

solver = Solver()

# Domains
solver.add(fn_sel >= 0, fn_sel <= 3)
solver.add(rn_sel >= 0, rn_sel <= 3)
solver.add(fp_sel >= 0, fp_sel <= 2)
solver.add(rp_sel >= 0, rp_sel <= 1)

# Constraints
# 1. Total selected (S) = 5 or 6
total_sel = fn_sel + rn_sel + fp_sel + rp_sel
solver.add(Or(total_sel == 5, total_sel == 6))

# 2. No more than four French works are selected
solver.add(fn_sel + fp_sel <= 4)

# 3. At least three but no more than four novels are selected
novels_sel = fn_sel + rn_sel
solver.add(novels_sel >= 3, novels_sel <= 4)

# 4. At least as many French novels as Russian novels are selected
solver.add(fn_sel >= rn_sel)

# 5. If both French plays are selected, then the Russian play is not selected
solver.add(Implies(fp_sel == 2, rp_sel == 0))

# Options
options = [
    ("A", And(rn_sel == 0, fp_sel + rp_sel == 1)),
    ("B", And(rn_sel == 1, fp_sel == 2)),
    ("C", And(fn_sel == 2, rp_sel == 1)),
    ("D", And(fn_sel == 2, fp_sel + rp_sel == 2)),
    ("E", And(rn_sel == 2, fp_sel + rp_sel == 1))
]

# Check which options are possible (SAT)
possible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        possible_options.append(letter)
    solver.pop()

print(f"Possible options: {possible_options}")

# The question asks for the one that CANNOT be true (the one that is NOT in possible_options)
all_options = ["A", "B", "C", "D", "E"]
impossible_options = [opt for opt in all_options if opt not in possible_options]

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Found {len(impossible_options)} impossible options: {impossible_options}")