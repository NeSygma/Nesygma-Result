from z3 import *

# Buildings with their classes and values:
buildings = [
    ('Garza Tower', 1, 4),
    ('Yates House', 3, 1),
    ('Zimmer House', 3, 1),
    ('Flores Tower', 1, 4),
    ('Lynch Building', 2, 2),
    ('King Building', 2, 2),
    ('Meyer Building', 2, 2),
    ('Ortiz Building', 2, 2)
]

num_buildings = len(buildings)
building_classes = [b[1] for b in buildings]
building_values = [b[2] for b in buildings]

# Final ownership: 0=RealProp, 1=Southco, 2=Trustcorp
owner = [Int(f'owner_{i}') for i in range(num_buildings)]

solver = Solver()

# Each building owned by exactly one company
for i in range(num_buildings):
    solver.add(Or([owner[i] == j for j in range(3)]))

# Condition: RealProp (company 0) owns only class 2 buildings
for i in range(num_buildings):
    solver.add(Implies(owner[i] == 0, building_classes[i] == 2))

# RealProp must have exactly 3 buildings (since it starts with 3 and ends with 3)
solver.add(Sum([If(owner[i] == 0, 1, 0) for i in range(num_buildings)]) == 3)

# RealProp's total value must be 6
solver.add(Sum([If(owner[i] == 0, building_values[i], 0) for i in range(num_buildings)]) == 6)

# Now, let's check each answer choice.

# First, let's get building indices:
building_names = [b[0] for b in buildings]
building_to_idx = {name: i for i, name in enumerate(building_names)}

yates_idx = building_to_idx['Yates House']
zimmer_idx = building_to_idx['Zimmer House']
flores_idx = building_to_idx['Flores Tower']
meyer_idx = building_to_idx['Meyer Building']
garza_idx = building_to_idx['Garza Tower']
lynch_idx = building_to_idx['Lynch Building']
king_idx = building_to_idx['King Building']
ortiz_idx = building_to_idx['Ortiz Building']

# Company indices:
realprop_idx = 0
southco_idx = 1
trustcorp_idx = 2

# Define the negations of each choice:
opt_a_constr = Not(Or([And(owner[i] == trustcorp_idx, building_classes[i] == 1) for i in range(num_buildings)]))
opt_b_constr = Not(owner[meyer_idx] == trustcorp_idx)
opt_c_constr = Not(Or([And(owner[i] == southco_idx, building_classes[i] == 2) for i in range(num_buildings)]))
opt_d_constr = Not(And(owner[yates_idx] == southco_idx, owner[zimmer_idx] == southco_idx))
opt_e_constr = Not(owner[flores_idx] == southco_idx)

# Now, test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Interpret results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")