from z3 import *

photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
assign = {p: Int(p) for p in photographers}

solver = Solver()

for p in photographers:
    solver.add(assign[p] >= 0, assign[p] <= 2)

# 1. Frost and Heideck must be assigned together to one of the graduation ceremonies.
# They must be assigned (not unassigned).
solver.add(assign['Frost'] == assign['Heideck'])
solver.add(assign['Frost'] != 0)

# 2. If Lai and Mays are both assigned, they must be in different ceremonies
solver.add(Implies(And(assign['Lai'] != 0, assign['Mays'] != 0), assign['Lai'] != assign['Mays']))

# 3. If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# 4. If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# 5. At least two photographers in each ceremony
solver.add(Sum([If(assign[p] == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(assign[p] == 2, 1, 0) for p in photographers]) >= 2)

# Define options
# A: Frost, Gonzalez, Heideck, Knutson in Silva
# B: Frost, Gonzalez, Heideck in Silva
# C: Gonzalez, Knutson in Silva
# D: Heideck, Lai in Silva
# E: Knutson, Mays in Silva

options = {
    "A": ['Frost', 'Gonzalez', 'Heideck', 'Knutson'],
    "B": ['Frost', 'Gonzalez', 'Heideck'],
    "C": ['Gonzalez', 'Knutson'],
    "D": ['Heideck', 'Lai'],
    "E": ['Knutson', 'Mays']
}

found_options = []
for letter, silva_list in options.items():
    solver.push()
    # Photographers in the list MUST be in Silva (1)
    for p in silva_list:
        solver.add(assign[p] == 1)
    # Photographers NOT in the list MUST NOT be in Silva (they can be 0 or 2)
    for p in photographers:
        if p not in silva_list:
            solver.add(assign[p] != 1)
    
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"STATUS: sat")
print(f"answer:{found_options[0]}")