from z3 import *

solver = Solver()

# Variables: for each solo (1-5), which pianist and which type
# pianist[i] = 0 for Wayne, 1 for Zara
# piece[i] = 0 for modern, 1 for traditional
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]
piece = [Int(f'piece_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Constraint 1: The third solo is a traditional piece.
solver.add(piece[2] == 1)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive solos that are both traditional,
# and no other consecutive pair is both traditional.
# Count consecutive traditional pairs
consec_trad = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(ct, 1, 0) for ct in consec_trad]) == 1)

# Constraint 3: In the fourth solo, either Wayne performs a traditional piece
# or Zara performs a modern piece.
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),  # Wayne traditional
    And(pianist[3] == 1, piece[3] == 0)   # Zara modern
))

# Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for any solo i that is traditional, there must exist some solo j < i
# where Wayne performs a modern piece.
# Equivalently: the first traditional piece must come after at least one Wayne-modern piece.
# Let's find the first traditional piece index (if any)
# For each solo i, if piece[i] == 1 (traditional), then there exists j < i with pianist[j]==0 and piece[j]==0
for i in range(5):
    # If solo i is traditional, then some earlier solo must be Wayne-modern
    earlier_wayne_modern = Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])
    if i == 0:
        # No earlier solos, so solo 0 cannot be traditional
        solver.add(piece[0] == 0)
    else:
        solver.add(Implies(piece[i] == 1, earlier_wayne_modern))

# Now we want to find the MINIMUM number of solos where Wayne performs a traditional piece.
# Wayne traditional count = sum of If(pianist[i]==0 AND piece[i]==1, 1, 0)
wayne_trad_count = Sum([If(And(pianist[i] == 0, piece[i] == 1), 1, 0) for i in range(5)])

# Test each option: can we achieve that count?
# (A) zero, (B) one, (C) two, (D) three, (E) four
options = [
    ("A", wayne_trad_count == 0),
    ("B", wayne_trad_count == 1),
    ("C", wayne_trad_count == 2),
    ("D", wayne_trad_count == 3),
    ("E", wayne_trad_count == 4),
]

found_options = []
for letter, constr in options:
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