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

# 2. Exactly two traditional pieces in total
solver.add(Sum(piece_type) == 2)

# 3. Exactly two traditional pieces are performed consecutively
# Given solo 2 is traditional, the only possible consecutive pairs are:
# - Solos 1 and 2
# - Solos 2 and 3
# So we must have either:
#   piece_type[1] == 1 and piece_type[2] == 1 and piece_type[0] == 0 and piece_type[3] == 0 and piece_type[4] == 0
#   OR
#   piece_type[2] == 1 and piece_type[3] == 1 and piece_type[0] == 0 and piece_type[1] == 0 and piece_type[4] == 0

solver.add(Or(
    And(piece_type[1] == 1, piece_type[2] == 1, piece_type[0] == 0, piece_type[3] == 0, piece_type[4] == 0),
    And(piece_type[2] == 1, piece_type[3] == 1, piece_type[0] == 0, piece_type[1] == 0, piece_type[4] == 0)
))

# 4. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece
# Equivalent to: piece_type[3] == 1 implies pianist[3] == 0, and pianist[3] == 1 implies piece_type[3] == 0
solver.add(Implies(piece_type[3] == 1, pianist[3] == 0))
solver.add(Implies(pianist[3] == 1, piece_type[3] == 0))

# 5. The pianist who performs the second solo does not perform the fifth solo
solver.add(pianist[1] != pianist[4])

# 6. No traditional piece is performed until Wayne performs at least one modern piece
# Since solo 2 is traditional, Wayne must have performed a modern piece in solo 0 or 1
solver.add(Or(
    And(pianist[0] == 0, piece_type[0] == 0),
    And(pianist[1] == 0, piece_type[1] == 0)
))

# 7. The pianist who performs the first solo also performs the second solo
solver.add(pianist[0] == pianist[1])

# Now, evaluate each option to see which one MUST be true
# For "must be true", we check if the negation of the option is unsatisfiable

# Option A: Zara performs the first solo
# pianist[0] == 1
opt_a = (pianist[0] == 1)

# Option B: Wayne performs the third solo
# pianist[2] == 0
opt_b = (pianist[2] == 0)

# Option C: Zara performs the fifth solo
# pianist[4] == 1
opt_c = (pianist[4] == 1)

# Option D: The second solo is a traditional piece
# piece_type[1] == 1
opt_d = (piece_type[1] == 1)

# Option E: The fourth solo is a modern piece
# piece_type[3] == 0
opt_e = (piece_type[3] == 0)

# List of options to check
options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
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