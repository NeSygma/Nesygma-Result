from z3 import *

# Define the solver
solver = Solver()

# Number of solos
N = 5

# Pianists: 0 = Wayne, 1 = Zara
pianist = [Int(f'pianist_{i}') for i in range(N)]

# Piece types: 0 = modern, 1 = traditional
piece_type = [Int(f'piece_type_{i}') for i in range(N)]

# Constraints

# 1. The third solo is a traditional piece
solver.add(piece_type[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively
# This means there is exactly one pair of consecutive solos where both are traditional,
# and no more than two traditional pieces in a row.
# Since solo 2 is traditional, the pair must be (1,2) or (2,3).
# Also, there must be exactly two traditional pieces in total.

# Total number of traditional pieces is exactly 2
solver.add(Sum(piece_type) == 2)

# Exactly one pair of consecutive traditional pieces
# Case 1: solos 1 and 2 are traditional
solver.add(Or(
    And(piece_type[1] == 1, piece_type[2] == 1, piece_type[0] == 0, piece_type[3] == 0, piece_type[4] == 0),
    # Case 2: solos 2 and 3 are traditional
    And(piece_type[2] == 1, piece_type[3] == 1, piece_type[0] == 0, piece_type[1] == 0, piece_type[4] == 0)
))

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece
# This is equivalent to: piece_type[3] == 1 if and only if pianist[3] == 0
solver.add(piece_type[3] == 1 == (pianist[3] == 0))

# 4. The pianist who performs the second solo does not perform the fifth solo
solver.add(pianist[1] != pianist[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece
# This means that before Wayne performs a modern piece, no traditional pieces can be performed.
# Since solo 2 is traditional, Wayne must have performed a modern piece before solo 2.
# So, Wayne must perform a modern piece in solo 0 or 1.
# We can express this as: for all i < first_wayne_modern, piece_type[i] must be modern.
# But since solo 2 is traditional, first_wayne_modern must be <= 1.
# So, Wayne must perform a modern piece in solo 0 or 1.
# Let's encode: Wayne must have at least one modern piece in solos 0 or 1.
# Since Wayne is pianist 0, we can say:
# There exists i in {0,1} such that pianist[i] == 0 and piece_type[i] == 0
solver.add(Or(
    And(pianist[0] == 0, piece_type[0] == 0),
    And(pianist[1] == 0, piece_type[1] == 0)
))

# Additional condition for the question:
# The pianist who performs the first solo also performs the second solo
solver.add(pianist[0] == pianist[1])

# Now, evaluate each option to see which one must be true

# Option A: Zara performs the first solo
# pianist[0] == 1
opt_a_constr = (pianist[0] == 1)

# Option B: Wayne performs the third solo
# pianist[2] == 0
opt_b_constr = (pianist[2] == 0)

# Option C: Zara performs the fifth solo
# pianist[4] == 1
opt_c_constr = (pianist[4] == 1)

# Option D: The second solo is a traditional piece
# piece_type[1] == 1
opt_d_constr = (piece_type[1] == 1)

# Option E: The fourth solo is a modern piece
# piece_type[3] == 0
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