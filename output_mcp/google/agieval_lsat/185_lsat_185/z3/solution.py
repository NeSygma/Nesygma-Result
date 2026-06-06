from z3 import *

# Workers
workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']

# Variables
member = {w: Bool(f'member_{w}') for w in workers}
leader = {w: Bool(f'leader_{w}') for w in workers}

solver = Solver()

# Exactly 3 members
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)

# Leader must be a member
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(member['Quinn'], leader['Quinn']))
solver.add(Implies(member['Ruiz'], leader['Ruiz']))

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(member['Smith'], member['Taylor']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member['Wells'], And(Not(member['Ruiz']), Not(member['Verma']))))

# Define options
options = {
    "A": (['Ruiz', 'Taylor', 'Wells'], 'Ruiz'),
    "B": (['Verma', 'Quinn', 'Taylor'], 'Verma'),
    "C": (['Verma', 'Smith', 'Taylor'], 'Verma'),
    "D": (['Verma', 'Smith', 'Xue'], 'Verma'),
    "E": (['Xue', 'Verma', 'Wells'], 'Xue')
}

found_options = []
for label, (members, lead) in options.items():
    solver.push()
    # Add constraints for this specific selection
    for w in workers:
        if w in members:
            solver.add(member[w])
        else:
            solver.add(Not(member[w]))
        
        if w == lead:
            solver.add(leader[w])
        else:
            solver.add(Not(leader[w]))
            
    if solver.check() == sat:
        found_options.append(label)
    solver.pop()

print(f"STATUS: sat")
print(f"Valid options: {found_options}")