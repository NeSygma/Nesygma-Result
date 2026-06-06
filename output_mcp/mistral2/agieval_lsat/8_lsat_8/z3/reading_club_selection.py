from z3 import *

solver = Solver()

# Declare symbolic variables for the selection of works
# We have 9 works: 3 French novels (F1, F2, F3), 3 Russian novels (R1, R2, R3),
# 2 French plays (FP1, FP2), 1 Russian play (RP)

# Selection variables: 1 if selected, 0 otherwise
F_novels = [Int(f"F_novel_{i}") for i in range(3)]
R_novels = [Int(f"R_novel_{i}") for i in range(3)]
F_plays = [Int(f"F_play_{i}") for i in range(2)]
RP = Int("RP")

# Each variable is either 0 (not selected) or 1 (selected)
for v in F_novels + R_novels + F_plays:
    solver.add(Or(v == 0, v == 1))
solver.add(Or(RP == 0, RP == 1))

# Total works selected: at least 5 and at most 6
total_selected = Sum(F_novels) + Sum(R_novels) + Sum(F_plays) + RP
solver.add(total_selected >= 5, total_selected <= 6)

# No more than four French works are selected
# French works: F_novels + F_plays
french_works = Sum(F_novels) + Sum(F_plays)
solver.add(french_works <= 4)

# At least three but no more than four novels are selected
novels_selected = Sum(F_novels) + Sum(R_novels)
solver.add(novels_selected >= 3, novels_selected <= 4)

# At least as many French novels as Russian novels are selected
solver.add(Sum(F_novels) >= Sum(R_novels))

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(F_plays[0] == 1, F_plays[1] == 1), RP == 0))

# Base constraints are set. Now evaluate each option.

# Option A: No Russian novels are selected
opt_a_constr = (Sum(R_novels) == 0)

# Option B: Exactly one French novel is selected
opt_b_constr = (Sum(F_novels) == 1)

# Option C: All three plays are selected
# Plays: F_plays (2) + RP (1)
opt_c_constr = (Sum(F_plays) + RP == 3)

# Option D: All three Russian novels are selected
opt_d_constr = (Sum(R_novels) == 3)

# Option E: All five French works are selected
# French works: F_novels (3) + F_plays (2)
opt_e_constr = (Sum(F_novels) + Sum(F_plays) == 5)

# Evaluate each option
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