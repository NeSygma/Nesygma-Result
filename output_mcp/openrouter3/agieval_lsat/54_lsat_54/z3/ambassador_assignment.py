from z3 import *

# Create solver
solver = Solver()

# Define countries and candidates
countries = ["Venezuela", "Yemen", "Zambia"]
candidates = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Create symbolic variables for each country's ambassador
# We'll use integer encoding for candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
assign = {country: Int(f"assign_{country}") for country in countries}

# Add domain constraints: each country gets one candidate from 0-4
for country in countries:
    solver.add(assign[country] >= 0)
    solver.add(assign[country] <= 4)

# Constraint: Each candidate assigned to at most one country (all different)
solver.add(Distinct([assign[country] for country in countries]))

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
# Kayne = 1, Novetzke = 3
# We need exactly one of them to be assigned to any country
kayne_assigned = Or([assign[country] == 1 for country in countries])
novetzke_assigned = Or([assign[country] == 3 for country in countries])
solver.add(Or(kayne_assigned, novetzke_assigned))  # At least one
solver.add(Not(And(kayne_assigned, novetzke_assigned)))  # Not both

# Constraint 2: If Jaramillo is assigned, then so is Kayne.
# Jaramillo = 0, Kayne = 1
jaramillo_assigned = Or([assign[country] == 0 for country in countries])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen.
# Ong = 4
solver.add(Implies(assign["Venezuela"] == 4, assign["Yemen"] != 1))

# Constraint 4: If Landon is assigned, it is to Zambia.
# Landon = 2
landon_assigned = Or([assign[country] == 2 for country in countries])
solver.add(Implies(landon_assigned, assign["Zambia"] == 2))

# Now test each option
found_options = []

# Option A: Venezuela: Jaramillo (0), Yemen: Ong (4), Zambia: Novetzke (3)
opt_a_constr = And(
    assign["Venezuela"] == 0,
    assign["Yemen"] == 4,
    assign["Zambia"] == 3
)

# Option B: Venezuela: Kayne (1), Yemen: Jaramillo (0), Zambia: Landon (2)
opt_b_constr = And(
    assign["Venezuela"] == 1,
    assign["Yemen"] == 0,
    assign["Zambia"] == 2
)

# Option C: Venezuela: Landon (2), Yemen: Novetzke (3), Zambia: Ong (4)
opt_c_constr = And(
    assign["Venezuela"] == 2,
    assign["Yemen"] == 3,
    assign["Zambia"] == 4
)

# Option D: Venezuela: Novetzke (3), Yemen: Jaramillo (0), Zambia: Kayne (1)
opt_d_constr = And(
    assign["Venezuela"] == 3,
    assign["Yemen"] == 0,
    assign["Zambia"] == 1
)

# Option E: Venezuela: Ong (4), Yemen: Kayne (1), Zambia: Landon (2)
opt_e_constr = And(
    assign["Venezuela"] == 4,
    assign["Yemen"] == 1,
    assign["Zambia"] == 2
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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