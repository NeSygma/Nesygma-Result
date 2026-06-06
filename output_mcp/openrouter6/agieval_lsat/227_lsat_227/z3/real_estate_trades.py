from z3 import *

# Define buildings: (name, class, value)
buildings = [
    ("Garza", 1, 4),
    ("Yates", 3, 1),
    ("Zimmer", 3, 1),
    ("Flores", 1, 4),
    ("Lynch", 2, 2),
    ("King", 2, 2),
    ("Meyer", 2, 2),
    ("Ortiz", 2, 2)
]

# Map building name to index
index = {name: i for i, (name, _, _) in enumerate(buildings)}

# Owner variables: 0=RealProp, 1=Southco, 2=Trustcorp
owner = [Int(f"owner_{i}") for i in range(8)]

# Values list
values = [b[2] for b in buildings]

solver = Solver()

# Base constraints: each owner in {0,1,2}
for i in range(8):
    solver.add(owner[i] >= 0)
    solver.add(owner[i] <= 2)

# Value constraint: each company's total value = 6
for c in range(3):
    total_value = Sum([If(owner[i] == c, values[i], 0) for i in range(8)])
    solver.add(total_value == 6)

# Define options
options = [
    ("A", [ ("Flores", 0), ("Garza", 0) ]),  # RealProp owns Flores and Garza
    ("B", [ ("Flores", 1), ("Meyer", 1) ]),  # Southco owns Flores and Meyer
    ("C", [ ("Garza", 1), ("Lynch", 1) ]),  # Southco owns Garza and Lynch
    ("D", [ ("Flores", 2), ("Ortiz", 2) ]),  # Trustcorp owns Flores and Ortiz
    ("E", [ ("Garza", 2), ("Meyer", 2) ])   # Trustcorp owns Garza and Meyer
]

unsat_options = []

for letter, assignments in options:
    solver.push()
    for building_name, company in assignments:
        i = index[building_name]
        solver.add(owner[i] == company)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found unsat {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found unsat")