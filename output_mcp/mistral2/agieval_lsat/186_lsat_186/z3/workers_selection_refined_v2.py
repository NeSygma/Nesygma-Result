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
# We need to find the third member explicitly
third_member = [w for w in workers if w not in ["Taylor", "Wells"]]

# The third member must be exactly one of the remaining workers
solver.add(Sum([is_member[w] for w in third_member]) == 1)

# Now, evaluate each option to see which one matches the third member
found_options = []

# Option A: Quinn or Smith
solver.push()
solver.add(Or(is_member["Quinn"], is_member["Smith"]))
if solver.check() == sat:
    m = solver.model()
    if m[is_member["Quinn"]] or m[is_member["Smith"]]:
        # Ensure only one of them is the third member
        if m[is_member["Quinn"]] and not m[is_member["Smith"]]:
            found_options.append("A")
        elif m[is_member["Smith"]] and not m[is_member["Quinn"]]:
            found_options.append("A")
solver.pop()

# Option B: Quinn or Xue
solver.push()
solver.add(Or(is_member["Quinn"], is_member["Xue"]))
if solver.check() == sat:
    m = solver.model()
    if m[is_member["Quinn"]] and not m[is_member["Xue"]]:
        found_options.append("B")
    elif m[is_member["Xue"]] and not m[is_member["Quinn"]]:
        found_options.append("B")
solver.pop()

# Option C: Ruiz or Verma
solver.push()
solver.add(Or(is_member["Ruiz"], is_member["Verma"]))
if solver.check() == sat:
    m = solver.model()
    if m[is_member["Ruiz"]] and not m[is_member["Verma"]]:
        found_options.append("C")
    elif m[is_member["Verma"]] and not m[is_member["Ruiz"]]:
        found_options.append("C")
solver.pop()

# Option D: Smith or Xue
solver.push()
solver.add(Or(is_member["Smith"], is_member["Xue"]))
if solver.check() == sat:
    m = solver.model()
    if m[is_member["Smith"]] and not m[is_member["Xue"]]:
        found_options.append("D")
    elif m[is_member["Xue"]] and not m[is_member["Smith"]]:
        found_options.append("D")
solver.pop()

# Option E: Verma or Xue
solver.push()
solver.add(Or(is_member["Verma"], is_member["Xue"]))
if solver.check() == sat:
    m = solver.model()
    if m[is_member["Verma"]] and not m[is_member["Xue"]]:
        found_options.append("E")
    elif m[is_member["Xue"]] and not m[is_member["Verma"]]:
        found_options.append("E")
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