from z3 import *

# Countries: Venezuela=0, Yemen=1, Zambia=2
V, Y, Z = 0, 1, 2

# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
amb = [Int(f"amb_{c}") for c in range(3)]

solver = Solver()

# Domain
for c in range(3):
    solver.add(amb[c] >= 0, amb[c] <= 4)

# All distinct
solver.add(Distinct(amb))

# Constraint 1: Exactly one of Kayne (1) or Novetzke (3) is assigned
solver.add(Sum([If(amb[c] == 1, 1, 0) for c in range(3)]) + 
           Sum([If(amb[c] == 3, 1, 0) for c in range(3)]) == 1)

# Constraint 2: If Jaramillo (0) is assigned, then Kayne (1) is assigned
solver.add(Implies(
    Sum([If(amb[c] == 0, 1, 0) for c in range(3)]) >= 1,
    Sum([If(amb[c] == 1, 1, 0) for c in range(3)]) >= 1
))

# Constraint 3: If Ong (4) is ambassador to Venezuela, Kayne (1) is not ambassador to Yemen
solver.add(Implies(amb[V] == 4, amb[Y] != 1))

# Constraint 4: If Landon (2) is assigned, it is to Zambia
solver.add(Implies(
    Sum([If(amb[c] == 2, 1, 0) for c in range(3)]) >= 1,
    amb[Z] == 2
))

# Option A: Jaramillo is assigned as ambassador to Zambia.
opt_a = (amb[Z] == 0)

# Option B: Kayne is assigned as ambassador to Zambia.
opt_b = (amb[Z] == 1)

# Option C: Novetzke is assigned as ambassador to Zambia.
opt_c = (amb[Z] == 3)

# Option D: Landon is not assigned to an ambassadorship.
opt_d = (Sum([If(amb[c] == 2, 1, 0) for c in range(3)]) == 0)

# Option E: Ong is not assigned to an ambassadorship.
opt_e = (Sum([If(amb[c] == 4, 1, 0) for c in range(3)]) == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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