from z3 import *

solver = Solver()

# Variables: how many of each type to select
FN = Int('FN')  # French novels (0-3)
RN = Int('RN')  # Russian novels (0-3)
FP = Int('FP')  # French plays (0-2)
RP = Int('RP')  # Russian play (0-1)

# Domain constraints
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Total works: 5 or 6
total = FN + RN + FP + RP
solver.add(Or(total == 5, total == 6))

# Constraint 1: No more than 4 French works
solver.add(FN + FP <= 4)

# Constraint 2: At least 3 but no more than 4 novels
novels = FN + RN
solver.add(novels >= 3, novels <= 4)

# Constraint 3: At least as many French novels as Russian novels
solver.add(FN >= RN)

# Constraint 4: If both French plays selected, Russian play not selected
solver.add(Implies(FP == 2, RP == 0))

# Now check each option: "must at least select" means the option is NECESSARY
# i.e., in EVERY valid selection, the condition holds
# We check by trying to find a valid selection that VIOLATES each option

options = {
    "A": "one French novel and one French play",
    "B": "one French novel and one Russian play",
    "C": "one Russian novel and one French play",
    "D": "two French novels",
    "E": "two Russian novels"
}

# Option constraints (what the option claims must be selected)
opt_a = And(FN >= 1, FP >= 1)  # at least 1 FN and 1 FP
opt_b = And(FN >= 1, RP >= 1)  # at least 1 FN and 1 RP
opt_c = And(RN >= 1, FP >= 1)  # at least 1 RN and 1 FP
opt_d = FN >= 2                 # at least 2 FN
opt_e = RN >= 2                 # at least 2 RN

# For each option, check if it's NECESSARY (must hold in all valid selections)
# An option is necessary if its negation is UNSATISFIABLE with the base constraints
necessary_options = []

for letter, opt_constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    # Add all base constraints
    s.add(FN >= 0, FN <= 3)
    s.add(RN >= 0, RN <= 3)
    s.add(FP >= 0, FP <= 2)
    s.add(RP >= 0, RP <= 1)
    s.add(Or(total == 5, total == 6))
    s.add(FN + FP <= 4)
    s.add(novels >= 3, novels <= 4)
    s.add(FN >= RN)
    s.add(Implies(FP == 2, RP == 0))
    
    # Try to find a valid selection that VIOLATES the option
    s.add(Not(opt_constr))
    
    if s.check() == unsat:
        # Cannot violate the option => it's necessary
        necessary_options.append(letter)
        print(f"Option {letter} ({options[letter]}): NECESSARY (cannot be violated)")
    else:
        m = s.model()
        print(f"Option {letter} ({options[letter]}): NOT necessary (counterexample: FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]})")

print()
if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessary options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No necessary options found")