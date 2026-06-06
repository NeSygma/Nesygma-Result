from z3 import *

# Problem analysis:
# Total works: 9 (3 French novels, 3 Russian novels, 2 French plays, 1 Russian play)
# Selection: 5-6 works total
# Constraints:
# 1. No more than 4 French works selected
# 2. At least 3 but no more than 4 novels selected
# 3. At least as many French novels as Russian novels
# 4. If both French plays selected, then Russian play not selected

# Define variables for counts
# French novels (FN), Russian novels (RN), French plays (FP), Russian play (RP)
FN = Int('FN')  # 0-3
RN = Int('RN')  # 0-3
FP = Int('FP')  # 0-2
RP = Int('RP')  # 0-1

solver = Solver()

# Domain constraints
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Total works constraint: 5-6
total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)

# Constraint 1: No more than 4 French works (FN + FP)
solver.add(FN + FP <= 4)

# Constraint 2: At least 3 but no more than 4 novels (FN + RN)
solver.add(FN + RN >= 3, FN + RN <= 4)

# Constraint 3: At least as many French novels as Russian novels
solver.add(FN >= RN)

# Constraint 4: If both French plays selected, then Russian play not selected
# FP == 2 implies RP == 0
solver.add(Implies(FP == 2, RP == 0))

# Now evaluate each option
# Option A: No Russian novels and exactly one play are selected
opt_a = And(RN == 0, FP + RP == 1)

# Option B: Exactly one Russian novel and both French plays are selected
opt_b = And(RN == 1, FP == 2)

# Option C: Exactly two French novels and the Russian play are selected
opt_c = And(FN == 2, RP == 1)

# Option D: Exactly two French novels and exactly two plays are selected
opt_d = And(FN == 2, FP + RP == 2)

# Option E: Exactly two Russian novels and exactly one play are selected
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