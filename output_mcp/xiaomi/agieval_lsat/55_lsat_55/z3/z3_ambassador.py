from z3 import *

solver = Solver()

# Countries: Venezuela=0, Yemen=1, Zambia=2
# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
candidates = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']
countries = ['Venezuela', 'Yemen', 'Zambia']

# assigned[c] = country index (0,1,2) if assigned, -1 if not assigned
assigned = [Int(f'assigned_{c}') for c in candidates]

# Each assigned value is either -1 (not assigned) or 0,1,2 (a country)
for i in range(5):
    solver.add(Or(assigned[i] == -1, assigned[i] == 0, assigned[i] == 1, assigned[i] == 2))

# No ambassador assigned to more than one country (each country gets at most one)
# Countries are 0,1,2 - each must be assigned to exactly one candidate
for country in range(3):
    solver.add(Sum([If(assigned[i] == country, 1, 0) for i in range(5)]) == 1)

# Exactly 3 candidates are assigned (one per country), 2 are not
solver.add(Sum([If(assigned[i] != -1, 1, 0) for i in range(5)]) == 3)

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned
solver.add(Xor(assigned[1] != -1, assigned[3] != -1))

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned
solver.add(Implies(assigned[0] != -1, assigned[1] != -1))

# Constraint 3: If Ong(4) is assigned to Venezuela(0), Kayne(1) is not assigned to Yemen(1)
solver.add(Implies(assigned[4] == 0, assigned[1] != 1))

# Constraint 4: If Landon(2) is assigned, it is to Zambia(2)
solver.add(Implies(assigned[2] != -1, assigned[2] == 2))

# Now check each answer option: which pair of candidates could be the two NOT assigned?
# Option A: Jaramillo(0) and Novetzke(3) not assigned
opt_a = And(assigned[0] == -1, assigned[3] == -1)
# Option B: Jaramillo(0) and Ong(4) not assigned
opt_b = And(assigned[0] == -1, assigned[4] == -1)
# Option C: Kayne(1) and Landon(2) not assigned
opt_c = And(assigned[1] == -1, assigned[2] == -1)
# Option D: Kayne(1) and Novetzke(3) not assigned
opt_d = And(assigned[1] == -1, assigned[3] == -1)
# Option E: Landon(2) and Ong(4) not assigned
opt_e = And(assigned[2] == -1, assigned[4] == -1)

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