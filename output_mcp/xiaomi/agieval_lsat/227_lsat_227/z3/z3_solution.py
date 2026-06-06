from z3 import *

# Define buildings and their classes
buildings = {
    'Garza': 1, 'Yates': 3, 'Zimmer': 3,  # RealProp
    'Flores': 1, 'Lynch': 2,              # Southco
    'King': 2, 'Meyer': 2, 'Ortiz': 2     # Trustcorp
}

all_buildings = list(buildings.keys())
building_index = {b: i for i, b in enumerate(all_buildings)}

# Value function: class1=4, class2=2, class3=1
def class_value(cls):
    if cls == 1:
        return 4
    elif cls == 2:
        return 2
    else:  # cls == 3
        return 1

# Create solver
solver = Solver()

# Create Z3 variables for ownership (0=RealProp, 1=Southco, 2=Trustcorp)
owner_vars = [Int(f'owner_{b}') for b in all_buildings]

# Base constraints: each owner is 0,1,2
for i in range(len(all_buildings)):
    solver.add(And(0 <= owner_vars[i], owner_vars[i] <= 2))

# Value constraints: for each company, sum of values of buildings it owns = 6
for c in range(3):
    value_sum = Sum([If(owner_vars[i] == c, class_value(buildings[all_buildings[i]]), 0) for i in range(len(all_buildings))])
    solver.add(value_sum == 6)

# Define option constraints
# Option A: RealProp owns Flores and Garza.
opt_a_constr = And(owner_vars[building_index['Flores']] == 0, owner_vars[building_index['Garza']] == 0)

# Option B: Southco owns Flores and Meyer.
opt_b_constr = And(owner_vars[building_index['Flores']] == 1, owner_vars[building_index['Meyer']] == 1)

# Option C: Southco owns Garza and Lynch.
opt_c_constr = And(owner_vars[building_index['Garza']] == 1, owner_vars[building_index['Lynch']] == 1)

# Option D: Trustcorp owns Flores and Ortiz.
opt_d_constr = And(owner_vars[building_index['Flores']] == 2, owner_vars[building_index['Ortiz']] == 2)

# Option E: Trustcorp owns Garza and Meyer.
opt_e_constr = And(owner_vars[building_index['Garza']] == 2, owner_vars[building_index['Meyer']] == 2)

# Now evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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