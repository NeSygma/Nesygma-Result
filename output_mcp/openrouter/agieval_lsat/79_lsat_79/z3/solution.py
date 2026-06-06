from z3 import *

solver = Solver()
# Variables for positions 1..7
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R1 = Int('pos_R1')
pos_R2 = Int('pos_R2')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
pos_V = Int('pos_V')
positions = [pos_O, pos_P, pos_R1, pos_R2, pos_S, pos_T, pos_V]
# Domain constraints
for p in positions:
    solver.add(p >= 1, p <= 7)
# All distinct
solver.add(Distinct(positions))
# Base constraints
# Pharmacy at an end and a restaurant at the opposite end
end_constraint = Or(
    And(pos_P == 1, Or(pos_R1 == 7, pos_R2 == 7)),
    And(pos_P == 7, Or(pos_R1 == 1, pos_R2 == 1))
)
solver.add(end_constraint)
# Restaurants separated by at least two other businesses
solver.add(Abs(pos_R1 - pos_R2) >= 3)
# Pharmacy next to optometrist or veterinarian
solver.add(Or(Abs(pos_P - pos_O) == 1, Abs(pos_P - pos_V) == 1))
# Toy store not next to veterinarian
solver.add(Abs(pos_T - pos_V) != 1)
# Condition for the question: optometrist next to shoe store
solver.add(Abs(pos_O - pos_S) == 1)
# Determine leftmost and rightmost of the O-S pair
leftmost = If(pos_O < pos_S, pos_O, pos_S)
rightmost = leftmost + 1
# Ensure the pair is not at the ends so both neighbors exist
solver.add(leftmost >= 2, rightmost <= 6)
L = leftmost - 1
R = rightmost + 1
# Helper for restaurant at a position
def restaurant_at(pos):
    return Or(pos_R1 == pos, pos_R2 == pos)
# Option constraints
opt_a = Or(
    And(pos_P == L, restaurant_at(R)),
    And(pos_P == R, restaurant_at(L))
)
opt_b = Or(
    And(pos_P == L, pos_T == R),
    And(pos_P == R, pos_T == L)
)
opt_c = Or(
    And(pos_R1 == L, pos_R2 == R),
    And(pos_R1 == R, pos_R2 == L)
)
opt_d = Or(
    And(restaurant_at(L), pos_T == R),
    And(restaurant_at(R), pos_T == L)
)
opt_e = Or(
    And(restaurant_at(L), pos_V == R),
    And(restaurant_at(R), pos_V == L)
)
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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