from z3 import *

solver = Solver()

# Variables: number of each type selected
# French Novels (FN), Russian Novels (RN), French Plays (FP), Russian Play (RP)
FN = Int('FN')
RN = Int('RN')
FP = Int('FP')
RP = Int('RP')

# Domain bounds
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Given: 3 French novels are selected
solver.add(FN == 3)

# Constraint 1: Select at least 5, at most 6 works total
total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)

# Constraint 2: No more than 4 French works
solver.add(FN + FP <= 4)

# Constraint 3: At least 3 but no more than 4 novels
solver.add(FN + RN >= 3, FN + RN <= 4)

# Constraint 4: At least as many French novels as Russian novels
solver.add(FN >= RN)

# Constraint 5: If both French plays selected, Russian play not selected
solver.add(Implies(FP == 2, RP == 0))

# Now test each answer option as the "remaining works" (besides the 3 French novels)
found_options = []

# (A) one Russian novel
opt_a = And(RN == 1, FP == 0, RP == 0)
# (B) two French plays
opt_b = And(RN == 0, FP == 2, RP == 0)
# (C) one Russian novel, one Russian play
opt_c = And(RN == 1, FP == 0, RP == 1)
# (D) one Russian novel, two French plays
opt_d = And(RN == 1, FP == 2, RP == 0)
# (E) two Russian novels, one French play
opt_e = And(RN == 2, FP == 1, RP == 0)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        t = m.eval(total)
        print(f"Option {letter}: SAT -> FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}, total={t}")
        found_options.append(letter)
    else:
        print(f"Option {letter}: UNSAT")
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