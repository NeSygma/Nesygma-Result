from z3 import *

# Base constraints for the problem
solver = Solver()

# Workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]

# Selection: exactly 3 workers are selected
selected = {w: Bool(f"selected_{w}") for w in workers}
solver.add(Sum([If(selected[w], 1, 0) for w in workers]) == 3)

# Exactly one project leader
leader = {w: Bool(f"leader_{w}") for w in workers}
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)

# Constraints:
# 1. Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(And(selected["Quinn"], leader["Quinn"] == False), False))
solver.add(Implies(And(selected["Ruiz"], leader["Ruiz"] == False), False))

# 2. If Smith is a project member, Taylor must also be.
solver.add(Implies(selected["Smith"], selected["Taylor"]))

# 3. If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(selected["Wells"], And(selected["Ruiz"] == False, selected["Verma"] == False)))

# Additional constraint: The leader must be one of the selected members
for w in workers:
    solver.add(Implies(leader[w], selected[w]))

# Base constraints are now set. Now evaluate each option.

# Option A: Neither Quinn nor Smith is selected.
opt_a_constr = And(selected["Quinn"] == False, selected["Smith"] == False)

# Option B: Neither Ruiz nor Taylor is selected.
opt_b_constr = And(selected["Ruiz"] == False, selected["Taylor"] == False)

# Option C: Neither Smith nor Taylor is selected.
opt_c_constr = And(selected["Smith"] == False, selected["Taylor"] == False)

# Option D: Neither Smith nor Xue is selected.
opt_d_constr = And(selected["Smith"] == False, selected["Xue"] == False)

# Option E: Neither Taylor nor Wells is selected.
opt_e_constr = And(selected["Taylor"] == False, selected["Wells"] == False)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Check if Verma can be the leader in this scenario
        solver.push()
        solver.add(leader["Verma"])
        if solver.check() == sat:
            found_options.append(letter)
        solver.pop()
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