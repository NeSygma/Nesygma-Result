from z3 import *

solver = Solver()

# Countries: Venezuela=0, Yemen=1, Zambia=2
# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
candidates = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']
countries = ['Venezuela', 'Yemen', 'Zambia']

# assigned[c] = country assigned to candidate c, or -1 if not assigned
assigned = [Int(f'assigned_{c}') for c in range(5)]

# Each candidate is either assigned to one of the 3 countries or not assigned (-1)
for c in range(5):
    solver.add(Or(assigned[c] == -1, assigned[c] == 0, assigned[c] == 1, assigned[c] == 2))

# No ambassador assigned to more than one country (each candidate assigned to at most one)
# One ambassador per country: each country gets exactly one candidate
# So exactly 3 candidates are assigned, and they are assigned to distinct countries
solver.add(Distinct([assigned[c] for c in range(5)]))

# Exactly 3 candidates are assigned (not -1)
solver.add(Sum([If(assigned[c] != -1, 1, 0) for c in range(5)]) == 3)

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned
solver.add(Xor(assigned[1] != -1, assigned[3] != -1))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(assigned[0] != -1, assigned[1] != -1))

# Constraint 3: If Ong is assigned to Venezuela (0), then Kayne is not assigned to Yemen (1)
solver.add(Implies(assigned[4] == 0, assigned[1] != 1))

# Constraint 4: If Landon is assigned, it is to Zambia (2)
solver.add(Implies(assigned[2] != -1, assigned[2] == 2))

# Now test each option to see which CANNOT be true
# (A) Jaramillo is assigned as ambassador to Zambia.
opt_a = (assigned[0] == 2)

# (B) Kayne is assigned as ambassador to Zambia.
opt_b = (assigned[1] == 2)

# (C) Novetzke is assigned as ambassador to Zambia.
opt_c = (assigned[3] == 2)

# (D) Landon is not assigned to an ambassadorship.
opt_d = (assigned[2] == -1)

# (E) Ong is not assigned to an ambassadorship.
opt_e = (assigned[4] == -1)

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