from z3 import *

solver = Solver()

# There are 5 solos, indexed 0..4 (1st solo = index 0, 5th solo = index 4)
# For each solo i, we have:
#   pianist[i] = 0 for Wayne, 1 for Zara
#   piece[i] = 0 for modern, 1 for traditional

pianist = [Int(f'p_{i}') for i in range(5)]
piece = [Int(f'g_{i}') for i in range(5)]

for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive traditional pairs: for i=0..3, piece[i]==1 and piece[i+1]==1
consec_pairs = [If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(4)]
solver.add(Sum(consec_pairs) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
# Wayne performs traditional: pianist[3]==0 and piece[3]==1
# Zara performs modern: pianist[3]==1 and piece[3]==0
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for any solo i, if piece[i]==1 (traditional), then there exists some j < i
# such that pianist[j]==0 (Wayne) and piece[j]==0 (modern).
# Equivalent: For each i, if piece[i]==1, then Or over j < i of (pianist[j]==0 and piece[j]==0)
for i in range(5):
    if i == 0:
        # No solos before the first, so the first cannot be traditional
        solver.add(piece[0] != 1)
    else:
        # If piece[i] is traditional, then at least one earlier solo has Wayne playing modern
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Additional condition from the question: In the fifth solo (index 4), Wayne performs a traditional piece.
solver.add(pianist[4] == 0)
solver.add(piece[4] == 1)

# Now evaluate each option
# Option A: Zara performs the first solo. pianist[0] == 1
opt_a = (pianist[0] == 1)

# Option B: Wayne performs the second solo. pianist[1] == 0
opt_b = (pianist[1] == 0)

# Option C: Zara performs the third solo. pianist[2] == 1
opt_c = (pianist[2] == 1)

# Option D: The second solo is a modern piece. piece[1] == 0
opt_d = (piece[1] == 0)

# Option E: The fourth solo is a traditional piece. piece[3] == 1
opt_e = (piece[3] == 1)

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