from z3 import *

# Companies
companies = ['RealProp', 'Southco', 'Trustcorp']

# Buildings with their initial classes
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

# Initial ownership mapping
initial_owner = {
    'Garza Tower': 'RealProp',
    'Yates House': 'RealProp',
    'Zimmer House': 'RealProp',
    'Flores Tower': 'Southco',
    'Lynch Building': 'Southco',
    'King Building': 'Trustcorp',
    'Meyer Building': 'Trustcorp',
    'Ortiz Building': 'Trustcorp'
}

# Create ownership variables: owner[building] = company
owner = {}
for building in buildings:
    owner[building] = Int(f'owner_{building}')
    # Domain: 0=RealProp, 1=Southco, 2=Trustcorp
    solver.add(owner[building] >= 0, owner[building] <= 2)

solver = Solver()

# Each building owned by exactly one company (already enforced by single variable per building)

# Count buildings per class per company
class_counts = {}
for company in companies:
    for cls in [1, 2, 3]:
        class_counts[(company, cls)] = Int(f'count_{company}_{cls}')

# Calculate class counts from ownership
for company_idx, company in enumerate(companies):
    for cls in [1, 2, 3]:
        # Count buildings of class cls owned by company
        count_expr = Sum([If(owner[building] == company_idx, 1, 0) for building in buildings if buildings[building] == cls])
        solver.add(class_counts[(company, cls)] == count_expr)

# Trade rules constraints:
# The key insight: trades preserve certain invariants. Let's think about what's possible.

# Initial class counts:
# RealProp: class1=1, class2=0, class3=2
# Southco: class1=1, class2=1, class3=0  
# Trustcorp: class1=0, class2=3, class3=0

# After trades, Trustcorp has no class2 buildings.
# So all class2 buildings must be with RealProp or Southco.

# Let's think about what trades can happen:
# 1. Same class trade: doesn't change class counts
# 2. Class1 -> 2 class2: decreases class1 by 1, increases class2 by 2
# 3. Class2 -> 2 class3: decreases class2 by 1, increases class3 by 2

# Since Trustcorp ends with 0 class2, and initially has 3 class2, it must trade away all 3 class2 buildings.
# Each class2 building can be traded via rule 1 (same class) or rule 3 (to 2 class3).

# If Trustcorp trades a class2 building via rule 3, it gets 2 class3 buildings.
# If via rule 1, it gets another class2 building (but then it still has class2, which contradicts final state).

# So Trustcorp must trade all 3 class2 buildings via rule 3, getting 6 class3 buildings in return.
# But wait, Trustcorp initially has 0 class3 buildings. After 3 trades of rule 3, it would have 6 class3 buildings.

# However, the problem doesn't say Trustcorp can't have class3 buildings. It only says no class2 buildings.

# Let's check the answer choices by seeing what must be true in all valid final states.

# First, let's add the constraint that Trustcorp has no class2 buildings
solver.add(class_counts[('Trustcorp', 2)] == 0)

# Now, we need to ensure the final state is reachable via trades.
# This is complex. Instead, I'll use a simpler approach: enumerate all possible final distributions
# that satisfy the class count constraints and see which statements are always true.

# But wait, we also need to ensure the total number of buildings per class is preserved (except for trades that change classes).
# Actually, trades change class counts! Let's track total class counts.

# Initial total class counts:
# Class1: 2 (Garza, Flores)
# Class2: 4 (Lynch, King, Meyer, Ortiz)
# Class3: 2 (Yates, Zimmer)

# After trades, the total class counts can change due to rules 2 and 3.
# Let's denote:
# Let x = number of times rule 2 is applied (class1 -> 2 class2)
# Let y = number of times rule 3 is applied (class2 -> 2 class3)

# Then final class counts:
# Class1: 2 - x
# Class2: 4 + 2x - y
# Class3: 2 + 2y

# Since Trustcorp has 0 class2 buildings, all class2 buildings (4 + 2x - y) must be with RealProp or Southco.

# Also, each building is owned by exactly one company.

# Let's add constraints for total class counts:
total_class1 = Sum([If(buildings[building] == 1, 1, 0) for building in buildings])
total_class2 = Sum([If(buildings[building] == 2, 1, 0) for building in buildings])
total_class3 = Sum([If(buildings[building] == 3, 1, 0) for building in buildings])

# But wait, the buildings' classes don't change! The buildings themselves have fixed classes.
# The trade rules change which company owns which building, but the building's class is fixed.
# So the total class counts are fixed: 2 class1, 4 class2, 2 class3.

# This means rule 2 and 3 cannot be applied because they would change the total class counts.
# But the problem says trades happen according to these rules. How is this possible?

# Re-reading: "Each trade must be of exactly one of the following three kinds"
# This means when two companies trade, they must follow one of these rules.
# But the buildings themselves have fixed classes. So how can a class1 building become two class2 buildings?
# This suggests that when trading a class1 building for two class2 buildings, the class1 building changes class?
# Or perhaps the trade involves transferring ownership of buildings, and the "class" refers to the value category,
# which might change after trade? But the problem says "each building they own is categorized as either class 1, 2, or 3"
# and lists buildings with their classes. So classes seem fixed.

# This is confusing. Let me re-read: "Trading one class 1 building for two class 2 buildings"
# This could mean: Company A gives a class1 building to Company B, and Company B gives two class2 buildings to Company A.
# The buildings' classes don't change, just ownership.

# So the trade rules are about what can be exchanged, not about changing building classes.
# That makes more sense.

# So the total class counts per company can change, but total class counts overall are fixed.

# Given that, let's proceed with the constraint that Trustcorp has 0 class2 buildings.

# Now, let's check each answer choice.

# Answer choices:
# (A) RealProp owns a class 1 building.
# (B) Southco owns only class 2 buildings.
# (C) Southco has made at least one trade with Trustcorp.
# (D) Trustcorp owns the Garza Tower.
# (E) Trustcorp owns the Zimmer House.

# We need to check which of these must be true in all valid final states.

# Let's create a function to check each option.

# First, let's add more constraints to make the model more realistic.
# We need to ensure that the final ownership is reachable via trades.
# This is complex. Instead, I'll assume that any distribution of buildings
# that satisfies the class count constraints and the Trustcorp constraint is reachable.

# But we also need to consider that trades are between two companies.
# Each trade involves two companies exchanging buildings according to one of the rules.

# Given the complexity, I'll use a simpler approach: enumerate all possible final distributions
# of buildings to companies that satisfy:
# 1. Each building owned by exactly one company
# 2. Trustcorp has 0 class2 buildings
# 3. The total number of buildings per class is preserved (2 class1, 4 class2, 2 class3)

# Then check which statements are always true.

# Let's add the constraint that total class counts are preserved:
solver.add(total_class1 == 2)
solver.add(total_class2 == 4)
solver.add(total_class3 == 2)

# Now, let's check each answer choice by seeing if it's necessarily true.

# We'll use the multiple choice skeleton.

found_options = []

# Option A: RealProp owns a class 1 building.
# This means: exists a building of class 1 owned by RealProp
opt_a_constr = Or([owner[building] == 0 for building in buildings if buildings[building] == 1])

# Option B: Southco owns only class 2 buildings.
# This means: Southco owns no class 1 and no class 3 buildings
opt_b_constr = And(
    class_counts[('Southco', 1)] == 0,
    class_counts[('Southco', 3)] == 0
)

# Option C: Southco has made at least one trade with Trustcorp.
# This is about the process, not the final state. Hard to model directly.
# But if Southco and Trustcorp have exchanged buildings, then in the final state,
# at least one building that was initially owned by Southco is now owned by Trustcorp,
# or vice versa.
# Let's check if there's any building that changed hands between Southco and Trustcorp.
# Initially: Southco owned Flores Tower (1), Lynch Building (2)
# Trustcorp owned King, Meyer, Ortiz (all class2)
# If any of these buildings changed ownership between Southco and Trustcorp, then they traded.
# But we don't know the sequence. However, if in the final state, Southco owns a building
# that was initially Trustcorp's, or Trustcorp owns a building that was initially Southco's,
# then they must have traded (directly or indirectly).
# But the problem says "Southco has made at least one trade with Trustcorp" meaning direct trade.
# This is hard to model from final state alone.

# Given the complexity, I'll assume that if in the final state, Southco and Trustcorp
# have exchanged buildings (i.e., Southco owns a building that was initially Trustcorp's,
# or Trustcorp owns a building that was initially Southco's), then they must have traded.
# But this might not be strictly true if there are multi-party trades.

# For simplicity, I'll model option C as: there exists a building that was initially owned by Southco
# and is now owned by Trustcorp, OR a building initially owned by Trustcorp and now owned by Southco.
opt_c_constr = Or(
    # Southco now owns a building that was initially Trustcorp's
    Or([owner[building] == 1 for building in buildings if initial_owner[building] == 'Trustcorp']),
    # Trustcorp now owns a building that was initially Southco's
    Or([owner[building] == 2 for building in buildings if initial_owner[building] == 'Southco'])
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