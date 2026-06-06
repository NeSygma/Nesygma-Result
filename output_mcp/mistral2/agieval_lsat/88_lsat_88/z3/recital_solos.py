from z3 import *

solver = Solver()

# We have 5 solos, indexed 0 to 4 (0 = first solo, 4 = fifth solo)
# Each solo has two attributes:
# 1. Pianist: Wayne (0) or Zara (1)
# 2. Piece type: Modern (0) or Traditional (1)

# Declare variables
pianists = [Int(f'pianist_{i}') for i in range(5)]  # 0 = Wayne, 1 = Zara
piece_types = [Int(f'piece_type_{i}') for i in range(5)]  # 0 = Modern, 1 = Traditional

# Base constraints

# 1. The third solo is a traditional piece (piece_types[2] == 1)
solver.add(piece_types[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively
# We need to count the number of consecutive pairs of traditional pieces
consecutive_traditional = []
for i in range(4):
    consecutive_traditional.append(And(piece_types[i] == 1, piece_types[i+1] == 1))

# Exactly one pair of consecutive traditional pieces
solver.add(Sum(consecutive_traditional) == 1)

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece
# Fourth solo is index 3
solver.add(Or(And(pianists[3] == 0, piece_types[3] == 1),  # Wayne performs traditional
              And(pianists[3] == 1, piece_types[3] == 0)))  # Zara performs modern

# 4. The pianist who performs the second solo does not perform the fifth solo
# Second solo is index 1, fifth solo is index 4
solver.add(pianists[1] != pianists[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece
# This means that for all i, if piece_types[i] == 1, then there exists some j < i where pianists[j] == 0 and piece_types[j] == 0
for i in range(5):
    if i == 0:
        solver.add(Implies(piece_types[i] == 1, False))  # No traditional piece in first solo
    else:
        solver.add(Implies(piece_types[i] == 1, 
                           Or([And(pianists[j] == 0, piece_types[j] == 0) for j in range(i)])))

# Now, evaluate the multiple choice options
# We need to check which of the options for traditional pieces is possible

# Define the options as constraints on piece_types
# A: first, third, and fourth are traditional
opt_a_constr = And(piece_types[0] == 1, piece_types[2] == 1, piece_types[3] == 1, 
                   piece_types[1] == 0, piece_types[4] == 0)

# B: second, third, and fourth are traditional
opt_b_constr = And(piece_types[1] == 1, piece_types[2] == 1, piece_types[3] == 1, 
                   piece_types[0] == 0, piece_types[4] == 0)

# C: third and fourth are traditional
opt_c_constr = And(piece_types[2] == 1, piece_types[3] == 1, 
                   piece_types[0] == 0, piece_types[1] == 0, piece_types[4] == 0)

# D: third and fifth are traditional
opt_d_constr = And(piece_types[2] == 1, piece_types[4] == 1, 
                   piece_types[0] == 0, piece_types[1] == 0, piece_types[3] == 0)

# E: fourth and fifth are traditional
opt_e_constr = And(piece_types[3] == 1, piece_types[4] == 1, 
                   piece_types[0] == 0, piece_types[1] == 0, piece_types[2] == 0)

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