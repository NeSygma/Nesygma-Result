from z3 import *

# Base constraints solver
solver = Solver()

# Workers
workers = ['quinn', 'ruiz', 'smith', 'taylor', 'verma', 'wells', 'xue']
selected = {w: Bool(f'selected_{w}') for w in workers}
leader = String('leader')

# Exactly 3 workers are selected
solver.add(Sum([selected[w] for w in workers]) == 3)

# Leader is one of the selected workers
solver.add(Or([And(selected[w], leader == w) for w in workers]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(selected['quinn'], leader == 'quinn'))
solver.add(Implies(selected['ruiz'], leader == 'ruiz'))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(selected['smith'], selected['taylor']))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(selected['wells'], And(Not(selected['ruiz']), Not(selected['verma']))))

# Additional constraint: leader must be one of the selected workers (already covered above)

# Now evaluate each option to see if Verma can be the leader under that condition
found_options = []

# Option A: Neither Quinn nor Smith is selected
solver.push()
solver.add(Not(selected['quinn']))
solver.add(Not(selected['smith']))
solver.add(leader == 'verma')
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Neither Ruiz nor Taylor is selected
solver.push()
solver.add(Not(selected['ruiz']))
solver.add(Not(selected['taylor']))
solver.add(leader == 'verma')
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Neither Smith nor Taylor is selected
solver.push()
solver.add(Not(selected['smith']))
solver.add(Not(selected['taylor']))
solver.add(leader == 'verma')
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Neither Smith nor Xue is selected
solver.push()
solver.add(Not(selected['smith']))
solver.add(Not(selected['xue']))
solver.add(leader == 'verma')
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Neither Taylor nor Wells is selected
solver.push()
solver.add(Not(selected['taylor']))
solver.add(Not(selected['wells']))
solver.add(leader == 'verma')
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")