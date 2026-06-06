from z3 import *

solver = Solver()

# Number of solos
N = 5

# Pianists: Wayne (W) or Zara (Z)
# We'll represent pianist assignments as a list of 0 (Wayne) and 1 (Zara)
pianist = [Int(f'pianist_{i}') for i in range(N)]

# Piece types: Modern (0) or Traditional (1)
# We'll represent piece types as a list of 0 (Modern) and 1 (Traditional)
piece_type = [Int(f'piece_type_{i}') for i in range(N)]

# Constraints

# 1. The third solo is a traditional piece.
solver.add(piece_type[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively.
# We need to find exactly one pair of consecutive traditional pieces.
consecutive_pairs = []
for i in range(N - 1):
    consecutive_pairs.append(And(piece_type[i] == 1, piece_type[i + 1] == 1))

# Exactly one pair of consecutive traditional pieces
solver.add(Sum([If(p, 1, 0) for p in consecutive_pairs]) == 1)

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
# Fourth solo is index 3 (0-based)
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),  # Wayne performs traditional
    And(pianist[3] == 1, piece_type[3] == 0)   # Zara performs modern
))

# 4. The pianist who performs the second solo does not perform the fifth solo.
# Second solo is index 1, fifth solo is index 4
solver.add(pianist[1] != pianist[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# This means that for all i, if piece_type[i] == 1, then there exists some j < i where pianist[j] == 0 and piece_type[j] == 0.
# We can encode this as: for each traditional piece, there is a Wayne modern piece before it.
for i in range(N):
    if i == 0:
        # First solo cannot be traditional (since no prior solo exists)
        solver.add(piece_type[0] == 0)
    else:
        # If this solo is traditional, there must be a Wayne modern piece before it
        solver.add(Implies(piece_type[i] == 1, 
                           Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])))

# Additional constraints for pianist assignments (0=Wayne, 1=Zara)
for i in range(N):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))

# Additional constraints for piece types (0=Modern, 1=Traditional)
for i in range(N):
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Hypothesis: In the fifth solo, Wayne performs a traditional piece.
# Fifth solo is index 4
solver.add(And(pianist[4] == 0, piece_type[4] == 1))

# Now, evaluate the multiple choice options
found_options = []

# Option A: Zara performs the first solo.
# First solo is index 0
solver.push()
solver.add(pianist[0] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Wayne performs the second solo.
# Second solo is index 1
solver.push()
solver.add(pianist[1] == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Zara performs the third solo.
# Third solo is index 2
solver.push()
solver.add(pianist[2] == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The second solo is a modern piece.
# Second solo is index 1
solver.push()
solver.add(piece_type[1] == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The fourth solo is a traditional piece.
# Fourth solo is index 3
solver.push()
solver.add(piece_type[3] == 1)
if solver.check() == sat:
    found_options.append("E")
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