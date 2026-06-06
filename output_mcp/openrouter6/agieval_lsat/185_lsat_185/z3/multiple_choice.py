from z3 import *

# Define indices for workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
idx = {name: i for i, name in enumerate(workers)}

# Boolean variables: member[i] = True if worker i is a project member
# leader[i] = True if worker i is the project leader
member = [Bool(f'member_{i}') for i in range(7)]
leader = [Bool(f'leader_{i}') for i in range(7)]

solver = Solver()

# Base constraints:
# 1. Exactly three members
solver.add(Sum([If(m, 1, 0) for m in member]) == 3)
# 2. Exactly one leader
solver.add(Sum([If(l, 1, 0) for l in leader]) == 1)
# 3. Leader must be a member
for i in range(7):
    solver.add(Implies(leader[i], member[i]))
# 4. Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(member[idx["Quinn"]], leader[idx["Quinn"]]))
solver.add(Implies(member[idx["Ruiz"]], leader[idx["Ruiz"]]))
# 5. If Smith is a project member, Taylor must also be
solver.add(Implies(member[idx["Smith"]], member[idx["Taylor"]]))
# 6. If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(member[idx["Wells"]], And(Not(member[idx["Ruiz"]]), Not(member[idx["Verma"]]))))

# Helper function to generate constraints for a given option
def option_constraints(leader_name, member_names):
    """Return a list of constraints that enforce the given selection."""
    constraints = []
    leader_idx = idx[leader_name]
    member_indices = [idx[name] for name in member_names]
    # Ensure exactly these three are members and the leader is among them
    for i in range(7):
        if i == leader_idx:
            constraints.append(leader[i] == True)
            constraints.append(member[i] == True)
        elif i in member_indices:
            constraints.append(member[i] == True)
            constraints.append(leader[i] == False)
        else:
            constraints.append(member[i] == False)
            constraints.append(leader[i] == False)
    return constraints

# Define each option as (letter, leader_name, member_names)
options = [
    ("A", "Ruiz", ["Taylor", "Wells"]),
    ("B", "Verma", ["Quinn", "Taylor"]),
    ("C", "Verma", ["Smith", "Taylor"]),
    ("D", "Verma", ["Smith", "Xue"]),
    ("E", "Xue", ["Verma", "Wells"])
]

found_options = []
for letter, leader_name, member_names in options:
    constr = option_constraints(leader_name, member_names)
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