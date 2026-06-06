from z3 import *

solver = Solver()

# Companies: 0=RealProp, 1=Southco, 2=Trustcorp
companies = [0, 1, 2]

# Buildings with their initial classes and initial owners
buildings_info = [
    ('Garza Tower', 1, 0),      # class 1, initially RealProp
    ('Yates House', 3, 0),      # class 3, initially RealProp  
    ('Zimmer House', 3, 0),     # class 3, initially RealProp
    ('Flores Tower', 1, 1),     # class 1, initially Southco
    ('Lynch Building', 2, 1),   # class 2, initially Southco
    ('King Building', 2, 2),    # class 2, initially Trustcorp
    ('Meyer Building', 2, 2),   # class 2, initially Trustcorp
    ('Ortiz Building', 2, 2)    # class 2, initially Trustcorp
]

# Create ownership variables: owner[building] = company
owner = {}
for building, cls, init_owner in buildings_info:
    owner[building] = Int(f'owner_{building}')
    solver.add(owner[building] >= 0, owner[building] <= 2)

# Count buildings per class per company
class_counts = {}
for company in companies:
    for cls in [1, 2, 3]:
        class_counts[(company, cls)] = Int(f'count_{company}_{cls}')

# Calculate class counts from ownership
for company in companies:
    for cls in [1, 2, 3]:
        count_expr = Sum([If(owner[building] == company, 1, 0) for building, b_cls, _ in buildings_info if b_cls == cls])
        solver.add(class_counts[(company, cls)] == count_expr)

# Constraint: Trustcorp has no class 2 buildings
solver.add(class_counts[(2, 2)] == 0)

# Total class counts are fixed
total_class1 = 2
total_class2 = 4
total_class3 = 2

# Let's think about the trade constraints more carefully.
# Each trade involves two companies exchanging buildings according to one of the three rules.
# The key insight: Trustcorp must end with 0 class 2 buildings, but it starts with 3 class 2 buildings.
# Therefore, Trustcorp must give away all 3 of its class 2 buildings.
# Since Trustcorp has no class 1 or class 3 buildings initially, it can only receive buildings through trades.

# Let's consider the possible trades Trustcorp can make:
# 1. Trade type 3: Give 1 class 2, receive 2 class 3
#    - Trustcorp can do this at most once because there are only 2 class 3 buildings total.
#    - If Trustcorp does this once, it gives away 1 class 2 and receives 2 class 3.
#    - Then Trustcorp has 2 class 2 buildings left and 2 class 3 buildings.
#    - But Trustcorp needs to end with 0 class 2 buildings, so it must give away the remaining 2 class 2 buildings.
#    - To give away class 2 buildings, Trustcorp needs to receive something in return.
#    - Trustcorp can receive class 2 buildings from other companies (via trade type 1) or class 1 buildings (via trade type 2).

# This is getting complex. Let's try a different approach.
# Instead of modeling the trade process, let's use the fact that the final distribution must satisfy certain constraints.
# Let's check each answer choice by seeing if it's necessarily true.

# We'll use the multiple choice skeleton.

found_options = []

# Option A: RealProp owns a class 1 building.
opt_a_constr = Or([owner[building] == 0 for building, cls, _ in buildings_info if cls == 1])

# Option B: Southco owns only class 2 buildings.
opt_b_constr = And(
    class_counts[(1, 1)] == 0,
    class_counts[(1, 3)] == 0
)

# Option C: Southco has made at least one trade with Trustcorp.
# This means that in the final state, at least one building that was initially owned by Southco is now owned by Trustcorp,
# or at least one building that was initially owned by Trustcorp is now owned by Southco.
opt_c_constr = Or(
    Or([owner[building] == 2 for building, _, init_owner in buildings_info if init_owner == 1]),
    Or([owner[building] == 1 for building, _, init_owner in buildings_info if init_owner == 2])
)

# Option D: Trustcorp owns the Garza Tower.
opt_d_constr = owner['Garza Tower'] == 2

# Option E: Trustcorp owns the Zimmer House.
opt_e_constr = owner['Zimmer House'] == 2

# Now test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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