from z3 import *

# Define countries and ambassadors
countries = ['Venezuela', 'Yemen', 'Zambia']
ambassadors = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']

# Create boolean variables: assigned[a][c] = True if ambassador a assigned to country c
assigned = {}
for a in ambassadors:
    for c in countries:
        assigned[(a, c)] = Bool(f'assigned_{a}_{c}')

# Helper sums
def sum_assigned(amb):
    return Sum([assigned[(amb, c)] for c in countries])

def sum_assigned_to_country(country):
    return Sum([assigned[(a, country)] for a in ambassadors])

# Base constraints
solver = Solver()

# Each country gets exactly one ambassador
for c in countries:
    solver.add(sum_assigned_to_country(c) == 1)

# Each ambassador assigned to at most one country
for a in ambassadors:
    solver.add(sum_assigned(a) <= 1)

# Constraint 1: Exactly one of Kayne or Novetzke is assigned
solver.add(sum_assigned('Kayne') + sum_assigned('Novetzke') == 1)

# Constraint 2: If Jaramillo assigned, then Kayne assigned
solver.add(Implies(sum_assigned('Jaramillo') == 1, sum_assigned('Kayne') == 1))

# Constraint 3: If Ong assigned to Venezuela, then Kayne not assigned to Yemen
solver.add(Implies(assigned[('Ong', 'Venezuela')], Not(assigned[('Kayne', 'Yemen')])))

# Constraint 4: If Landon assigned, then Landon assigned to Zambia
solver.add(Implies(sum_assigned('Landon') == 1, assigned[('Landon', 'Zambia')]))

# Now define option constraints
def option_constraints(option):
    # option is a list of tuples (country, ambassador)
    constraints = []
    for country, amb in option:
        constraints.append(assigned[(amb, country)])
    # Also ensure that the other ambassadors are not assigned to those countries? Actually, the base constraints already enforce each country gets exactly one ambassador, so if we assign a specific ambassador to a country, that's enough. However, we also need to ensure that the other ambassadors are not assigned to that country? The base constraint sum_assigned_to_country(c) == 1 ensures exactly one ambassador per country, so if we assign amb to country, that's fine. But we also need to ensure that the other ambassadors are not assigned to that country? The sum constraint will enforce that only one ambassador is assigned to that country. However, we also need to ensure that the other ambassadors are not assigned to that country? Actually, the sum constraint ensures that exactly one ambassador is assigned to that country. If we add a constraint that amb is assigned to that country, then the sum constraint will force the other ambassadors to be not assigned to that country. So we don't need extra constraints.
    return constraints

# Options as per the problem
opt_a = [('Venezuela', 'Jaramillo'), ('Yemen', 'Ong'), ('Zambia', 'Novetzke')]
opt_b = [('Venezuela', 'Kayne'), ('Yemen', 'Jaramillo'), ('Zambia', 'Landon')]
opt_c = [('Venezuela', 'Landon'), ('Yemen', 'Novetzke'), ('Zambia', 'Ong')]
opt_d = [('Venezuela', 'Novetzke'), ('Yemen', 'Jaramillo'), ('Zambia', 'Kayne')]
opt_e = [('Venezuela', 'Ong'), ('Yemen', 'Kayne'), ('Zambia', 'Landon')]

# Evaluate each option
found_options = []
for letter, opt in [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]:
    solver.push()
    solver.add(option_constraints(opt))
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")