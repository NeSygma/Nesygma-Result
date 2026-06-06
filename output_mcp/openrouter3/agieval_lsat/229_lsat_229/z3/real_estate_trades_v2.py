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

# Trade constraints: The final distribution must be reachable via trades.
# Each trade is one of three types:
# 1. Trade one building for another of the same class
# 2. Trade one class 1 for two class 2
# 3. Trade one class 2 for two class 3

# Let's think about the net effect of trades on class counts per company.
# For each company, the change in class counts must be achievable via trades.

# Let's define variables for the net change in class counts for each company
# delta[(company, cls)] = final_count - initial_count
initial_counts = {
    (0, 1): 1, (0, 2): 0, (0, 3): 2,  # RealProp
    (1, 1): 1, (1, 2): 1, (1, 3): 0,  # Southco
    (2, 1): 0, (2, 2): 3, (2, 3): 0   # Trustcorp
}

delta = {}
for company in companies:
    for cls in [1, 2, 3]:
        delta[(company, cls)] = Int(f'delta_{company}_{cls}')
        solver.add(delta[(company, cls)] == class_counts[(company, cls)] - initial_counts[(company, cls)])

# The sum of deltas across all companies for each class must be 0
for cls in [1, 2, 3]:
    solver.add(Sum([delta[(company, cls)] for company in companies]) == 0)

# Now, we need to ensure that the deltas are achievable via trades.
# Each trade affects the class counts of two companies (the two parties in the trade).
# Let's think about the possible trade patterns:

# Trade type 1: Same class exchange
# Company A gives 1 class X to B, B gives 1 class X to A
# Net effect: delta_A[X] = 0, delta_B[X] = 0 (no net change)

# Trade type 2: 1 class 1 for 2 class 2
# Company A gives 1 class 1 to B, B gives 2 class 2 to A
# Net effect: delta_A[1] = -1, delta_A[2] = +2, delta_B[1] = +1, delta_B[2] = -2

# Trade type 3: 1 class 2 for 2 class 3
# Company A gives 1 class 2 to B, B gives 2 class 3 to A
# Net effect: delta_A[2] = -1, delta_A[3] = +2, delta_B[2] = +1, delta_B[3] = -2

# Since Trustcorp has delta[2,2] = -3 (it loses 3 class 2 buildings), it must be involved in trades that reduce its class 2 count.
# Trustcorp can only reduce its class 2 count via trade type 3 (giving away class 2 buildings).
# Each trade type 3 reduces Trustcorp's class 2 count by 1 and increases its class 3 count by 2.
# But Trustcorp starts with 0 class 3 buildings and there are only 2 class 3 buildings total.
# So Trustcorp can gain at most 2 class 3 buildings (if it gets both class 3 buildings).
# This means Trustcorp can participate in at most 1 trade type 3 (giving away 1 class 2, getting 2 class 3).
# But Trustcorp needs to lose 3 class 2 buildings. So it must also receive class 2 buildings from other companies and then trade them away again.

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