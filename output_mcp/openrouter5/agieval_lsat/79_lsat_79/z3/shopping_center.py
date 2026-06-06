from z3 import *

solver = Solver()

# 7 spaces, numbered 0..6 (space 1..7)
# We'll assign each business to a space.
# Businesses: optometrist (O), pharmacy (P), restaurant1 (R1), restaurant2 (R2),
# shoe store (S), toy store (T), veterinarian (V)

businesses = ['O', 'P', 'R1', 'R2', 'S', 'T', 'V']
# Use integer variables for positions (0-indexed)
pos = {b: Int(f'pos_{b}') for b in businesses}

# Each position is between 0 and 6
for b in businesses:
    solver.add(pos[b] >= 0, pos[b] <= 6)

# All positions distinct
solver.add(Distinct([pos[b] for b in businesses]))

# Constraint 1: Pharmacy at one end, one of the restaurants at the other.
# Ends are 0 and 6.
solver.add(Or(pos['P'] == 0, pos['P'] == 6))
solver.add(Or(pos['R1'] == 0, pos['R1'] == 6, pos['R2'] == 0, pos['R2'] == 6))
# The pharmacy and the restaurant at the ends must be opposite ends.
# If P is at 0, then one restaurant is at 6. If P is at 6, then one restaurant is at 0.
solver.add(Or(
    And(pos['P'] == 0, Or(pos['R1'] == 6, pos['R2'] == 6)),
    And(pos['P'] == 6, Or(pos['R1'] == 0, pos['R2'] == 0))
))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# That means |pos[R1] - pos[R2]| >= 3 (since at least 2 businesses between means distance >= 3)
solver.add(Or(pos['R1'] - pos['R2'] >= 3, pos['R2'] - pos['R1'] >= 3))

# Constraint 3: Pharmacy next to either optometrist or veterinarian.
# "Next to" means |pos[P] - pos[X]| == 1
solver.add(Or(
    pos['P'] - pos['O'] == 1, pos['O'] - pos['P'] == 1,
    pos['P'] - pos['V'] == 1, pos['V'] - pos['P'] == 1
))

# Constraint 4: Toy store cannot be next to veterinarian.
# |pos[T] - pos[V]| != 1
solver.add(Not(Or(pos['T'] - pos['V'] == 1, pos['V'] - pos['T'] == 1)))

# Additional condition from the question: The optometrist is next to the shoe store.
# |pos[O] - pos[S]| == 1
solver.add(Or(pos['O'] - pos['S'] == 1, pos['S'] - pos['O'] == 1))

# Now we need to evaluate each answer choice.
# The question asks: "the businesses immediately on either side of this pair must be"
# "this pair" = the optometrist and shoe store pair (adjacent).
# So we need to find what businesses are on either side of the O-S pair.
# Since O and S are adjacent, they form a block of 2. The businesses immediately
# on either side are the ones at positions min(pos[O], pos[S]) - 1 and max(pos[O], pos[S]) + 1.
# But we need to check which answer choice is necessarily true (must be).

# Let's define helper: for a given model, find the left and right neighbors of the O-S pair.
# We'll encode each answer choice as a constraint and check if it's forced.

# Answer choices:
# A: the pharmacy and a restaurant
# B: the pharmacy and the toy store
# C: the two restaurants
# D: a restaurant and the toy store
# E: a restaurant and the veterinarian

# We need to find which option MUST be true. So we check if the option is forced.
# Approach: For each option, check if there exists a model where the option is FALSE.
# If no model exists where the option is false, then the option must be true.

# Let's define the neighbors. We'll use auxiliary variables.
left_neighbor = Int('left_neighbor')
right_neighbor = Int('right_neighbor')

# The O-S pair: let's find which is left and which is right.
# left_pos = min(pos[O], pos[S]), right_pos = max(pos[O], pos[S])
# They are adjacent, so right_pos = left_pos + 1.
left_pos = Int('left_pos')
right_pos = Int('right_pos')
solver.add(left_pos == If(pos['O'] < pos['S'], pos['O'], pos['S']))
solver.add(right_pos == If(pos['O'] < pos['S'], pos['S'], pos['O']))
solver.add(right_pos == left_pos + 1)  # they are adjacent

# left_neighbor is at left_pos - 1, right_neighbor is at right_pos + 1
# But these might be out of bounds (if the pair is at an end).
# The question says "businesses immediately on either side" - if the pair is at an end,
# there's only one side. But the phrasing implies both sides exist.
# Let's add that the pair is not at an end (both sides exist).
solver.add(left_pos > 0)
solver.add(right_pos < 6)

# Now left_neighbor and right_neighbor are the businesses at those positions.
# We need to map position to business.
# For each business b, if pos[b] == left_pos - 1, then left_neighbor = b (encoded as int)
# Let's encode businesses as integers: O=0, P=1, R1=2, R2=3, S=4, T=5, V=6
business_to_int = {'O': 0, 'P': 1, 'R1': 2, 'R2': 3, 'S': 4, 'T': 5, 'V': 6}
int_to_business = {0: 'O', 1: 'P', 2: 'R1', 3: 'R2', 4: 'S', 5: 'T', 6: 'V'}

# left_neighbor is the business at position left_pos - 1
for b, idx in business_to_int.items():
    solver.add(Implies(pos[b] == left_pos - 1, left_neighbor == idx))

# right_neighbor is the business at position right_pos + 1
for b, idx in business_to_int.items():
    solver.add(Implies(pos[b] == right_pos + 1, right_neighbor == idx))

# Now let's check each answer choice.
# Each choice specifies what the two neighbors are (order doesn't matter for the pair).
# We'll check if the option is forced.

# For each option, we'll check if there's a model where the option is FALSE.
# If unsat for the negated option, then the option is forced.

# But first, let's get a model to see what's happening.
solver.push()
result = solver.check()
if result == sat:
    m = solver.model()
    print("Sample model:")
    for b in businesses:
        print(f"  {b}: space {m[pos[b]]}")
    print(f"  left_pos: {m[left_pos]}, right_pos: {m[right_pos]}")
    print(f"  left_neighbor: {m[left_neighbor]}, right_neighbor: {m[right_neighbor]}")
    print(f"  left_neighbor business: {int_to_business[m[left_neighbor].as_long()]}")
    print(f"  right_neighbor business: {int_to_business[m[right_neighbor].as_long()]}")
solver.pop()

# Now check each option.
# For each option, we need to encode what the two neighbors are.
# The option says the businesses on either side are X and Y (order doesn't matter).

# Let's define a helper: a set of two businesses (as ints) that the neighbors must match.
# We'll check if the option is forced by checking if there's a model where the neighbors
# are NOT exactly those two businesses.

options = {
    "A": {business_to_int['P'], business_to_int['R1']},  # pharmacy and a restaurant (R1 or R2)
    "B": {business_to_int['P'], business_to_int['T']},    # pharmacy and toy store
    "C": {business_to_int['R1'], business_to_int['R2']},  # two restaurants
    "D": {business_to_int['R1'], business_to_int['T']},   # a restaurant and toy store
    "E": {business_to_int['R1'], business_to_int['V']},   # a restaurant and veterinarian
}

# For options with "a restaurant", we need to check if either R1 or R2 works.
# Let's redefine more carefully.

# Option A: pharmacy and a restaurant -> {P, R1} or {P, R2}
# Option B: pharmacy and toy store -> {P, T}
# Option C: two restaurants -> {R1, R2}
# Option D: a restaurant and toy store -> {R1, T} or {R2, T}
# Option E: a restaurant and veterinarian -> {R1, V} or {R2, V}

# Let's check each option by seeing if it's forced.
# We'll check: is there a model where the neighbors are NOT the specified pair?
# If no such model exists, the option is forced.

found_options = []

for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    # Add constraint that the option is FALSE
    # i.e., the set {left_neighbor, right_neighbor} is NOT the specified pair
    
    if letter == "A":
        # Not (pharmacy and a restaurant)
        # The neighbors are {P, R1} or {P, R2}
        solver.add(Not(Or(
            And(Or(left_neighbor == 1, right_neighbor == 1), Or(left_neighbor == 2, right_neighbor == 2)),
            And(Or(left_neighbor == 1, right_neighbor == 1), Or(left_neighbor == 3, right_neighbor == 3))
        )))
    elif letter == "B":
        # Not (pharmacy and toy store)
        solver.add(Not(And(
            Or(left_neighbor == 1, right_neighbor == 1),
            Or(left_neighbor == 5, right_neighbor == 5)
        )))
    elif letter == "C":
        # Not (two restaurants)
        solver.add(Not(And(
            Or(left_neighbor == 2, right_neighbor == 2),
            Or(left_neighbor == 3, right_neighbor == 3)
        )))
    elif letter == "D":
        # Not (a restaurant and toy store)
        solver.add(Not(Or(
            And(Or(left_neighbor == 2, right_neighbor == 2), Or(left_neighbor == 5, right_neighbor == 5)),
            And(Or(left_neighbor == 3, right_neighbor == 3), Or(left_neighbor == 5, right_neighbor == 5))
        )))
    elif letter == "E":
        # Not (a restaurant and veterinarian)
        solver.add(Not(Or(
            And(Or(left_neighbor == 2, right_neighbor == 2), Or(left_neighbor == 6, right_neighbor == 6)),
            And(Or(left_neighbor == 3, right_neighbor == 3), Or(left_neighbor == 6, right_neighbor == 6))
        )))
    
    if solver.check() == unsat:
        # No model where the option is false -> option is forced
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