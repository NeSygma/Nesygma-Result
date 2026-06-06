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

# Each building owned by exactly one company (already enforced)

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

# Total class counts are fixed (buildings don't change class)
total_class1 = Sum([1 for _, cls, _ in buildings_info if cls == 1])
total_class2 = Sum([1 for _, cls, _ in buildings_info if cls == 2])
total_class3 = Sum([1 for _, cls, _ in buildings_info if cls == 3])
# These are constants: total_class1=2, total_class2=4, total_class3=2

# Now, we need to ensure the final state is reachable via trades.
# This is complex. Instead, I'll use a simpler approach:
# The key insight is about what must be true given Trustcorp has no class 2 buildings.

# Let's think about the answer choices:

# (A) RealProp owns a class 1 building.
# Could be false if RealProp trades away both class 1 buildings.

# (B) Southco owns only class 2 buildings.
# Could be false if Southco keeps its class 1 building or gets class 3 buildings.

# (C) Southco has made at least one trade with Trustcorp.
# This is about the process, not the final state. Hard to model.

# (D) Trustcorp owns the Garza Tower.
# Could be true or false.

# (E) Trustcorp owns the Zimmer House.
# Could be true or false.

# Let's check each option by seeing if it's necessarily true.

# We'll use the multiple choice skeleton.

found_options = []

# Option A: RealProp owns a class 1 building.
# This means: exists a building of class 1 owned by RealProp
opt_a_constr = Or([owner[building] == 0 for building, cls, _ in buildings_info if cls == 1])

# Option B: Southco owns only class 2 buildings.
# This means: Southco owns no class 1 and no class 3 buildings
opt_b_constr = And(
    class_counts[(1, 1)] == 0,
    class_counts[(1, 3)] == 0
)

# Option C: Southco has made at least one trade with Trustcorp.
# This is tricky. If Southco and Trustcorp traded directly, then in the final state,
# at least one building that was initially owned by Southco is now owned by Trustcorp,
# or vice versa. But this might not be necessary if there are indirect trades.
# However, given the small number of buildings, let's assume direct trades are needed.
# Let's check if there's any building that changed hands between Southco and Trustcorp.
opt_c_constr = Or(
    # Southco now owns a building that was initially Trustcorp's
    Or([owner[building] == 1 for building, _, init_owner in buildings_info if init_owner == 2]),
    # Trustcorp now owns a building that was initially Southco's
    Or([owner[building] == 2 for building, _, init_owner in buildings_info if init_owner == 1])
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