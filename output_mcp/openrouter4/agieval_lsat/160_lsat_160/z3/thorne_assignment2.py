from z3 import *

# Photographers: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
N = 6
assign = [Int(f"assign_{i}") for i in range(N)]

solver = Solver()

# Domain: 0=Silva, 1=Thorne, 2=Unassigned
for i in range(N):
    solver.add(And(assign[i] >= 0, assign[i] <= 2))

# Base constraints

# 1. Frost and Heideck must be assigned together to one of the ceremonies
solver.add(assign[0] == assign[2])  # Frost and Heideck assigned together
solver.add(assign[0] != 2)          # They must be assigned (not unassigned)

# 2. If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(And(assign[4] != 2, assign[5] != 2), assign[4] != assign[5]))

# 3. If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign[1] == 0, assign[4] == 1))

# 4. If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(assign[3] != 1, And(assign[2] == 1, assign[5] == 1)))

# 5. At least two photographers at each ceremony
solver.add(Sum([If(assign[i] == 0, 1, 0) for i in range(N)]) >= 2)
solver.add(Sum([If(assign[i] == 1, 1, 0) for i in range(N)]) >= 2)

# Options
names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
name_to_idx = {name: i for i, name in enumerate(names)}

options = {
    "A": ["Frost", "Gonzalez", "Heideck", "Mays"],
    "B": ["Frost", "Heideck", "Knutson", "Mays"],
    "C": ["Gonzalez", "Knutson", "Lai"],
    "D": ["Gonzalez", "Knutson", "Mays"],
    "E": ["Knutson", "Mays"]
}

# Find which option is UNSAT (cannot be the complete assignment)
cannot_be = []

for letter, opt_list in options.items():
    solver.push()
    opt_indices = [name_to_idx[name] for name in opt_list]
    for idx in opt_indices:
        solver.add(assign[idx] == 1)
    for i in range(N):
        if i not in opt_indices:
            solver.add(assign[i] != 1)
    result = solver.check()
    if result == unsat:
        cannot_be.append(letter)
    solver.pop()

if len(cannot_be) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be[0]}")
elif len(cannot_be) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be {cannot_be}")
else:
    print("STATUS: unsat")
    print("Refine: No option found that cannot be")