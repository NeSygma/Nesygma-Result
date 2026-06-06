from z3 import *

# Declare variables for batches
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# Base constraints from problem statement
base_constraints = [
    # No two batches of same kind on same day
    Distinct([O1, O2, O3]),
    Distinct([P1, P2, P3]),
    Distinct([S1, S2, S3]),
    # At least one batch on Monday
    Or(O1 == 1, O2 == 1, O3 == 1, P1 == 1, P2 == 1, P3 == 1, S1 == 1, S2 == 1, S3 == 1),
    # Second oatmeal batch same day as first peanut butter batch
    O2 == P1,
    # Second sugar batch on Thursday (Thursday = 4)
    S2 == 4
]

solver = Solver()
solver.add(base_constraints)

# Helper to generate constraints for a given option
def constraints_for_option(oat_days, pb_days, sugar_days):
    constr = []
    # Oatmeal days
    for var in [O1, O2, O3]:
        constr.append(Or([var == d for d in oat_days]))
    # Peanut butter days
    for var in [P1, P2, P3]:
        constr.append(Or([var == d for d in pb_days]))
    # Sugar days
    for var in [S1, S2, S3]:
        constr.append(Or([var == d for d in sugar_days]))
    return And(constr)

# Options: (letter, oat_days, pb_days, sugar_days)
# Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5
options = [
    ("A", [1, 3, 4], [3, 4, 5], [1, 4, 5]),
    ("B", [1, 2, 4], [2, 3, 4], [1, 3, 4]),
    ("C", [2, 3, 4], [3, 4, 5], [2, 4, 5]),
    ("D", [1, 2, 4], [1, 3, 4], [1, 4, 5]),
    ("E", [1, 4, 5], [2, 3, 4], [1, 4, 5])
]

found_options = []
for letter, oat_days, pb_days, sugar_days in options:
    solver.push()
    solver.add(constraints_for_option(oat_days, pb_days, sugar_days))
    if solver.check() == sat:
        found_options.append(letter)
        # Optional: print model for debugging
        # m = solver.model()
        # print(f"Option {letter} model: O1={m[O1]}, O2={m[O2]}, O3={m[O3]}, P1={m[P1]}, P2={m[P2]}, P3={m[P3]}, S1={m[S1]}, S2={m[S2]}, S3={m[S3]}")
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