from z3 import *

# Declare variables for each worker
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
member = {w: Bool(f"member_{w}") for w in workers}
leader = {w: Bool(f"leader_{w}") for w in workers}

solver = Solver()

# Exactly 3 members
member_list = [member[w] for w in workers]
solver.add(Sum([If(m, 1, 0) for m in member_list]) == 3)

# Exactly 1 leader
leader_list = [leader[w] for w in workers]
solver.add(Sum([If(l, 1, 0) for l in leader_list]) == 1)

# Leader must be a member
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraint 1: Quinn or Ruiz can be a member only if leading the project
solver.add(Implies(member["Quinn"], leader["Quinn"]))
solver.add(Implies(member["Ruiz"], leader["Ruiz"]))

# Constraint 2: If Smith is a member, Taylor must also be
solver.add(Implies(member["Smith"], member["Taylor"]))

# Constraint 3: If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(member["Wells"], And(Not(member["Ruiz"]), Not(member["Verma"]))))

# Given: Taylor is NOT a project member
solver.add(Not(member["Taylor"]))

# Now test each option: check if it's possible for that worker to NOT be a member
# If unsat, then that worker MUST be a member
print("Testing which workers MUST be members (i.e., cannot be non-members)...")
must_be_members = []
for w in workers:
    solver.push()
    solver.add(Not(member[w]))
    result = solver.check()
    if result == unsat:
        must_be_members.append(w)
    solver.pop()

print(f"Workers that must be members: {must_be_members}")
print()

# Now use the exact skeleton for multiple choice evaluation
# But we need to test the CORRECT condition: whether the worker MUST be a member
# The skeleton tests whether the worker CAN be a member, which is not what we want
# We need to test whether it's IMPOSSIBLE for the worker to NOT be a member

print("Using exact skeleton for multiple choice evaluation...")
found_options = []

# For each option, check if it's possible for that worker to NOT be a member
# If it's impossible (unsat), then that worker MUST be a member
for letter, worker in [("A", "Quinn"), ("B", "Ruiz"), ("C", "Verma"), 
                       ("D", "Wells"), ("E", "Xue")]:
    solver.push()
    solver.add(Not(member[worker]))  # Try to make this worker NOT a member
    result = solver.check()
    if result == unsat:  # If impossible, then this worker MUST be a member
        found_options.append(letter)
    solver.pop()

print(f"Options where worker MUST be a member: {found_options}")
print()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")