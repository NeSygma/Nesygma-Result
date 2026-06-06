from z3 import *

solver = Solver()

# Define variables for each category of work
# French novels (FN), Russian novels (RN), French plays (FP), Russian plays (RP)
FN = Int('FN')  # French novels selected (0-3)
RN = Int('RN')  # Russian novels selected (0-3)
FP = Int('FP')  # French plays selected (0-2)
RP = Int('RP')  # Russian plays selected (0-1)

# Domain constraints
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Total works selected: at least 5, at most 6
total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)

# No more than four French works are selected
french_total = FN + FP
solver.add(french_total <= 4)

# At least three but no more than four novels are selected
novels = FN + RN
solver.add(novels >= 3, novels <= 4)

# At least as many French novels as Russian novels
solver.add(FN >= RN)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(FP == 2, RP == 0))

# Define option constraints
# (A) No Russian novels and exactly one play are selected.
opt_a = And(RN == 0, FP + RP == 1)

# (B) Exactly one Russian novel and both French plays are selected.
opt_b = And(RN == 1, FP == 2)

# (C) Exactly two French novels and the Russian play are selected.
opt_c = And(FN == 2, RP == 1)

# (D) Exactly two French novels and exactly two plays are selected.
opt_d = And(FN == 2, FP + RP == 2)

# (E) Exactly two Russian novels and exactly one play are selected.
opt_e = And(RN == 2, FP + RP == 1)

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