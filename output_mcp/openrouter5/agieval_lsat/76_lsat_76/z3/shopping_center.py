from z3 import *

# Seven spaces 1-7
# Businesses: optometrist (O), pharmacy (P), two restaurants (R1, R2), shoe store (S), toy store (T), veterinarian (V)
# We'll assign each space a business type.
# Since there are two restaurants, we need to distinguish them or just use a count.
# Let's use integer variables for each space: 0=optometrist, 1=pharmacy, 2=restaurant, 3=shoe store, 4=toy store, 5=veterinarian
# But we have TWO restaurants. So we need to ensure exactly two spaces have value 2.

# Better: use an enum-like approach with Ints.
# Let's define: 0=optometrist, 1=pharmacy, 2=restaurant, 3=shoe store, 4=toy store, 5=veterinarian
# Constraint: exactly two restaurants (value 2).

spaces = [Int(f'space_{i}') for i in range(1, 8)]  # spaces 1..7

solver = Solver()

# Domain: each space is one of the 6 business types
for s in spaces:
    solver.add(And(s >= 0, s <= 5))

# Exactly one of each type except restaurant which has two
# Count each type
for t in range(6):
    if t == 2:  # restaurant
        solver.add(Sum([If(s == t, 1, 0) for s in spaces]) == 2)
    else:
        solver.add(Sum([If(s == t, 1, 0) for s in spaces]) == 1)

# Constraint 1: The pharmacy (1) must be at one end of the row and one of the restaurants (2) at the other.
solver.add(Or(
    And(spaces[0] == 1, spaces[6] == 2),
    And(spaces[0] == 2, spaces[6] == 1)
))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# Find positions of the two restaurants and ensure |pos1 - pos2| >= 3
# We'll use an Or-loop pattern to enforce this.
# Let r1_pos, r2_pos be the positions (0-indexed) of the two restaurants.
# We can encode: there exist i, j such that spaces[i]==2, spaces[j]==2, i<j, and j-i >= 3
# Using a disjunction over all pairs.
pair_constraints = []
for i in range(7):
    for j in range(i+1, 7):
        pair_constraints.append(And(spaces[i] == 2, spaces[j] == 2, j - i >= 3))
solver.add(Or(pair_constraints))

# Constraint 3: The pharmacy must be next to either the optometrist or the veterinarian.
# Pharmacy is at position p (0-indexed). It must have neighbor (p-1 or p+1) that is optometrist (0) or veterinarian (5).
pharmacy_pos_constraints = []
for p in range(7):
    neighbor_conds = []
    if p > 0:
        neighbor_conds.append(Or(spaces[p-1] == 0, spaces[p-1] == 5))
    if p < 6:
        neighbor_conds.append(Or(spaces[p+1] == 0, spaces[p+1] == 5))
    pharmacy_pos_constraints.append(And(spaces[p] == 1, Or(neighbor_conds)))
solver.add(Or(pharmacy_pos_constraints))

# Constraint 4: The toy store (4) cannot be next to the veterinarian (5).
# For every pair of adjacent spaces, they cannot be (4,5) or (5,4).
for i in range(6):
    solver.add(Not(Or(
        And(spaces[i] == 4, spaces[i+1] == 5),
        And(spaces[i] == 5, spaces[i+1] == 4)
    )))

# Now evaluate each option
# Each option is a sequence of 7 business names.
# Map: pharmacy->1, optometrist->0, shoe store->3, restaurant->2, veterinarian->5, toy store->4

def parse_option(seq):
    mapping = {
        "pharmacy": 1,
        "optometrist": 0,
        "shoe store": 3,
        "restaurant": 2,
        "veterinarian": 5,
        "toy store": 4
    }
    return [mapping[name] for name in seq]

options = {
    "A": ["pharmacy", "optometrist", "shoe store", "restaurant", "veterinarian", "toy store", "restaurant"],
    "B": ["pharmacy", "veterinarian", "optometrist", "shoe store", "restaurant", "toy store", "restaurant"],
    "C": ["restaurant", "shoe store", "veterinarian", "pharmacy", "optometrist", "toy store", "restaurant"],
    "D": ["restaurant", "toy store", "optometrist", "restaurant", "veterinarian", "shoe store", "pharmacy"],
    "E": ["restaurant", "optometrist", "toy store", "restaurant", "shoe store", "veterinarian", "pharmacy"]
}

found_options = []
for letter, seq in options.items():
    constr = [spaces[i] == val for i, val in enumerate(parse_option(seq))]
    solver.push()
    solver.add(And(constr))
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