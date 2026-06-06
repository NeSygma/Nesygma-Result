from z3 import *

# Workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]

# Create boolean variables for selection
selected = {w: Bool(f"selected_{w}") for w in workers}
# Create a variable for the leader (must be one of the selected workers)
leader = {w: Bool(f"leader_{w}") for w in workers}

solver = Solver()

# Exactly 3 workers are selected
solver.add(Sum([selected[w] for w in workers]) == 3)

# Exactly one leader
solver.add(Sum([leader[w] for w in workers]) == 1)

# Leader must be one of the selected workers
for w in workers:
    solver.add(Implies(leader[w], selected[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
for w in ["Quinn", "Ruiz"]:
    solver.add(Implies(selected[w], leader[w]))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(selected["Smith"], selected["Taylor"]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(selected["Wells"], Not(selected["Ruiz"])))
solver.add(Implies(selected["Wells"], Not(selected["Verma"])))

# Base constraints are set. Now evaluate each option.

# Option A: Ruiz (leader), Taylor, Wells
opt_a_constr = And(
    leader["Ruiz"],
    selected["Ruiz"],
    selected["Taylor"],
    selected["Wells"],
    Not(selected["Quinn"]),
    Not(selected["Smith"]),
    Not(selected["Verma"]),
    Not(selected["Xue"])
)

# Option B: Verma (leader), Quinn, Taylor
opt_b_constr = And(
    leader["Verma"],
    selected["Verma"],
    selected["Quinn"],
    selected["Taylor"],
    Not(selected["Ruiz"]),
    Not(selected["Smith"]),
    Not(selected["Wells"]),
    Not(selected["Xue"])
)

# Option C: Verma (leader), Smith, Taylor
opt_c_constr = And(
    leader["Verma"],
    selected["Verma"],
    selected["Smith"],
    selected["Taylor"],
    Not(selected["Quinn"]),
    Not(selected["Ruiz"]),
    Not(selected["Wells"]),
    Not(selected["Xue"])
)

# Option D: Verma (leader), Smith, Xue
opt_d_constr = And(
    leader["Verma"],
    selected["Verma"],
    selected["Smith"],
    selected["Xue"],
    Not(selected["Quinn"]),
    Not(selected["Ruiz"]),
    Not(selected["Taylor"]),
    Not(selected["Wells"])
)

# Option E: Xue (leader), Verma, Wells
opt_e_constr = And(
    leader["Xue"],
    selected["Xue"],
    selected["Verma"],
    selected["Wells"],
    Not(selected["Quinn"]),
    Not(selected["Ruiz"]),
    Not(selected["Smith"]),
    Not(selected["Taylor"])
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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