from z3 import *

solver = Solver()

# Positions for each business (1-7)
O = Int('O')  # optometrist
P = Int('P')  # pharmacy
R1 = Int('R1')  # first restaurant
R2 = Int('R2')  # second restaurant
S = Int('S')  # shoe store
T = Int('T')  # toy store
V = Int('V')  # veterinarian

# All positions must be between 1 and 7
solver.add(And(1 <= O, O <= 7))
solver.add(And(1 <= P, P <= 7))
solver.add(And(1 <= R1, R1 <= 7))
solver.add(And(1 <= R2, R2 <= 7))
solver.add(And(1 <= S, S <= 7))
solver.add(And(1 <= T, T <= 7))
solver.add(And(1 <= V, V <= 7))

# All positions must be distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Constraint 1: Pharmacy at one end
solver.add(Or(P == 1, P == 7))

# Constraint 2: One restaurant at the other end
# If P == 1, then one restaurant must be at 7
# If P == 7, then one restaurant must be at 1
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 3: Two restaurants separated by at least two other businesses
# Distance between R1 and R2 must be at least 3
solver.add(Or(
    R1 >= R2 + 3,
    R2 >= R1 + 3
))

# Constraint 4: Pharmacy next to either optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 5: Toy store cannot be next to veterinarian
solver.add(Abs(T - V) != 1)

# Additional condition: Optometrist is next to shoe store
solver.add(Abs(O - S) == 1)

# Now we need to find what's on either side of the O-S pair
# The pair occupies two consecutive positions
# We need to find the positions immediately before and after this pair

# Let's define the left and right neighbors of the O-S pair
# First, determine which of O or S is leftmost
left_of_pair = If(O < S, O, S)
right_of_pair = If(O > S, O, S)

# The positions immediately before and after the pair
left_neighbor = left_of_pair - 1
right_neighbor = right_of_pair + 1

# These neighbors must be valid positions (1-7)
solver.add(And(left_neighbor >= 1, left_neighbor <= 7))
solver.add(And(right_neighbor >= 1, right_neighbor <= 7))

# Now we need to check which businesses occupy these neighbor positions
# We'll test each option

# Option A: the pharmacy and a restaurant
opt_a_constr = Or(
    And(left_neighbor == P, Or(right_neighbor == R1, right_neighbor == R2)),
    And(right_neighbor == P, Or(left_neighbor == R1, left_neighbor == R2))
)

# Option B: the pharmacy and the toy store
opt_b_constr = Or(
    And(left_neighbor == P, right_neighbor == T),
    And(right_neighbor == P, left_neighbor == T)
)

# Option C: the two restaurants
opt_c_constr = Or(
    And(left_neighbor == R1, right_neighbor == R2),
    And(left_neighbor == R2, right_neighbor == R1)
)

# Option D: a restaurant and the toy store
opt_d_constr = Or(
    And(left_neighbor == T, Or(right_neighbor == R1, right_neighbor == R2)),
    And(right_neighbor == T, Or(left_neighbor == R1, left_neighbor == R2))
)

# Option E: a restaurant and the veterinarian
opt_e_constr = Or(
    And(left_neighbor == V, Or(right_neighbor == R1, right_neighbor == R2)),
    And(right_neighbor == V, Or(left_neighbor == R1, left_neighbor == R2))
)

# Test each option
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