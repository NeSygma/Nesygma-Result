from z3 import *

# Define workers
workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']

# Base constraints solver
solver = Solver()

# Selected workers: boolean variables
selected = {w: Bool(f'selected_{w}') for w in workers}

# Leader: one of the selected workers
leader = String('leader')
solver.add(Or([leader == w for w in workers]))

# Exactly 3 workers are selected
solver.add(Sum([If(selected[w], 1, 0) for w in workers]) == 3)

# Exactly one leader, who must be selected
solver.add(Or([And(leader == w, selected[w]) for w in workers]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(selected['Quinn'], leader == 'Quinn'))
solver.add(Implies(selected['Ruiz'], leader == 'Ruiz'))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(selected['Smith'], selected['Taylor']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(selected['Wells'], And(Not(selected['Ruiz']), Not(selected['Verma']))))

# Now evaluate each option to see which one uniquely determines the selection
options = [
    ("A", And(Not(selected['Quinn']), Not(selected['Smith']))),
    ("B", And(Not(selected['Quinn']), Not(selected['Taylor']))),
    ("C", And(Not(selected['Quinn']), Not(selected['Xue']))),
    ("D", And(Not(selected['Ruiz']), Not(selected['Wells']))),
    ("E", And(Not(selected['Ruiz']), Not(selected['Verma'])))
]

unique_options = []

for letter, constr in options:
    solver.push()
    solver.add(constr)
    
    # Check if there is at least one solution
    if solver.check() == sat:
        model = solver.model()
        
        # Block the current solution to check for uniqueness
        block = []
        for w in workers:
            if is_true(model[selected[w]]):
                block.append(selected[w] == False)
            else:
                block.append(selected[w] == True)
        if model[leader] == workers[0]:
            block.append(leader != workers[0])
        elif model[leader] == workers[1]:
            block.append(leader != workers[1])
        elif model[leader] == workers[2]:
            block.append(leader != workers[2])
        elif model[leader] == workers[3]:
            block.append(leader != workers[3])
        elif model[leader] == workers[4]:
            block.append(leader != workers[4])
        elif model[leader] == workers[5]:
            block.append(leader != workers[5])
        elif model[leader] == workers[6]:
            block.append(leader != workers[6])
        
        solver.add(Or(block))
        
        # Check if another solution exists
        if solver.check() != sat:
            unique_options.append(letter)
    
    solver.pop()

if len(unique_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unique_options[0]}")
elif len(unique_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {unique_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")