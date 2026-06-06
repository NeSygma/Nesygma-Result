from z3 import *

# Create solver
solver = Solver()

# Countries: 0=Venezuela, 1=Yemen, 2=Zambia
# Candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
countries = ["Venezuela", "Yemen", "Zambia"]
candidates = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Variables: assignment[country] = candidate index
assignment = [Int(f"assign_{c}") for c in countries]

# Domain constraints: each assignment must be 0-4
for a in assignment:
    solver.add(a >= 0, a <= 4)

# All ambassadors assigned to at most one country (all different)
solver.add(Distinct(assignment))

# Constraint 1: Either Kayne (1) or Novetzke (3), but not both, is assigned
# Count how many of {1,3} are in assignment
count_kayne_or_novetzke = Sum([If(Or(a == 1, a == 3), 1, 0) for a in assignment])
solver.add(count_kayne_or_novetzke == 1)

# Constraint 2: If Jaramillo (0) is assigned, then Kayne (1) is assigned
# Jaramillo assigned means at least one country has candidate 0
jaramillo_assigned = Or([a == 0 for a in assignment])
kayne_assigned = Or([a == 1 for a in assignment])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong (4) is assigned to Venezuela (index 0), then Kayne is not assigned to Yemen (index 1)
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))

# Constraint 4: If Landon (2) is assigned, it is to Zambia (index 2)
# This means: if Landon appears in assignment, it must be at index 2 (Zambia)
landon_assigned = Or([a == 2 for a in assignment])
solver.add(Implies(landon_assigned, assignment[2] == 2))

# Now test each option
# Option A: Jaramillo is assigned as ambassador to Zambia
opt_a = (assignment[2] == 0)  # Zambia gets Jaramillo

# Option B: Kayne is assigned as ambassador to Zambia
opt_b = (assignment[2] == 1)  # Zambia gets Kayne

# Option C: Novetzke is assigned as ambassador to Zambia
opt_c = (assignment[2] == 3)  # Zambia gets Novetzke

# Option D: Landon is not assigned to an ambassadorship
opt_d = Not(landon_assigned)  # Landon not assigned anywhere

# Option E: Ong is not assigned to an ambassadorship
opt_e = Not(Or([a == 4 for a in assignment]))  # Ong not assigned anywhere

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