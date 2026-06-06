from z3 import *

solver = Solver()

# Declare variables
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

# Base constraints
solver.add(And(fuel >= 1, fuel <= 6))
solver.add(And(grain >= 1, grain <= 6))
solver.add(And(livestock >= 1, livestock <= 6))
solver.add(And(machinery >= 1, machinery <= 6))
solver.add(And(produce >= 1, produce <= 6))
solver.add(And(textiles >= 1, textiles <= 6))
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce + 1, textiles + 1 == produce))

# Define option constraints (contradictions for all but C)
opt_a_constr = And(grain == livestock)  # contradicts grain > livestock
opt_b_constr = And(produce <= fuel)   # contradicts produce > fuel
opt_c_constr = True                   # always satisfiable
opt_d_constr = And(livestock <= textiles)  # contradicts livestock > textiles
opt_e_constr = And(grain == textiles)   # contradicts grain > textiles (implied)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")