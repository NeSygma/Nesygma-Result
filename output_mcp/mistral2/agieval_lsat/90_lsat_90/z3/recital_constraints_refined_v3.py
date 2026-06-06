from z3 import *

solver = Solver()

# Number of solos
N = 5

# Pianists: Wayne (0) or Zara (1)
pianist = [Int(f'pianist_{i}') for i in range(N)]

# Piece types: Modern (0) or Traditional (1)
piece_type = [Int(f'piece_type_{i}') for i in range(N)]

# Constraints

# 1. The third solo is a traditional piece.
solver.add(piece_type[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive traditional pieces, and no other traditional pieces are adjacent.
consecutive_traditional = []
for i in range(N - 1):
    consecutive_traditional.append(And(piece_type[i] == 1, piece_type[i+1] == 1))

# Exactly one pair of consecutive traditional pieces
solver.add(Sum([If(c, 1, 0) for c in consecutive_traditional]) == 1)

# Ensure no other traditional pieces are adjacent to the pair
for i in range(N - 2):
    solver.add(Not(And(piece_type[i] == 1, piece_type[i+1] == 1, piece_type[i+2] == 1)))

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1), And(pianist[3] == 1, piece_type[3] == 0)))

# 4. The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# This means that for any traditional piece at position i, there must be a modern piece by Wayne before i.
for i in range(N):
    if i > 0:
        solver.add(Implies(piece_type[i] == 1, Or(
            *[And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)]
        )))
    else:
        solver.add(piece_type[i] == 0)  # No traditional piece at position 0

# Additional constraint: The pianist who performs the first solo also performs the second solo.
solver.add(pianist[0] == pianist[1])

# Now, evaluate the multiple choice options

# Define the options as constraints
# (A) Zara performs the first solo.
opt_a_constr = (pianist[0] == 1)

# (B) Wayne performs the third solo.
opt_b_constr = (pianist[2] == 0)

# (C) Zara performs the fifth solo.
opt_c_constr = (pianist[4] == 1)

# (D) The second solo is a traditional piece.
opt_d_constr = (piece_type[1] == 1)

# (E) The fourth solo is a modern piece.
opt_e_constr = (piece_type[3] == 0)

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