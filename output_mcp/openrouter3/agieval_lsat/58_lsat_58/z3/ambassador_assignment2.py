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
count_kayne_or_novetzke = Sum([If(Or(a == 1, a == 3), 1, 0) for a in assignment])
solver.add(count_kayne_or_novetzke == 1)

# Constraint 2: If Jaramillo (0) is assigned, then Kayne (1) is assigned
jaramillo_assigned = Or([a == 0 for a in assignment])
kayne_assigned = Or([a == 1 for a in assignment])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong (4) is assigned to Venezuela (index 0), then Kayne is not assigned to Yemen (index 1)
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))

# Constraint 4: If Landon (2) is assigned, it is to Zambia (index 2)
landon_assigned = Or([a == 2 for a in assignment])
solver.add(Implies(landon_assigned, assignment[2] == 2))

# Now test each option - we want to find which option CANNOT be true
# That means when we add that option, the problem becomes UNSAT
# So we check for each option: if adding it makes solver UNSAT, then that option cannot be true

# Option A: Jaramillo is assigned as ambassador to Zambia
opt_a = (assignment[2] == 0)

# Option B: Kayne is assigned as ambassador to Zambia
opt_b = (assignment[2] == 1)

# Option C: Novetzke is assigned as ambassador to Zambia
opt_c = (assignment[2] == 3)

# Option D: Landon is not assigned to an ambassadorship
opt_d = Not(landon_assigned)

# Option E: Ong is not assigned to an ambassadorship
opt_e = Not(Or([a == 4 for a in assignment]))

# For each option, check if adding it makes the problem UNSAT
cannot_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        cannot_be_true.append(letter)
    solver.pop()

if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true: {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that cannot be true")