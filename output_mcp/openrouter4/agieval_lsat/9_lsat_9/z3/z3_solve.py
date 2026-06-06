from z3 import *

solver = Solver()

# Decision variables (counts of selected works)
FN = Int('FN')  # French novels selected
RN = Int('RN')  # Russian novels selected
FP = Int('FP')  # French plays selected
RP = Int('RP')  # Russian plays selected (0 or 1)

# Domain constraints (total works available)
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# GIVEN: The works selected include three French novels
solver.add(FN == 3)

# Requirement: Total selected works between 5 and 6
solver.add(FN + RN + FP + RP >= 5)
solver.add(FN + RN + FP + RP <= 6)

# Requirement 1: No more than four French works selected
solver.add(FN + FP <= 4)

# Requirement 2: At least three but no more than four novels selected
solver.add(FN + RN >= 3)
solver.add(FN + RN <= 4)

# Requirement 3: At least as many French novels as Russian novels
solver.add(FN >= RN)

# Requirement 4: If both French plays are selected, then the Russian play is not selected
# FP_sel == 2  =>  RP_sel == 0
solver.add(Implies(FP == 2, RP == 0))

# Now test each option
# Each option gives a "complete and accurate list of the remaining works selected"
# So the option specifies exactly what other works are selected (nothing else)

# Option A: one Russian novel
opt_a = And(RN == 1, FP == 0, RP == 0)

# Option B: two French plays
opt_b = And(RN == 0, FP == 2, RP == 0)

# Option C: one Russian novel, one Russian play
opt_c = And(RN == 1, FP == 0, RP == 1)

# Option D: one Russian novel, two French plays
opt_d = And(RN == 1, FP == 2, RP == 0)

# Option E: two Russian novels, one French play
opt_e = And(RN == 2, FP == 1, RP == 0)

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