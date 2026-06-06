from z3 import *

# Define weights for each class
# Class 1: weight 4, Class 2: weight 2, Class 3: weight 1
# This ensures trades are balanced: 1 class 1 = 2 class 2 = 4 class 3

# Buildings with their classes and weights
buildings = {
    'Garza Tower': 1,
    'Yates House': 3,
    'Zimmer House': 3,
    'Flores Tower': 1,
    'Lynch Building': 2,
    'King Building': 2,
    'Meyer Building': 2,
    'Ortiz Building': 2
}

# Map class to weight
def weight(class_num):
    if class_num == 1:
        return 4
    elif class_num == 2:
        return 2
    else:  # class 3
        return 1

# Companies
companies = ['RealProp', 'Southco', 'Trustcorp']

# For each option, we need to check if there exists a final ownership state
# that satisfies the statement and has total weight 6 for each company

# Define variables for final ownership of each building
ownership = {}
for building in buildings:
    ownership[building] = Int(f'owner_{building}')

# Base solver with constraints that apply to all scenarios
base_solver = Solver()
for building in buildings:
    base_solver.add(Or([ownership[building] == i for i in range(3)]))

# Add constraint that each company's total weight is 6
for i, company in enumerate(companies):
    total_weight = 0
    for building in buildings:
        class_num = buildings[building]
        w = weight(class_num)
        total_weight += If(ownership[building] == i, w, 0)
    base_solver.add(total_weight == 6)

# Now define the options as constraints on ownership
# Option A: RealProp owns Flores Tower and Garza Tower (and no others)
opt_a_constr = And(
    ownership['Flores Tower'] == 0,
    ownership['Garza Tower'] == 0,
    ownership['Yates House'] != 0,
    ownership['Zimmer House'] != 0,
    ownership['Lynch Building'] != 0,
    ownership['King Building'] != 0,
    ownership['Meyer Building'] != 0,
    ownership['Ortiz Building'] != 0
)

# Option B: Southco owns Flores Tower and Meyer Building (and no others)
opt_b_constr = And(
    ownership['Flores Tower'] == 1,
    ownership['Meyer Building'] == 1,
    ownership['Garza Tower'] != 1,
    ownership['Yates House'] != 1,
    ownership['Zimmer House'] != 1,
    ownership['Lynch Building'] != 1,
    ownership['King Building'] != 1,
    ownership['Ortiz Building'] != 1
)

# Option C: Southco owns Garza Tower and Lynch Building (and no others)
opt_c_constr = And(
    ownership['Garza Tower'] == 1,
    ownership['Lynch Building'] == 1,
    ownership['Flores Tower'] != 1,
    ownership['Yates House'] != 1,
    ownership['Zimmer House'] != 1,
    ownership['King Building'] != 1,
    ownership['Meyer Building'] != 1,
    ownership['Ortiz Building'] != 1
)

# Option D: Trustcorp owns Flores Tower and Ortiz Building (and no others)
opt_d_constr = And(
    ownership['Flores Tower'] == 2,
    ownership['Ortiz Building'] == 2,
    ownership['Garza Tower'] != 2,
    ownership['Yates House'] != 2,
    ownership['Zimmer House'] != 2,
    ownership['Lynch Building'] != 2,
    ownership['King Building'] != 2,
    ownership['Meyer Building'] != 2
)

# Option E: Trustcorp owns Garza Tower and Meyer Building (and no others)
opt_e_constr = And(
    ownership['Garza Tower'] == 2,
    ownership['Meyer Building'] == 2,
    ownership['Flores Tower'] != 2,
    ownership['Yates House'] != 2,
    ownership['Zimmer House'] != 2,
    ownership['Lynch Building'] != 2,
    ownership['King Building'] != 2,
    ownership['Ortiz Building'] != 2
)

# Now test each option for UNSAT (cannot be true)
cannot_be_true = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver = Solver()
    # Add base constraints
    for building in buildings:
        solver.add(Or([ownership[building] == i for i in range(3)]))
    # Add weight constraints
    for i, company in enumerate(companies):
        total_weight = 0
        for building in buildings:
            class_num = buildings[building]
            w = weight(class_num)
            total_weight += If(ownership[building] == i, w, 0)
        solver.add(total_weight == 6)
    # Add option constraint
    solver.add(constr)
    # Check
    result = solver.check()
    if result == unsat:
        cannot_be_true.append(letter)

if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that cannot be true")