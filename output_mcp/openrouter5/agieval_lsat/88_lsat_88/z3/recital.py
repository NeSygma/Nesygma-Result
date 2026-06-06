from z3 import *

solver = Solver()

# There are 5 solos, indexed 0..4 (1st=0, 2nd=1, 3rd=2, 4th=3, 5th=4)
# For each solo i, we have:
#   pianist[i] = 0 for Wayne, 1 for Zara
#   piece[i]   = 0 for modern, 1 for traditional

pianist = [Int(f'p_{i}') for i in range(5)]
piece   = [Int(f'c_{i}') for i in range(5)]

for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive pairs (i,i+1) where both are traditional.
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
# (pianist[3]==0 AND piece[3]==1) OR (pianist[3]==1 AND piece[3]==0)
solver.add(Or(And(pianist[3] == 0, piece[3] == 1),
              And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# That means: for any solo i that is traditional, there must exist some j < i such that
# pianist[j]==0 and piece[j]==0.
# Equivalent: If piece[i]==1, then there exists j < i with pianist[j]==0 and piece[j]==0.
for i in range(5):
    if i == 0:
        # First solo cannot be traditional because no earlier solo exists for Wayne to play modern.
        solver.add(piece[i] == 0)
    else:
        # piece[i]==1 implies Or over j < i of (pianist[j]==0 and piece[j]==0)
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Now evaluate each option.
# Each option gives a set of solo indices (0-indexed) that are traditional.
# We need to check if there exists a valid assignment where exactly those solos are traditional
# (and the rest are modern).

options = {
    "A": [0, 2, 3],  # first(0), third(2), fourth(3)
    "B": [1, 2, 3],  # second(1), third(2), fourth(3)
    "C": [2, 3],     # third(2), fourth(3)
    "D": [2, 4],     # third(2), fifth(4)
    "E": [3, 4]      # fourth(3), fifth(4)
}

found_options = []
for letter, trad_indices in options.items():
    solver.push()
    # For each solo i, if i is in trad_indices, piece[i]==1; else piece[i]==0
    for i in range(5):
        if i in trad_indices:
            solver.add(piece[i] == 1)
        else:
            solver.add(piece[i] == 0)
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