from z3 import *
solver = Solver()

# Declare variables
photographers = ['F', 'G', 'H', 'K', 'L', 'M']
assign = {p: Int(f'assign_{p}') for p in photographers}
# Values: 0 = unassigned, 1 = Silva, 2 = Thorne

# Base constraints
# Each photographer assigned to at most one ceremony
for p in photographers:
    solver.add(Or(assign[p] == 0, assign[p] == 1, assign[p] == 2))

# At least two photographers per ceremony
count_S = Sum([If(assign[p] == 1, 1, 0) for p in photographers])
count_T = Sum([If(assign[p] == 2, 1, 0) for p in photographers])
solver.add(count_S >= 2)
solver.add(count_T >= 2)

# Frost and Heideck together
solver.add(assign['F'] == assign['H'])
solver.add(assign['F'] != 0)

# If Lai and Mays both assigned, different ceremonies
solver.add(Implies(And(assign['L'] != 0, assign['M'] != 0), assign['L'] != assign['M']))

# If Gonzalez assigned to Silva, then Lai assigned to Thorne
solver.add(Implies(assign['G'] == 1, assign['L'] == 2))

# If Knutson not assigned to Thorne, then Heideck and Mays assigned to Thorne
solver.add(Implies(assign['K'] != 2, And(assign['H'] == 2, assign['M'] == 2)))

# Condition: Heideck and Lai same ceremony
solver.add(assign['H'] == assign['L'])
solver.add(assign['H'] != 0)  # since same ceremony, both assigned

# Now, for each option, check if the option is entailed.
# We'll check if the negation of the option is unsatisfiable.
found_options = []
for letter, opt_constr in [
    ("A", assign['F'] == 2),
    ("B", assign['G'] == 1),
    ("C", assign['G'] == 0),
    ("D", assign['K'] == 2),
    ("E", assign['L'] == 2)
]:
    solver.push()
    solver.add(Not(opt_constr))
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