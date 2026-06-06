from z3 import *

# Declare workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]

# Create Bool variables for membership and leadership
is_member = {w: Bool(f"is_member_{w}") for w in workers}
is_leader = {w: Bool(f"is_leader_{w}") for w in workers}

# Create solver
solver = Solver()

# Base constraints
# Exactly 3 workers are project members
solver.add(Sum([is_member[w] for w in workers]) == 3)

# Exactly 1 project leader
solver.add(Sum([is_leader[w] for w in workers]) == 1)

# Quinn or Ruiz can be a project member only if they are the project leader
for w in ["Quinn", "Ruiz"]:
    solver.add(Implies(is_member[w], is_leader[w]))

# If Smith is a project member, Taylor must also be
solver.add(Implies(is_member["Smith"], is_member["Taylor"]))

# If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(is_member["Wells"], And(Not(is_member["Ruiz"]), Not(is_member["Verma"]))))

# Given: Taylor is the project leader and Wells is a project member
solver.add(is_leader["Taylor"])
solver.add(is_member["Wells"])

# The third member is the one in the member set excluding Taylor (leader) and Wells (member)
# We need to ensure that only one of the options is valid for the third member

# Define the options as constraints on the third member
# Option A: Quinn or Smith
opt_a_constr = And(
    Or(is_member["Quinn"], is_member["Smith"]),
    Not(Or(is_member["Xue"], is_member["Verma"]))
)

# Option B: Quinn or Xue
opt_b_constr = And(
    Or(is_member["Quinn"], is_member["Xue"]),
    Not(Or(is_member["Smith"], is_member["Verma"]))
)

# Option C: Ruiz or Verma
opt_c_constr = And(
    Or(is_member["Ruiz"], is_member["Verma"]),
    Not(Or(is_member["Quinn"], is_member["Smith"], is_member["Xue"]))
)

# Option D: Smith or Xue
opt_d_constr = And(
    Or(is_member["Smith"], is_member["Xue"]),
    Not(Or(is_member["Quinn"], is_member["Verma"]))
)

# Option E: Verma or Xue
opt_e_constr = And(
    Or(is_member["Verma"], is_member["Xue"]),
    Not(Or(is_member["Quinn"], is_member["Smith"]))
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