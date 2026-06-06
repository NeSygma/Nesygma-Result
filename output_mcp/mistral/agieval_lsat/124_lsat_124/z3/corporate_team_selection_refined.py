from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare boolean variables for each employee
employees = ["Myers", "Ortega", "Paine", "Schmidt", "Thomson", "Wong", "Yoder", "Zayre"]
selected = {e: Bool(f"selected_{e}") for e in employees}

# Initialize solver
solver = Solver()

# Constraint 1: Team size is at least 4
solver.add(Sum([selected[e] for e in employees]) >= 4)

# Constraint 2: If Myers is selected, neither Ortega nor Paine can be selected
solver.add(Implies(selected["Myers"], And(Not(selected["Ortega"]), Not(selected["Paine"]))))

# Constraint 3: If Schmidt is selected, both Paine and Thomson must be selected
solver.add(Implies(selected["Schmidt"], And(selected["Paine"], selected["Thomson"])))

# Constraint 4: If Wong is selected, both Myers and Yoder must be selected
solver.add(Implies(selected["Wong"], And(selected["Myers"], selected["Yoder"])))

# Evaluate each option to see if the pair CANNOT be selected together
found_options = []

# Option A: Myers and Thomson
solver.push()
solver.add(And(selected["Myers"], selected["Thomson"]))
result_A = solver.check()
solver.pop()

# Option B: Ortega and Yoder
solver.push()
solver.add(And(selected["Ortega"], selected["Yoder"]))
result_B = solver.check()
solver.pop()

# Option C: Paine and Zayre
solver.push()
solver.add(And(selected["Paine"], selected["Zayre"]))
result_C = solver.check()
solver.pop()

# Option D: Schmidt and Wong
solver.push()
solver.add(And(selected["Schmidt"], selected["Wong"]))
result_D = solver.check()
solver.pop()

# Option E: Wong and Yoder
solver.push()
solver.add(And(selected["Wong"], selected["Yoder"]))
result_E = solver.check()
solver.pop()

# Determine which option is unsatisfiable (cannot be selected together)
unsat_options = []
if result_A == unsat:
    unsat_options.append("A")
if result_B == unsat:
    unsat_options.append("B")
if result_C == unsat:
    unsat_options.append("C")
if result_D == unsat:
    unsat_options.append("D")
if result_E == unsat:
    unsat_options.append("E")

# The correct answer is the only unsatisfiable option
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options are unsatisfiable {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options are unsatisfiable (all pairs can be selected together)")