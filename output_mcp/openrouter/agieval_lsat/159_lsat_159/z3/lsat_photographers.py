from z3 import *

# Create solver and base constraints
solver = Solver()

# Photographers variables: 0=unassigned, 1=Silva, 2=Thorne
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
vars = {name: Int(name) for name in photographers}

# Domain constraints
for v in vars.values():
    solver.add(v >= 0, v <= 2)

# Exactly four photographers assigned (non-zero)
assigned_cnt = Sum([If(v != 0, 1, 0) for v in vars.values()])
solver.add(assigned_cnt == 4)

# At least two per ceremony
silva_cnt = Sum([If(v == 1, 1, 0) for v in vars.values()])
thorne_cnt = Sum([If(v == 2, 1, 0) for v in vars.values()])
solver.add(silva_cnt >= 2)
solver.add(thorne_cnt >= 2)

# Frost and Heideck together at same ceremony, both assigned
solver.add(vars['Frost'] == vars['Heideck'])
solver.add(vars['Frost'] != 0)

# If Lai and Mays both assigned, they must be at different ceremonies
solver.add(Implies(And(vars['Lai'] != 0, vars['Mays'] != 0), vars['Lai'] != vars['Mays']))

# If Gonzalez assigned to Silva, then Lai assigned to Thorne
solver.add(Implies(vars['Gonzalez'] == 1, vars['Lai'] == 2))

# If Knutson not assigned to Thorne, then Heideck and Mays must be assigned to Thorne
solver.add(Implies(vars['Knutson'] != 2, And(vars['Heideck'] == 2, vars['Mays'] == 2)))

# Define option constraints
option_constraints = {
    "A": vars['Frost'] == 1,
    "B": vars['Gonzalez'] == 1,
    "C": vars['Knutson'] == 1,
    "D": vars['Lai'] == 1,
    "E": vars['Mays'] == 1,
}

found_options = []
for letter, opt_constr in [("A", option_constraints["A"]),
                         ("B", option_constraints["B"]),
                         ("C", option_constraints["C"]),
                         ("D", option_constraints["D"]),
                         ("E", option_constraints["E"])]:
    solver.push()
    solver.add(opt_constr)
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