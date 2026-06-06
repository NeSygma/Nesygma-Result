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

# Evaluate each option to see if the pair can be selected together
found_options = []

# Option A: Myers and Thomson
solver.push()
solver.add(And(selected["Myers"], selected["Thomson"]))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Ortega and Yoder
solver.push()
solver.add(And(selected["Ortega"], selected["Yoder"]))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Paine and Zayre
solver.push()
solver.add(And(selected["Paine"], selected["Zayre"]))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Schmidt and Wong
solver.push()
solver.add(And(selected["Schmidt"], selected["Wong"]))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Wong and Yoder
solver.push()
solver.add(And(selected["Wong"], selected["Yoder"]))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")