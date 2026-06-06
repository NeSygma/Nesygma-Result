from z3 import *

# Define workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
member = {w: Bool(f"member_{w}") for w in workers}
leader = {w: Bool(f"leader_{w}") for w in workers}

solver = Solver()

# Base constraints:
# Exactly three members
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)
# Exactly one leader
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
# Leader must be a member
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(member["Quinn"], leader["Quinn"]))
solver.add(Implies(member["Ruiz"], leader["Ruiz"]))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(member["Smith"], member["Taylor"]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(member["Wells"], And(Not(member["Ruiz"]), Not(member["Verma"]))))

# Condition: Taylor is not a project member
solver.add(Not(member["Taylor"]))

# Now evaluate each option using the skeleton
# We want to find which worker must be a member.
# We'll test the negation of each option: if assuming the worker is NOT a member leads to unsat, then that worker must be a member.
# So we define opt_a_constr as Not(member["Quinn"]), etc.
# Then we check if the solver is unsat for that option.

found_options = []
options = [
    ("A", Not(member["Quinn"])),
    ("B", Not(member["Ruiz"])),
    ("C", Not(member["Verma"])),
    ("D", Not(member["Wells"])),
    ("E", Not(member["Xue"]))
]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    # We check for unsat because if assuming the worker is NOT a member leads to unsat,
    # then the worker must be a member.
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

# According to the skeleton, we should have exactly one found option.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")