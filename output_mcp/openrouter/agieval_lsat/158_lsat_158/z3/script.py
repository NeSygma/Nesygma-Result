from z3 import *

# Photographers list
names = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
# Create Int vars: 0=unassigned,1=Silva,2=Thorne
vars = {n: Int(n) for n in names}
solver = Solver()
# Domain constraints
for v in vars.values():
    solver.add(Or(v == 0, v == 1, v == 2))
# Frost and Heideck together, both assigned, same ceremony
solver.add(vars['Frost'] != 0)
solver.add(vars['Heideck'] != 0)
solver.add(vars['Frost'] == vars['Heideck'])
# If Lai and Mays both assigned, different ceremonies
solver.add(Or(vars['Lai'] == 0, vars['Mays'] == 0, vars['Lai'] != vars['Mays']))
# If Gonzalez assigned to Silva then Lai to Thorne
solver.add(Implies(vars['Gonzalez'] == 1, vars['Lai'] == 2))
# If Knutson not Thorne then Heideck and Mays must be Thorne
solver.add(Implies(vars['Knutson'] != 2, And(vars['Heideck'] == 2, vars['Mays'] == 2)))
# At least two per ceremony
silva_count = Sum([If(v == 1, 1, 0) for v in vars.values()])
thorne_count = Sum([If(v == 2, 1, 0) for v in vars.values()])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Determine forced photographers: those that cannot be 0 in any model
forced = []
for name in names:
    s = Solver()
    s.add(solver.assertions())
    s.add(vars[name] == 0)
    if s.check() == unsat:
        forced.append(name)

# Map forced set to option letters
options = {
    'A': ['Frost', 'Heideck'],
    'B': ['Frost', 'Heideck', 'Knutson'],
    'C': ['Frost', 'Heideck', 'Knutson', 'Lai'],
    'D': ['Frost', 'Gonzalez', 'Heideck'],
    'E': ['Frost', 'Gonzalez', 'Heideck', 'Mays']
}
found = []
for letter, lst in options.items():
    if set(lst) == set(forced):
        found.append(letter)

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")