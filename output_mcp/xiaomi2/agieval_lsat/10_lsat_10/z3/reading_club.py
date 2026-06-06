from z3 import *

# Decision variables: number of each type selected
FN = Int('FN')  # French novels (0..3)
RN = Int('RN')  # Russian novels (0..3)
FP = Int('FP')  # French plays (0..2)
RP = Int('RP')  # Russian play (0..1)

# Base constraints from problem statement
base = [
    # Domain bounds
    FN >= 0, FN <= 3,
    RN >= 0, RN <= 3,
    FP >= 0, FP <= 2,
    RP >= 0, RP <= 1,
    # At least 5, at most 6 works total
    FN + RN + FP + RP >= 5,
    FN + RN + FP + RP <= 6,
    # No more than 4 French works
    FN + FP <= 4,
    # At least 3 but no more than 4 novels
    FN + RN >= 3,
    FN + RN <= 4,
    # At least as many French novels as Russian novels
    FN >= RN,
    # If both French plays selected, Russian play not selected
    Implies(FP == 2, RP == 0),
]

# Answer choices: what the organizer "must at least select"
# This means the condition holds in ALL valid selections
# We check by negating each option and seeing if it's unsatisfiable
options = {
    "A": And(FN >= 1, FP >= 1),   # one French novel and one French play
    "B": And(FN >= 1, RP >= 1),   # one French novel and one Russian play
    "C": And(RN >= 1, FP >= 1),   # one Russian novel and one French play
    "D": FN >= 2,                  # two French novels
    "E": RN >= 2,                  # two Russian novels
}

# For each option, check if its negation is unsatisfiable (i.e., option must be true)
must_be_true = []
for letter, condition in options.items():
    s = Solver()
    s.add(base)
    s.add(Not(condition))  # Try to find a valid selection where the option is FALSE
    result = s.check()
    if result == unsat:
        # The negation is unsatisfiable, so the option MUST be true in all valid selections
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    elif result == sat:
        m = s.model()
        print(f"Option {letter}: NOT necessarily true (counterexample: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]})")
    else:
        print(f"Option {letter}: unknown")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")