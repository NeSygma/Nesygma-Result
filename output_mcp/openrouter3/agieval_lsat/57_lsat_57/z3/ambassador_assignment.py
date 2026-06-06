from z3 import *

# Create solver
solver = Solver()

# Define countries and candidates
countries = ["Venezuela", "Yemen", "Zambia"]
candidates = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Create assignment variables: assign[country] = candidate
# We'll use integer indices for candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
assign = {country: Int(f"assign_{country}") for country in countries}

# Domain constraints: each assignment must be one of the candidates (0-4)
for country in countries:
    solver.add(assign[country] >= 0)
    solver.add(assign[country] <= 4)

# Constraint: Each candidate can be assigned to at most one country
# We'll use Distinct on the assignment values
solver.add(Distinct([assign[country] for country in countries]))

# Additional constraint: Exactly 3 ambassadors are assigned (since we have 3 countries)
# This is already enforced by Distinct with 3 variables taking values from 0-4

# Map candidate names to indices for easier constraint writing
J, K, L, N, O = 0, 1, 2, 3, 4

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
# This means exactly one of K or N appears in the assignments
kayne_assigned = Or([assign[country] == K for country in countries])
novetzke_assigned = Or([assign[country] == N for country in countries])
solver.add(Or(kayne_assigned, novetzke_assigned))  # At least one
solver.add(Not(And(kayne_assigned, novetzke_assigned)))  # Not both

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
jaramillo_assigned = Or([assign[country] == J for country in countries])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assign["Venezuela"] == O, assign["Yemen"] != K))

# Constraint 4: If Landon is assigned, it is to Zambia
landon_assigned = Or([assign[country] == L for country in countries])
solver.add(Implies(landon_assigned, assign["Zambia"] == L))

# PREMISE: Kayne is assigned to Yemen
solver.add(assign["Yemen"] == K)

# Now evaluate each answer choice
# Answer choices:
# (A) Jaramillo is assigned as ambassador to Venezuela.
# (B) Landon is assigned as ambassador to Zambia.
# (C) Ong is assigned as ambassador to Zambia.
# (D) Jaramillo is not assigned to an ambassadorship.
# (E) Ong is not assigned to an ambassadorship.

# Define option constraints
opt_a = assign["Venezuela"] == J
opt_b = assign["Zambia"] == L
opt_c = assign["Zambia"] == O
opt_d = Not(jaramillo_assigned)  # Jaramillo not assigned to any country
opt_e = Not(Or([assign[country] == O for country in countries]))  # Ong not assigned to any country

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")