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
# i.e., if member[Quinn] then leader[Quinn]; if member[Ruiz] then leader[Ruiz]
solver.add(Implies(member["Quinn"], leader["Quinn"]))
solver.add(Implies(member["Ruiz"], leader["Ruiz"]))

# Constraint 2: If Smith is a member, Taylor must also be
solver.add(Implies(member["Smith"], member["Taylor"]))

# Constraint 3: If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(member["Wells"], And(Not(member["Ruiz"]), Not(member["Verma"]))))

# Given: Taylor is NOT a project member
solver.add(Not(member["Taylor"]))

# Now we need to find which worker MUST be a member
# We'll test each option by checking if it's possible for that worker to NOT be a member
# If it's impossible (unsat), then that worker MUST be a member

print("Testing which workers must be members given Taylor is not a member...")
print()

must_be_members = []
for w in workers:
    solver.push()
    solver.add(Not(member[w]))  # Try to make this worker NOT a member
    result = solver.check()
    if result == unsat:
        must_be_members.append(w)
    solver.pop()

print(f"Workers that must be members: {must_be_members}")
print()

# Now test the multiple choice options
print("Testing multiple choice options...")
found_options = []

# Option A: Quinn must be a member
solver.push()
solver.add(member["Quinn"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Ruiz must be a member
solver.push()
solver.add(member["Ruiz"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Verma must be a member
solver.push()
solver.add(member["Verma"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Wells must be a member
solver.push()
solver.add(member["Wells"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Xue must be a member
solver.push()
solver.add(member["Xue"])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Options that can be members: {found_options}")
print()

# According to the problem, we need to find which one MUST be a member
# Let's check which of the must_be_members are in the answer choices
answer_choices = {"A": "Quinn", "B": "Ruiz", "C": "Verma", "D": "Wells", "E": "Xue"}
correct_options = []
for letter, worker in answer_choices.items():
    if worker in must_be_members:
        correct_options.append(letter)

print(f"Correct options (workers that must be members): {correct_options}")
print()

# Now use the exact skeleton for multiple choice evaluation
print("Using exact skeleton for multiple choice evaluation...")
found_options = []
for letter, constr in [("A", member["Quinn"]), ("B", member["Ruiz"]), ("C", member["Verma"]), 
                      ("D", member["Wells"]), ("E", member["Xue"])]:
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