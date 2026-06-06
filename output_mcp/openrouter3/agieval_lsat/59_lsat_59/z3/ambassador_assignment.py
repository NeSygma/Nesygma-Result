from z3 import *

# Create solver
solver = Solver()

# Define countries
countries = ['Venezuela', 'Yemen', 'Zambia']
country_idx = {c: i for i, c in enumerate(countries)}

# Define ambassadors
ambassadors = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']
amb_idx = {a: i for i, a in enumerate(ambassadors)}

# Create assignment variables: assign[country] = ambassador index
assign = [Int(f'assign_{c}') for c in countries]

# Domain constraints: each country gets one ambassador from 0-4
for i in range(len(countries)):
    solver.add(assign[i] >= 0)
    solver.add(assign[i] <= 4)

# All ambassadors assigned to exactly one country (bijection)
# Since we have 5 ambassadors and 3 countries, only 3 ambassadors will be assigned
# We need to ensure each country gets a distinct ambassador
solver.add(Distinct(assign))

# Helper functions to check if an ambassador is assigned to any country
def is_assigned(amb_idx):
    return Or([assign[i] == amb_idx for i in range(len(countries))])

# Original constraints
# 1. Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
kayne_assigned = is_assigned(amb_idx['Kayne'])
novetzke_assigned = is_assigned(amb_idx['Novetzke'])
solver.add(Or(kayne_assigned, novetzke_assigned))
solver.add(Not(And(kayne_assigned, novetzke_assigned)))

# 2. If Jaramillo is assigned to one of the ambassadorships, then so is Kayne
jaramillo_assigned = is_assigned(amb_idx['Jaramillo'])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# 3. If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen
# We need to check specific country assignments
ong_venezuela = assign[country_idx['Venezuela']] == amb_idx['Ong']
kayne_yemen = assign[country_idx['Yemen']] == amb_idx['Kayne']
solver.add(Implies(ong_venezuela, Not(kayne_yemen)))

# 4. If Landon is assigned to an ambassadorship, it is to Zambia
landon_assigned = is_assigned(amb_idx['Landon'])
landon_zambia = assign[country_idx['Zambia']] == amb_idx['Landon']
solver.add(Implies(landon_assigned, landon_zambia))

# Now test each answer choice by replacing constraint 2
# We'll test each option by removing the original constraint 2 and adding the new one

# Store the original constraint 2 for reference
original_constraint_2 = Implies(jaramillo_assigned, kayne_assigned)

# Define the options
opt_a_constr = Implies(kayne_assigned, jaramillo_assigned)  # A: If Kayne is assigned, then Jaramillo is assigned
opt_b_constr = Implies(And(landon_assigned, is_assigned(amb_idx['Ong'])), novetzke_assigned)  # B: If Landon and Ong are both assigned, then Novetzke is assigned
opt_c_constr = Implies(Not(is_assigned(amb_idx['Ong'])), kayne_assigned)  # C: If Ong is not assigned, then Kayne is assigned
opt_d_constr = Not(And(jaramillo_assigned, novetzke_assigned))  # D: Jaramillo and Novetzke are not both assigned
opt_e_constr = Not(And(novetzke_assigned, is_assigned(amb_idx['Ong'])))  # E: Novetzke and Ong are not both assigned

# Test each option
found_options = []

# Test option A
solver.push()
solver.remove(original_constraint_2)  # Remove original constraint 2
solver.add(opt_a_constr)  # Add option A
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Test option B
solver.push()
solver.remove(original_constraint_2)
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Test option C
solver.push()
solver.remove(original_constraint_2)
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Test option D
solver.push()
solver.remove(original_constraint_2)
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Test option E
solver.push()
solver.remove(original_constraint_2)
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append('E')
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