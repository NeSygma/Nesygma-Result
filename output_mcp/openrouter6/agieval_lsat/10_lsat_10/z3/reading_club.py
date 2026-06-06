from z3 import *

solver = Solver()

# Declare variables
FN = Int('FN')  # French novels selected
RN = Int('RN')  # Russian novels selected
FP = Int('FP')  # French plays selected
RP = Int('RP')  # Russian plays selected

# Base constraints
# 1. No more than 4 French works
solver.add(FN + FP <= 4)
# 2. At least 3 but no more than 4 novels
solver.add(FN + RN >= 3)
solver.add(FN + RN <= 4)
# 3. At least as many French novels as Russian novels
solver.add(FN >= RN)
# 4. If both French plays are selected, then Russian play is not selected
solver.add(Or(FP != 2, RP == 0))
# 5. Total selected works between 5 and 6
total = FN + RN + FP + RP
solver.add(total >= 5)
solver.add(total <= 6)
# Domain constraints (optional but helpful)
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Define options as constraints that must be true for necessity
# We will check necessity by adding the negation of the option and seeing if unsat
options = [
    ("A", And(FN >= 1, FP >= 1)),          # one French novel and one French play
    ("B", And(FN >= 1, RP >= 1)),          # one French novel and one Russian play
    ("C", And(RN >= 1, FP >= 1)),          # one Russian novel and one French play
    ("D", FN >= 2),                        # two French novels
    ("E", RN >= 2)                         # two Russian novels
]

found_options = []
for letter, constr in options:
    solver.push()
    # Add the negation of the option to test necessity
    solver.add(Not(constr))
    if solver.check() == unsat:
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