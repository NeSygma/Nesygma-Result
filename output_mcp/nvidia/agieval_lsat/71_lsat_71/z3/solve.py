from z3 import *

solver = Solver()

# Variables for each assistant: slot index 0-5
sJ = Int('sJ')
sK = Int('sK')
sL = Int('sL')
sN = Int('sN')
sO = Int('sO')
sR = Int('sR')

# Domain constraints
solver.add(And(sJ >= 0, sJ <= 5))
solver.add(And(sK >= 0, sK <= 5))
solver.add(And(sL >= 0, sL <= 5))
solver.add(And(sN >= 0, sN <= 5))
solver.add(And(sO >= 0, sO <= 5))
solver.add(And(sR >= 0, sR <= 5))
solver.add(Distinct([sJ, sK, sL, sN, sO, sR]))

# Base constraints
solver.add(Div(sK, 2) == Div(sR, 2))           # Kevin and Rebecca same day
solver.add(Div(sL, 2) != Div(sO, 2))           # Lan and Olivia different days
solver.add(Mod(sN, 2) == 1)                    # Nessa afternoon
solver.add(Div(sJ, 2) < Div(sO, 2))            # Julio earlier day than Olivia

# Option constraints (full assignment for each option)
opt_a = And(sJ == 2, sK == 1, sL == 3, sN == 4, sO == 5, sR == 0)
opt_b = And(sJ == 2, sK == 4, sL == 3, sN == 1, sO == 0, sR == 5)
opt_c = And(sJ == 3, sK == 1, sL == 0, sN == 5, sO == 4, sR == 2)
opt_d = And(sJ == 2, sK == 0, sL == 5, sN == 3, sO == 4, sR == 1)
opt_e = And(sJ == 0, sL == 1, sO == 2, sN == 3, sR == 4, sK == 5)

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