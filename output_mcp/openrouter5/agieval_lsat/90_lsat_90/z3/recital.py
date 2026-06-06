from z3 import *

solver = Solver()

# There are 5 solos, indexed 0..4 (1st solo = index 0, etc.)
# For each solo i, we have:
#   pianist[i] = 0 for Wayne, 1 for Zara
#   piece[i] = 0 for modern, 1 for traditional

pianist = [Int(f'p_{i}') for i in range(5)]
piece = [Int(f'pc_{i}') for i in range(5)]

for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive pairs of traditional pieces.
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
# Wayne performs traditional: pianist[3]==0 AND piece[3]==1
# Zara performs modern: pianist[3]==1 AND piece[3]==0
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# That means: for any solo i that is traditional, there must exist some j < i where Wayne performs a modern piece.
# Equivalently: if piece[i]==1, then there exists j < i with pianist[j]==0 and piece[j]==0.
for i in range(5):
    if i == 0:
        # First solo cannot be traditional because no earlier solo for Wayne to play modern.
        solver.add(piece[0] != 1)
    else:
        # If piece[i]==1, then at least one earlier solo j has pianist[j]==0 and piece[j]==0.
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Additional condition from the question: The pianist who performs the first solo also performs the second solo.
solver.add(pianist[0] == pianist[1])

# Now evaluate each option.

# Option A: Zara performs the first solo. (pianist[0] == 1)
opt_a = (pianist[0] == 1)

# Option B: Wayne performs the third solo. (pianist[2] == 0)
opt_b = (pianist[2] == 0)

# Option C: Zara performs the fifth solo. (pianist[4] == 1)
opt_c = (pianist[4] == 1)

# Option D: The second solo is a traditional piece. (piece[1] == 1)
opt_d = (piece[1] == 1)

# Option E: The fourth solo is a modern piece. (piece[3] == 0)
opt_e = (piece[3] == 0)

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