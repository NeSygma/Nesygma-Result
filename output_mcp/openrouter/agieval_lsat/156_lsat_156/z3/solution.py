from z3 import *

# Define constants for locations
S, T, N = 0, 1, 2

# Photographers
photogs = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
vars = {p: Int(p) for p in photogs}
solver = Solver()

# Domain constraints
for v in vars.values():
    solver.add(Or(v == S, v == T, v == N))

# Base constraints
# At least two assigned to each ceremony
cnt_S = Sum([If(v == S, 1, 0) for v in vars.values()])
cnt_T = Sum([If(v == T, 1, 0) for v in vars.values()])
solver.add(cnt_S >= 2)
solver.add(cnt_T >= 2)

# Frost must be assigned together with Heideck to one ceremony (both assigned, same)
solver.add(vars['Frost'] == vars['Heideck'])
solver.add(vars['Frost'] != N)  # both assigned

# If Lai and Mays both assigned, they must be to different ceremonies
solver.add(Implies(And(vars['Lai'] != N, vars['Mays'] != N), vars['Lai'] != vars['Mays']))

# If Gonzalez assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(vars['Gonzalez'] == S, vars['Lai'] == T))

# If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(vars['Knutson'] != T, And(vars['Heideck'] == T, vars['Mays'] == T)))

# Assumption: Heideck is assigned to the same ceremony as Lai (and they are assigned)
solver.add(vars['Heideck'] == vars['Lai'])
solver.add(vars['Heideck'] != N)

# Define option constraints
opt_a = vars['Frost'] == T
opt_b = vars['Gonzalez'] == S
opt_c = vars['Gonzalez'] == N
opt_d = vars['Knutson'] == T
opt_e = vars['Lai'] == T

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
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