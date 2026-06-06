from z3 import *

# Companies
companies = ['RealProp', 'Southco', 'Trustcorp']
# Buildings with their initial class and owner
buildings = {
    'Garza Tower': (1, 'RealProp'),
    'Yates House': (3, 'RealProp'),
    'Zimmer House': (3, 'RealProp'),
    'Flores Tower': (1, 'Southco'),
    'Lynch Building': (2, 'Southco'),
    'King Building': (2, 'Trustcorp'),
    'Meyer Building': (2, 'Trustcorp'),
    'Ortiz Building': (2, 'Trustcorp')
}

# For each building, track which company owns it after trades
# Use a function: building_owner(building_name) -> company_index
# We'll use an array indexed by building name, but since building names are strings,
# we'll map them to indices
building_names = list(buildings.keys())
building_to_idx = {name: i for i, name in enumerate(building_names)}
num_buildings = len(building_names)

# company_index: 0=RealProp, 1=Southco, 2=Trustcorp
company_to_idx = {name: i for i, name in enumerate(companies)}

# For each building, final owner (0,1,2)
building_owner = [Int(f'owner_{i}') for i in range(num_buildings)]

# Constraints: each building must be owned by exactly one company
solver = Solver()
for i in range(num_buildings):
    solver.add(Or([building_owner[i] == j for j in range(3)]))

# Initial ownership constraint (but trades can change this, so we don't enforce it)
# Actually, we need to model that trades can change ownership, but we need to ensure
# that the final state is reachable through valid trades.

# Instead of modeling individual trades, we can think about what final states are possible.
# The key insight: trades preserve certain invariants.

# Let's think about the total "value" or "class sum" across all companies.
# But trades change the number of buildings.

# Alternative approach: Since we only care about the final condition (RealProp has only class 2),
# and we want to know which statements must be true, we can:
# 1. Find all possible final states satisfying the condition
# 2. Check which statements are true in all such states

# But enumerating all states is hard. Instead, we can use Z3 to check each statement:
# For each statement, check if there exists a valid final state where RealProp has only class 2
# AND the statement is false. If no such state exists, then the statement must be true.

# So for each answer choice, we'll check satisfiability of:
# - Final state reachable through trades
# - RealProp has only class 2 buildings
# - The answer choice is FALSE

# If unsat, then the answer choice must be true.

# But we need to model "reachable through trades". This is complex.

# Let's simplify: Since trades are reversible, any redistribution of buildings that preserves
# certain invariants might be reachable. What invariants are preserved?

# Let's calculate total "class value" or something.

# Actually, let's think about the total number of buildings of each class across all companies.
# Initially:
# Class 1: Garza Tower, Flores Tower → 2 buildings
# Class 2: Lynch Building, King Building, Meyer Building, Ortiz Building → 4 buildings
# Class 3: Yates House, Zimmer House → 2 buildings

# Trade rules:
# 1. Same class exchange: no change in counts
# 2. 1 class 1 → 2 class 2: decreases class 1 by 1, increases class 2 by 2
# 3. 1 class 2 → 2 class 3: decreases class 2 by 1, increases class 3 by 2

# So the total counts can change. Let's define variables for final counts per company.

# For each company, count of buildings of each class
count = {}
for comp in companies:
    for cls in [1,2,3]:
        count[(comp, cls)] = Int(f'count_{comp}_{cls}')

# Constraints: counts must be non-negative
for comp in companies:
    for cls in [1,2,3]:
        solver.add(count[(comp, cls)] >= 0)

# Total buildings per company can vary
# But we also need to track specific buildings for answer choices.

# Let's first focus on the condition: RealProp has only class 2 buildings
# This means: count[('RealProp', 1)] == 0 and count[('RealProp', 3)] == 0
# And count[('RealProp', 2)] >= 0 (could be zero? but probably not, since they start with 3 buildings)

# But wait, RealProp starts with 1 class 1 and 2 class 3. To end with only class 2,
# they must trade away their class 1 and class 3 buildings and acquire class 2 buildings.

# Let's add the final condition:
solver.add(count[('RealProp', 1)] == 0)
solver.add(count[('RealProp', 3)] == 0)
solver.add(count[('RealProp', 2)] >= 0)  # could be zero, but let's see

# Now, we need to ensure that the final counts are reachable through trades.
# The trades change the total counts of each class across all companies.

# Let's define total counts across all companies:
total_class1 = Sum([count[(comp, 1)] for comp in companies])
total_class2 = Sum([count[(comp, 2)] for comp in companies])
total_class3 = Sum([count[(comp, 3)] for comp in companies])

# Initial totals:
# Class 1: 2, Class 2: 4, Class 3: 2

# Trades can change these totals. Let's see the possible changes:
# Rule 2: 1 class 1 → 2 class 2: Δclass1 = -1, Δclass2 = +2
# Rule 3: 1 class 2 → 2 class 3: Δclass2 = -1, Δclass3 = +2

# So the totals can change by multiples of these deltas.

# Let's define variables for how many times each trade type is applied:
# Let x = number of rule 2 trades (1 class 1 → 2 class 2)
# Let y = number of rule 3 trades (1 class 2 → 2 class 3)
# Rule 1 trades don't change totals, so we can ignore them for totals.

# Then:
# total_class1 = 2 - x
# total_class2 = 4 + 2x - y
# total_class3 = 2 + 2y

# But x and y must be non-negative integers, and we can't have negative counts.
# Also, we can't have more rule 2 trades than available class 1 buildings (2 initially).
# Similarly, for rule 3, we need enough class 2 buildings.

# However, note that rule 2 trades consume class 1 buildings and produce class 2 buildings,
# which can then be used in rule 3 trades.

# Let's add these constraints:
x = Int('x')  # number of rule 2 trades
y = Int('y')  # number of rule 3 trades
solver.add(x >= 0)
solver.add(y >= 0)

# Total class 1 buildings after trades: 2 - x >= 0
solver.add(total_class1 == 2 - x)
solver.add(total_class1 >= 0)

# Total class 2 buildings after trades: 4 + 2x - y >= 0
solver.add(total_class2 == 4 + 2*x - y)
solver.add(total_class2 >= 0)

# Total class 3 buildings after trades: 2 + 2y >= 0 (always true)
solver.add(total_class3 == 2 + 2*y)

# Now, we also need to ensure that the counts per company sum to the totals:
for cls in [1,2,3]:
    if cls == 1:
        solver.add(Sum([count[(comp, cls)] for comp in companies]) == total_class1)
    elif cls == 2:
        solver.add(Sum([count[(comp, cls)] for comp in companies]) == total_class2)
    else:
        solver.add(Sum([count[(comp, cls)] for comp in companies]) == total_class3)

# Now, we need to model that specific buildings are owned by specific companies.
# But we have counts, not specific buildings. For answer choices that mention specific buildings,
# we need to track them.

# Let's track ownership of specific buildings. For each building, we have a variable for its owner.
# We already defined building_owner[i] for each building i.

# We need to relate the counts to the specific buildings.
# For each company and class, the count should equal the number of buildings of that class owned by that company.

# For each company c and class cls:
# count[(c, cls)] = number of buildings i such that building_owner[i] == company_to_idx[c] and building class of i == cls

# We can express this using Sum and If:
for comp in companies:
    comp_idx = company_to_idx[comp]
    for cls in [1,2,3]:
        # For each building, check if it's owned by comp and has class cls
        terms = []
        for i, (b_name, (b_class, _)) in enumerate(buildings.items()):
            # If building i has class cls and owner is comp_idx, contribute 1
            terms.append(If(And(building_owner[i] == comp_idx, b_class == cls), 1, 0))
        solver.add(count[(comp, cls)] == Sum(terms))

# Now, we have a complete model of final ownership counts and specific building ownership.

# But we haven't enforced that the final state is reachable through trades.
# The counts constraints above ensure that the totals match what's possible through trades,
# but we also need to ensure that the distribution among companies is possible.

# However, since trades can involve any companies, and we're only constraining totals,
# any distribution of buildings among companies that matches the totals should be reachable
# through some sequence of trades (assuming we can always find a sequence).

# This might be an over-approximation, but for this problem, it should be sufficient.

# Now, let's check each answer choice.

# Answer choices:
# (A) Trustcorp owns a class 1 building.
# (B) Trustcorp owns the Meyer Building.
# (C) Southco owns a class 2 Building.
# (D) Southco owns both of the class 3 buildings.
# (E) Southco owns the Flores Tower.

# We need to check for each choice: is there a valid final state where RealProp has only class 2
# AND the choice is FALSE? If no such state exists, then the choice must be true.

# Let's define the conditions for each choice being false:

# (A) False: Trustcorp owns NO class 1 building.
#    That means count[('Trustcorp', 1)] == 0

# (B) False: Trustcorp does NOT own the Meyer Building.
#    Meyer Building is building index: building_to_idx['Meyer Building']
#    So building_owner[that_index] != company_to_idx['Trustcorp']

# (C) False: Southco owns NO class 2 building.
#    That means count[('Southco', 2)] == 0

# (D) False: Southco does NOT own both class 3 buildings.
#    There are two class 3 buildings: Yates House and Zimmer House.
#    So either Southco doesn't own Yates House OR doesn't own Zimmer House.
#    Let yates_idx = building_to_idx['Yates House']
#    Let zimmer_idx = building_to_idx['Zimmer House']
#    So: Not(And(building_owner[yates_idx] == company_to_idx['Southco'],
#                building_owner[zimmer_idx] == company_to_idx['Southco']))

# (E) False: Southco does NOT own the Flores Tower.
#    Flores Tower is building index: building_to_idx['Flores Tower']
#    So building_owner[that_index] != company_to_idx['Southco']

# Now, for each choice, we'll check satisfiability of the model plus the negation of the choice.

# But note: we already have the base model (with RealProp having only class 2).
# We'll create a new solver for each choice, add the base constraints, add the negation of the choice,
# and check satisfiability.

# If unsat, then the choice must be true.

# Let's implement this.

# First, let's get the building indices:
yates_idx = building_to_idx['Yates House']
zimmer_idx = building_to_idx['Zimmer House']
flores_idx = building_to_idx['Flores Tower']
meyer_idx = building_to_idx['Meyer Building']

# Company indices:
realprop_idx = company_to_idx['RealProp']
southco_idx = company_to_idx['Southco']
trustcorp_idx = company_to_idx['Trustcorp']

# Now, for each choice, we'll check.

found_options = []

# Choice A: Trustcorp owns a class 1 building.
# We check if there exists a state where RealProp has only class 2 AND Trustcorp has NO class 1 building.
s_a = Solver()
# Add all base constraints from the solver (we need to copy them)
# Instead of copying, let's rebuild the solver for each choice.
# But that's inefficient. Let's use solver.push() and solver.pop() as per the skeleton.

# Actually, let's use the skeleton approach: we have a base solver with all constraints,
# then for each choice, we push, add the negation of the choice, check, pop.

# But we haven't added all constraints to the solver yet. Let's add them.

# First, let's add all constraints we have so far to the solver.
# We'll create a function to add base constraints.

def add_base_constraints(s):
    # Add count constraints
    for comp in companies:
        for cls in [1,2,3]:
            s.add(count[(comp, cls)] >= 0)
    
    # Add final condition for RealProp
    s.add(count[('RealProp', 1)] == 0)
    s.add(count[('RealProp', 3)] == 0)
    s.add(count[('RealProp', 2)] >= 0)
    
    # Add trade variables and total constraints
    s.add(x >= 0)
    s.add(y >= 0)
    s.add(total_class1 == 2 - x)
    s.add(total_class1 >= 0)
    s.add(total_class2 == 4 + 2*x - y)
    s.add(total_class2 >= 0)
    s.add(total_class3 == 2 + 2*y)
    
    # Add sum constraints
    s.add(Sum([count[(comp, 1)] for comp in companies]) == total_class1)
    s.add(Sum([count[(comp, 2)] for comp in companies]) == total_class2)
    s.add(Sum([count[(comp, 3)] for comp in companies]) == total_class3)
    
    # Add building owner constraints
    for i in range(num_buildings):
        s.add(Or([building_owner[i] == j for j in range(3)]))
    
    # Add count to building owner mapping
    for comp in companies:
        comp_idx = company_to_idx[comp]
        for cls in [1,2,3]:
            terms = []
            for i, (b_name, (b_class, _)) in enumerate(buildings.items()):
                terms.append(If(And(building_owner[i] == comp_idx, b_class == cls), 1, 0))
            s.add(count[(comp, cls)] == Sum(terms))

# Now, let's use the skeleton approach.

solver = Solver()
add_base_constraints(solver)

# Define the negations of each choice:
opt_a_constr = count[('Trustcorp', 1)] == 0  # False: Trustcorp owns NO class 1 building
opt_b_constr = Not(building_owner[meyer_idx] == trustcorp_idx)  # False: Trustcorp does NOT own Meyer
opt_c_constr = count[('Southco', 2)] == 0  # False: Southco owns NO class 2 building
opt_d_constr = Not(And(building_owner[yates_idx] == southco_idx,
                       building_owner[zimmer_idx] == southco_idx))  # False: Southco does NOT own both class 3
opt_e_constr = Not(building_owner[flores_idx] == southco_idx)  # False: Southco does NOT own Flores Tower

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