from z3 import *

solver = Solver()

workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']

# Decision variables
member = {w: Bool(f'member_{w}') for w in workers}
leader = {w: Bool(f'leader_{w}') for w in workers}

# Exactly 3 members
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)

# Leader must be a member
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(member['Quinn'], leader['Quinn']))
solver.add(Implies(member['Ruiz'], leader['Ruiz']))

# If Smith is a project member, Taylor must also be
solver.add(Implies(member['Smith'], member['Taylor']))

# If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(member['Wells'], And(Not(member['Ruiz']), Not(member['Verma']))))

# Now evaluate each option
# We want Verma to be the leader

options = {
    'A': And(Not(member['Quinn']), Not(member['Smith'])),
    'B': And(Not(member['Ruiz']), Not(member['Taylor'])),
    'C': And(Not(member['Smith']), Not(member['Taylor'])),
    'D': And(Not(member['Smith']), Not(member['Xue'])),
    'E': And(Not(member['Taylor']), Not(member['Wells']))
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    solver.add(leader['Verma'])  # We want Verma to be the leader
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