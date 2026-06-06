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
solver.add(Distinct([assign[country] for country in countries]))

# Map candidate names to indices
J, K, L, N, O = 0, 1, 2, 3, 4

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
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

# Now test each option by checking if its negation makes the problem unsatisfiable
# If adding NOT(option) makes it unsat, then the option must be true in all models

# Define option constraints
opt_a = assign["Venezuela"] == J
opt_b = assign["Zambia"] == L
opt_c = assign["Zambia"] == O
opt_d = Not(jaramillo_assigned)
opt_e = Not(Or([assign[country] == O for country in countries]))

print("Testing which options must be true (adding NOT(option) makes it unsat):")

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))  # Add negation of the option
    result = solver.check()
    print(f"Option {letter} (negated): {result}")
    if result == unsat:
        # If negation is unsat, then the option must be true in all models
        found_options.append(letter)
    solver.pop()

print(f"\nOptions that must be true: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")