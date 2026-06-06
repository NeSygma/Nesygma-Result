from z3 import *

# Photographers
photographers = ['F', 'G', 'H', 'K', 'L', 'M']
# 0: None, 1: Silva, 2: Thorne
assign = {p: Int(p) for p in photographers}

solver = Solver()

# Domain constraints
for p in photographers:
    solver.add(assign[p] >= 0, assign[p] <= 2)

# Constraint 1: At least two photographers at S
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)

# Constraint 2: At least two photographers at T
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 4: Frost must be assigned together with Heideck to one of the graduation ceremonies
solver.add(assign['F'] == assign['H'])
solver.add(assign['F'] != 0)

# Constraint 5: If Lai and Mays are both assigned, it must be to different ceremonies
solver.add(Implies(And(assign['L'] != 0, assign['M'] != 0), assign['L'] != assign['M']))

# Constraint 6: If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony
solver.add(Implies(assign['G'] == 1, assign['L'] == 2))

# Constraint 7: If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign['K'] != 2, And(assign['H'] == 2, assign['M'] == 2)))

# Question condition: Heideck is assigned to the same graduation ceremony as Lai
# (Implies they are both assigned to S or both assigned to T)
solver.push()
solver.add(assign['H'] == assign['L'])
solver.add(assign['H'] != 0)

# Answer Choices
# (A) Frost is assigned to the Thorne University ceremony.
# (B) Gonzalez is assigned to the Silva University ceremony.
# (C) Gonzalez is assigned to neither graduation ceremony.
# (D) Knutson is assigned to the Thorne University ceremony.
# (E) Lai is assigned to the Thorne University ceremony.

options = [
    ("A", assign['F'] == 2),
    ("B", assign['G'] == 1),
    ("C", assign['G'] == 0),
    ("D", assign['K'] == 2),
    ("E", assign['L'] == 2)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

print(f"STATUS: sat")
print(f"Valid options: {found_options}")
solver.pop()