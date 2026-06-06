from z3 import *

solver = Solver()

# There are 5 solos, indexed 0..4 (1st solo = index 0, etc.)
# For each solo i, we have:
#   pianist[i] = 0 for Wayne, 1 for Zara
#   piece[i]   = 0 for modern, 1 for traditional

pianist = [Int(f'p_{i}') for i in range(5)]
piece   = [Int(f'g_{i}') for i in range(5)]

# Domains
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive traditional pairs (i,i+1) where both are traditional.
# We need exactly one such pair (since "exactly two ... consecutively" means
# there is exactly one pair of consecutive traditional pieces).
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
# (pianist[3] == 0 AND piece[3] == 1) OR (pianist[3] == 1 AND piece[3] == 0)
solver.add(Or(And(pianist[3] == 0, piece[3] == 1),
              And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# That means: for any solo i that is traditional, there must exist some solo j < i
# where Wayne performs a modern piece (pianist[j]==0 and piece[j]==0).
# Equivalently: if piece[i]==1, then there exists j < i with pianist[j]==0 and piece[j]==0.
# We encode this as: for each i, if piece[i]==1 then Or over j < i of (pianist[j]==0, piece[j]==0).
for i in range(5):
    # If piece[i] is traditional, then at least one earlier solo has Wayne + modern
    if i == 0:
        # First solo cannot be traditional because no earlier solo for Wayne's modern
        solver.add(piece[0] == 0)
    else:
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Now we need to find the minimum number of solos in which Wayne performs a traditional piece.
# Let's define a variable for the count of Wayne's traditional solos.
# We'll test each possible count (0 through 5) to see which is feasible.

# We'll use the multiple choice skeleton.
# Options:
# A: zero  -> count == 0
# B: one   -> count == 1
# C: two   -> count == 2
# D: three -> count == 3
# E: four  -> count == 4

# Count Wayne's traditional solos
wayne_trad_count = Sum([If(And(pianist[i] == 0, piece[i] == 1), 1, 0) for i in range(5)])

found_options = []
for letter, constr in [("A", wayne_trad_count == 0),
                       ("B", wayne_trad_count == 1),
                       ("C", wayne_trad_count == 2),
                       ("D", wayne_trad_count == 3),
                       ("E", wayne_trad_count == 4)]:
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