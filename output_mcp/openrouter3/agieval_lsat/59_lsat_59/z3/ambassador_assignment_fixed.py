from z3 import *

# Define countries
countries = ['Venezuela', 'Yemen', 'Zambia']
country_idx = {c: i for i, c in enumerate(countries)}

# Define ambassadors
ambassadors = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']
amb_idx = {a: i for i, a in enumerate(ambassadors)}

# Create assignment variables: assign[country] = ambassador index
assign = [Int(f'assign_{c}') for c in countries]

# Helper functions to check if an ambassador is assigned to any country
def is_assigned(amb_idx):
    return Or([assign[i] == amb_idx for i in range(len(countries))])

# Original constraints (without the constraint we're testing)
def add_base_constraints(solver):
    # Domain constraints: each country gets one ambassador from 0-4
    for i in range(len(countries)):
        solver.add(assign[i] >= 0)
        solver.add(assign[i] <= 4)
    
    # All ambassadors assigned to exactly one country (bijection)
    solver.add(Distinct(assign))
    
    # 1. Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
    kayne_assigned = is_assigned(amb_idx['Kayne'])
    novetzke_assigned = is_assigned(amb_idx['Novetzke'])
    solver.add(Or(kayne_assigned, novetzke_assigned))
    solver.add(Not(And(kayne_assigned, novetzke_assigned)))
    
    # 3. If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen
    ong_venezuela = assign[country_idx['Venezuela']] == amb_idx['Ong']
    kayne_yemen = assign[country_idx['Yemen']] == amb_idx['Kayne']
    solver.add(Implies(ong_venezuela, Not(kayne_yemen)))
    
    # 4. If Landon is assigned to an ambassadorship, it is to Zambia
    landon_assigned = is_assigned(amb_idx['Landon'])
    landon_zambia = assign[country_idx['Zambia']] == amb_idx['Landon']
    solver.add(Implies(landon_assigned, landon_zambia))

# Define the options (the constraint we're testing)
jaramillo_assigned = is_assigned(amb_idx['Jaramillo'])
kayne_assigned = is_assigned(amb_idx['Kayne'])
novetzke_assigned = is_assigned(amb_idx['Novetzke'])
landon_assigned = is_assigned(amb_idx['Landon'])

opt_a_constr = Implies(kayne_assigned, jaramillo_assigned)  # A: If Kayne is assigned, then Jaramillo is assigned
opt_b_constr = Implies(And(landon_assigned, is_assigned(amb_idx['Ong'])), novetzke_assigned)  # B: If Landon and Ong are both assigned, then Novetzke is assigned
opt_c_constr = Implies(Not(is_assigned(amb_idx['Ong'])), kayne_assigned)  # C: If Ong is not assigned, then Kayne is assigned
opt_d_constr = Not(And(jaramillo_assigned, novetzke_assigned))  # D: Jaramillo and Novetzke are not both assigned
opt_e_constr = Not(And(novetzke_assigned, is_assigned(amb_idx['Ong'])))  # E: Novetzke and Ong are not both assigned

# Test each option
found_options = []

# Test option A
solver = Solver()
add_base_constraints(solver)
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append('A')

# Test option B
solver = Solver()
add_base_constraints(solver)
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append('B')

# Test option C
solver = Solver()
add_base_constraints(solver)
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append('C')

# Test option D
solver = Solver()
add_base_constraints(solver)
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append('D')

# Test option E
solver = Solver()
add_base_constraints(solver)
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append('E')

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