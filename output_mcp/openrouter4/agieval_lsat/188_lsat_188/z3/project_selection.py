from z3 import *

solver = Solver()

workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']

# Boolean variables for membership and leadership
member = {w: Bool(f'member_{w}') for w in workers}
leader = {w: Bool(f'leader_{w}') for w in workers}

# Exactly 3 members
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)

# If a worker is leader, they must be a member
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(member['Quinn'], leader['Quinn']))
solver.add(Implies(member['Ruiz'], leader['Ruiz']))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(member['Smith'], member['Taylor']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(member['Wells'], And(Not(member['Ruiz']), Not(member['Verma']))))

# Given condition: Taylor is not a project member
solver.add(Not(member['Taylor']))

# Now test each option: which worker MUST be a member?
# We test by trying to make that worker NOT a member; if unsat, then they must be a member.
found_options = []
for letter, w in [('A', 'Quinn'), ('B', 'Ruiz'), ('C', 'Verma'), ('D', 'Wells'), ('E', 'Xue')]:
    solver.push()
    solver.add(Not(member[w]))
    if solver.check() == unsat:
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