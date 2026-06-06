from z3 import *

solver = Solver()

# Define candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
assign = [Int(f'assign_{i}') for i in range(5)]

# Each assignment is -1 (not assigned) or 0,1,2 (Venezuela, Yemen, Zambia)
for i in range(5):
    solver.add(Or(assign[i] == -1, assign[i] == 0, assign[i] == 1, assign[i] == 2))

# Exactly three candidates are assigned
solver.add(Sum([If(assign[i] != -1, 1, 0) for i in range(5)]) == 3)

# Each country has exactly one candidate
for c in range(3):
    solver.add(Sum([If(assign[i] == c, 1, 0) for i in range(5)]) == 1)

# Constraint 1: Exactly one of Kayne (1) and Novetzke (3) is assigned
solver.add((assign[1] != -1) + (assign[3] != -1) == 1)

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(assign[0] != -1, assign[1] != -1))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assign[4] == 0, assign[1] != 1))

# Constraint 4: If Landon is assigned, then he is assigned to Zambia
solver.add(Implies(assign[2] != -1, assign[2] == 2))

# Define options as constraints that would make the statement true
opt_a = (assign[0] == 2)   # Jaramillo to Zambia
opt_b = (assign[1] == 2)   # Kayne to Zambia
opt_c = (assign[3] == 2)   # Novetzke to Zambia
opt_d = (assign[2] == -1)  # Landon not assigned
opt_e = (assign[4] == -1)  # Ong not assigned

# Evaluate each option: we want to find which one CANNOT be true.
# So we check if adding the option makes the problem unsatisfiable.
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:   # Option cannot be true
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