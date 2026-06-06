from z3 import *

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
# 0: Unassigned, 1: Silva, 2: Thorne
assign = {p: Int(p) for p in photographers}

solver = Solver()

# Domain constraints
for p in photographers:
    solver.add(assign[p] >= 0, assign[p] <= 2)

# 1. Each ceremony has at least 2 photographers
# Count in Silva (1)
count_s = Sum([If(assign[p] == 1, 1, 0) for p in photographers])
# Count in Thorne (2)
count_t = Sum([If(assign[p] == 2, 1, 0) for p in photographers])
solver.add(count_s >= 2)
solver.add(count_t >= 2)

# 2. Frost must be assigned together with Heideck to one of the graduation ceremonies
solver.add(assign['Frost'] == assign['Heideck'])
solver.add(Or(assign['Frost'] == 1, assign['Frost'] == 2))

# 3. If Lai and Mays are both assigned, they must be in different ceremonies
solver.add(Implies(And(assign['Lai'] != 0, assign['Mays'] != 0), assign['Lai'] != assign['Mays']))

# 4. If Gonzalez is assigned to the Silva University ceremony, then Lai must be assigned to the Thorne University ceremony
solver.add(Implies(assign['Gonzalez'] == 1, assign['Lai'] == 2))

# 5. If Knutson is not assigned to the Thorne University ceremony, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign['Knutson'] != 2, And(assign['Heideck'] == 2, assign['Mays'] == 2)))

# Define options
options = {
    "A": {"Silva": ["Gonzalez", "Lai"], "Thorne": ["Frost", "Heideck", "Mays"]},
    "B": {"Silva": ["Gonzalez", "Mays"], "Thorne": ["Knutson", "Lai"]},
    "C": {"Silva": ["Frost", "Gonzalez", "Heideck"], "Thorne": ["Knutson", "Lai", "Mays"]},
    "D": {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Lai"]},
    "E": {"Silva": ["Frost", "Heideck", "Mays"], "Thorne": ["Gonzalez", "Knutson", "Lai"]}
}

def check_option(opt_name):
    opt = options[opt_name]
    solver.push()
    # Set assignments based on option
    for p in photographers:
        if p in opt["Silva"]:
            solver.add(assign[p] == 1)
        elif p in opt["Thorne"]:
            solver.add(assign[p] == 2)
        else:
            solver.add(assign[p] == 0)
    
    res = solver.check()
    solver.pop()
    return res == sat

found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    if check_option(letter):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")