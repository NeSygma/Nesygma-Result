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
# Wayne must perform a modern piece in solo 0 or 1
solver.add(Or(
    And(pianist[0] == 0, piece_type[0] == 0),
    And(pianist[1] == 0, piece_type[1] == 0)
))

# Additional condition for the question:
# The pianist who performs the first solo also performs the second solo
solver.add(pianist[0] == pianist[1])

# Now, evaluate each option to see which one MUST be true
# For "must be true", we check if the negation of the option is unsatisfiable

# Option A: Zara performs the first solo
# pianist[0] == 1
# Negation: pianist[0] != 1
opt_a_must = (pianist[0] == 1)

# Option B: Wayne performs the third solo
# pianist[2] == 0
# Negation: pianist[2] != 0
opt_b_must = (pianist[2] == 0)

# Option C: Zara performs the fifth solo
# pianist[4] == 1
# Negation: pianist[4] != 1
opt_c_must = (pianist[4] == 1)

# Option D: The second solo is a traditional piece
# piece_type[1] == 1
# Negation: piece_type[1] != 1
opt_d_must = (piece_type[1] == 1)

# Option E: The fourth solo is a modern piece
# piece_type[3] == 0
# Negation: piece_type[3] != 0
opt_e_must = (piece_type[3] == 0)

# List of options to check
options = [
    ("A", opt_a_must),
    ("B", opt_b_must),
    ("C", opt_c_must),
    ("D", opt_d_must),
    ("E", opt_e_must)
]

must_be_true = []

for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        # The negation is unsatisfiable, so the option must be true
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")