from z3 import *

# Variables: number of works selected from each category
FN = Int('FN')  # French novels (0-3)
RN = Int('RN')  # Russian novels (0-3)
FP = Int('FP')  # French plays (0-2)
RP = Int('RP')  # Russian plays (0-1)

solver = Solver()

# Domain constraints
solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

# Total selected: at least 5, at most 6
solver.add(FN + RN + FP + RP >= 5)
solver.add(FN + RN + FP + RP <= 6)

# No more than 4 French works
solver.add(FN + FP <= 4)

# At least 3 but no more than 4 novels
solver.add(FN + RN >= 3)
solver.add(FN + RN <= 4)

# At least as many French novels as Russian novels
solver.add(FN >= RN)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(FP == 2, RP == 0))

# Now, for each option, check if it is necessarily true (must hold in ALL valid selections)
# We do this by checking if NOT(option) is unsatisfiable under the base constraints.

options = {
    "A": And(FN >= 1, FP >= 1),  # one French novel and one French play
    "B": And(FN >= 1, RP >= 1),  # one French novel and one Russian play
    "C": And(RN >= 1, FP >= 1),  # one Russian novel and one French play
    "D": FN >= 2,                # two French novels
    "E": RN >= 2                 # two Russian novels
}

must_options = []
for letter, constr in options.items():
    solver.push()
    # Check if NOT(option) is satisfiable
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        # NOT(option) is unsatisfiable => option MUST be true in all valid selections
        must_options.append(letter)
    solver.pop()

if len(must_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_options[0]}")
elif len(must_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")

# Also print all valid solutions for verification
print("\n=== All valid solutions ===")
s2 = Solver()
s2.add(FN >= 0, FN <= 3)
s2.add(RN >= 0, RN <= 3)
s2.add(FP >= 0, FP <= 2)
s2.add(RP >= 0, RP <= 1)
s2.add(FN + RN + FP + RP >= 5)
s2.add(FN + RN + FP + RP <= 6)
s2.add(FN + FP <= 4)
s2.add(FN + RN >= 3)
s2.add(FN + RN <= 4)
s2.add(FN >= RN)
s2.add(Implies(FP == 2, RP == 0))

solutions = []
while s2.check() == sat:
    m = s2.model()
    sol = {str(v): m.eval(v, model_completion=True) for v in [FN, RN, FP, RP]}
    solutions.append(sol)
    # Block this solution
    s2.add(Or([v != m.eval(v, model_completion=True) for v in [FN, RN, FP, RP]]))

print(f"Total valid solutions: {len(solutions)}")
for s in solutions:
    print(f"  FN={s['FN']}, RN={s['RN']}, FP={s['FP']}, RP={s['RP']} | Total={int(str(s['FN']))+int(str(s['RN']))+int(str(s['FP']))+int(str(s['RP']))}")