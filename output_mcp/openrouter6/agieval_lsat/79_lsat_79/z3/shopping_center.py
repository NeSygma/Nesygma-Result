from z3 import *

solver = Solver()

pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R1 = Int('pos_R1')
pos_R2 = Int('pos_R2')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
pos_V = Int('pos_V')

# All positions between 1 and 7
solver.add(pos_O >= 1, pos_O <= 7)
solver.add(pos_P >= 1, pos_P <= 7)
solver.add(pos_R1 >= 1, pos_R1 <= 7)
solver.add(pos_R2 >= 1, pos_R2 <= 7)
solver.add(pos_S >= 1, pos_S <= 7)
solver.add(pos_T >= 1, pos_T <= 7)
solver.add(pos_V >= 1, pos_V <= 7)

# All distinct
solver.add(Distinct([pos_O, pos_P, pos_R1, pos_R2, pos_S, pos_T, pos_V]))

# Constraint 1: Pharmacy at one end
solver.add(Or(pos_P == 1, pos_P == 7))

# Constraint 2: One restaurant at the other end
solver.add(Or(
    And(pos_P == 1, Or(pos_R1 == 7, pos_R2 == 7)),
    And(pos_P == 7, Or(pos_R1 == 1, pos_R2 == 1))
))

# Constraint 3: Two restaurants separated by at least two other businesses
solver.add(Abs(pos_R1 - pos_R2) >= 3)

# Constraint 4: Pharmacy next to optometrist or veterinarian
solver.add(Or(
    pos_P == pos_O + 1,
    pos_P == pos_O - 1,
    pos_P == pos_V + 1,
    pos_P == pos_V - 1
))

# Constraint 5: Toy store not next to veterinarian
solver.add(Not(Or(
    pos_T == pos_V + 1,
    pos_T == pos_V - 1
)))

# O-S adjacency condition
os_adjacent = Or(pos_O == pos_S + 1, pos_O == pos_S - 1)

# Interior pair condition (so that there are two sides)
min_pos = If(pos_O < pos_S, pos_O, pos_S)
max_pos = If(pos_O > pos_S, pos_O, pos_S)
interior_pair = And(min_pos >= 2, max_pos <= 6)

# Positions of the sides
left = min_pos - 1
right = max_pos + 1

# Option A: pharmacy and a restaurant
opt_a_constr = Or(
    And(pos_P == left, Or(pos_R1 == right, pos_R2 == right)),
    And(pos_P == right, Or(pos_R1 == left, pos_R2 == left))
)

# Option B: pharmacy and toy store
opt_b_constr = Or(
    And(pos_P == left, pos_T == right),
    And(pos_P == right, pos_T == left)
)

# Option C: two restaurants
opt_c_constr = Or(
    And(pos_R1 == left, pos_R2 == right),
    And(pos_R1 == right, pos_R2 == left)
)

# Option D: a restaurant and toy store
opt_d_constr = Or(
    And(Or(pos_R1 == left, pos_R2 == left), pos_T == right),
    And(Or(pos_R1 == right, pos_R2 == right), pos_T == left)
)

# Option E: a restaurant and veterinarian
opt_e_constr = Or(
    And(Or(pos_R1 == left, pos_R2 == left), pos_V == right),
    And(Or(pos_R1 == right, pos_R2 == right), pos_V == left)
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(os_adjacent)
    solver.add(interior_pair)
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