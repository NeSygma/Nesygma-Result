from z3 import *

solver = Solver()

# Works: 3 French novels (FN0, FN1, FN2), 3 Russian novels (RN0, RN1, RN2),
# 2 French plays (FP0, FP1), 1 Russian play (RP0)
# Total 9 works.

# Boolean variables: True if selected
FN = [Bool(f'FN_{i}') for i in range(3)]
RN = [Bool(f'RN_{i}') for i in range(3)]
FP = [Bool(f'FP_{i}') for i in range(2)]
RP = [Bool(f'RP_{0}') for i in range(1)]  # just one

# Helper: total selected
total_selected = Sum([If(b, 1, 0) for b in FN + RN + FP + RP])

# Constraint: at least 5, at most 6 works selected
solver.add(total_selected >= 5)
solver.add(total_selected <= 6)

# French works: FN + FP
french_works = Sum([If(b, 1, 0) for b in FN + FP])
solver.add(french_works <= 4)

# Novels: FN + RN
novels = Sum([If(b, 1, 0) for b in FN + RN])
solver.add(novels >= 3)
solver.add(novels <= 4)

# At least as many French novels as Russian novels
french_novels = Sum([If(b, 1, 0) for b in FN])
russian_novels = Sum([If(b, 1, 0) for b in RN])
solver.add(french_novels >= russian_novels)

# If both French plays are selected, then Russian play is not selected
both_french_plays = And(FP[0], FP[1])
solver.add(Implies(both_french_plays, Not(RP[0])))

# Now evaluate each option

# Option A: No Russian novels are selected.
opt_a = russian_novels == 0

# Option B: Exactly one French novel is selected.
opt_b = french_novels == 1

# Option C: All three plays are selected (2 French plays + 1 Russian play)
opt_c = And(FP[0], FP[1], RP[0])

# Option D: All three Russian novels are selected.
opt_d = russian_novels == 3

# Option E: All five French works are selected (3 French novels + 2 French plays)
opt_e = french_works == 5

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