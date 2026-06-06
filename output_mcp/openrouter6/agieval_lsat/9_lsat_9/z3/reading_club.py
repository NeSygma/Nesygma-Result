from z3 import *

# Set benchmark mode
BENCHMARK_MODE = True

# Declare variables
FN = Int('FN')  # French novels selected
RN = Int('RN')  # Russian novels selected
FP = Int('FP')  # French plays selected
RP = Int('RP')  # Russian play selected

# Base constraints
solver = Solver()

# Available limits
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Total works selected between 5 and 6
total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)

# French works <= 4
solver.add(FN + FP <= 4)

# Novels between 3 and 4
solver.add(FN + RN >= 3)
solver.add(FN + RN <= 4)

# At least as many French novels as Russian novels
solver.add(FN >= RN)

# If both French plays selected, Russian play not selected
solver.add(Implies(FP == 2, RP == 0))

# Given: three French novels selected
solver.add(FN == 3)

# Define options as constraints on the remaining works
options = [
    ("A", And(RN == 1, FP == 0, RP == 0)),
    ("B", And(RN == 0, FP == 2, RP == 0)),
    ("C", And(RN == 1, FP == 0, RP == 1)),
    ("D", And(RN == 1, FP == 2, RP == 0)),
    ("E", And(RN == 2, FP == 1, RP == 0))
]

found_options = []
for letter, constr in options:
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