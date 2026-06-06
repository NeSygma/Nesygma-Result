from z3 import *

# Create solver
solver = Solver()

# Define positions 1-8
positions = [Int(f'pos_{i}') for i in range(1, 9)]  # pos_1 to pos_8

# Define compositions as integers for easier comparison
F, H, L, O, P, R, S, T = 0, 1, 2, 3, 4, 5, 6, 7

# Each position has exactly one composition, and each composition appears exactly once
compositions = [F, H, L, O, P, R, S, T]
for i in range(8):
    solver.add(positions[i] >= 0, positions[i] <= 7)
    
# All positions must be distinct (each composition appears exactly once)
solver.add(Distinct(positions))

# Helper function to get position of a composition
def get_pos(comp):
    # Returns the position (1-8) where composition 'comp' is performed
    # Using Or-loop pattern to avoid indexing with Z3 variables
    return If(positions[0] == comp, 1,
           If(positions[1] == comp, 2,
           If(positions[2] == comp, 3,
           If(positions[3] == comp, 4,
           If(positions[4] == comp, 5,
           If(positions[5] == comp, 6,
           If(positions[6] == comp, 7, 8)))))))

# Get positions for each composition
pos_F = get_pos(F)
pos_H = get_pos(H)
pos_L = get_pos(L)
pos_O = get_pos(O)
pos_P = get_pos(P)
pos_R = get_pos(R)
pos_S = get_pos(S)
pos_T = get_pos(T)

# Base constraints from problem statement

# 1. T is performed either immediately before F or immediately after R
solver.add(Or(
    pos_T == pos_F - 1,  # T immediately before F
    pos_T == pos_R + 1   # T immediately after R
))

# 2. At least two compositions are performed either after F and before R, or after R and before F
# This means the distance between F and R is at least 3 (positions differ by at least 3)
solver.add(Or(
    pos_F < pos_R - 2,  # At least 2 between F and R (F before R)
    pos_R < pos_F - 2   # At least 2 between R and F (R before F)
))

# 3. O is performed either first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))

# 4. The eighth composition is either L or H
solver.add(Or(positions[7] == L, positions[7] == H))

# 5. P is performed before S
solver.add(pos_P < pos_S)

# 6. At least one composition is performed either after O and before S, or after S and before O
# This means O and S are not adjacent (distance at least 2)
solver.add(Or(
    pos_O < pos_S - 1,  # At least one between O and S (O before S)
    pos_S < pos_O - 1   # At least one between S and O (S before O)
))

# Additional given constraints
# P is performed third
solver.add(pos_P == 3)

# S is performed sixth
solver.add(pos_S == 6)

# Now evaluate each answer choice
# The question asks: "the composition performed fifth must be either"
# We need to check which option is forced by the constraints

# Define the options as constraints on the fifth position
opt_a_constr = Or(positions[4] == F, positions[4] == H)  # F or H
opt_b_constr = Or(positions[4] == F, positions[4] == O)  # F or O
opt_c_constr = Or(positions[4] == F, positions[4] == T)  # F or T
opt_d_constr = Or(positions[4] == H, positions[4] == L)  # H or L
opt_e_constr = Or(positions[4] == O, positions[4] == R)  # O or R

found_options = []
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