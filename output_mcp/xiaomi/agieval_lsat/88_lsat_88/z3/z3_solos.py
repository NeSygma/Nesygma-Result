from z3 import *

solver = Solver()

# Variables: for each solo (1-5), which pianist and which type
# pianist: 0 = Wayne, 1 = Zara
# piece_type: 0 = modern, 1 = traditional

pianist = [Int(f'pianist_{i}') for i in range(1, 6)]
piece = [Int(f'piece_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# This means there exists exactly one pair of consecutive solos that are both traditional,
# and no other traditional pieces are adjacent to them.
# We need to enumerate all possible sets of traditional pieces and check which have exactly
# one consecutive pair.

# Count consecutive traditional pairs
consecutive_pairs = []
for i in range(4):
    consecutive_pairs.append(And(piece[i] == 1, piece[i+1] == 1))

# Exactly one consecutive pair
solver.add(Sum([If(cp, 1, 0) for cp in consecutive_pairs]) == 1)

# Condition 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),  # Wayne performs traditional
    And(pianist[3] == 1, piece[3] == 0)   # Zara performs modern
))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for each solo i that is traditional, there must exist some solo j < i where Wayne performs a modern piece.
# Equivalently: the first traditional piece must come after at least one Wayne modern piece.
# Find the first traditional piece position
for i in range(5):
    # If solo i is traditional, then there must be some j < i with pianist[j]==0 and piece[j]==0
    solver.add(Implies(piece[i] == 1, Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])))

# Now test each option: which sets of traditional pieces are possible?
# Option A: solos 1, 3, 4 are traditional (indices 0, 2, 3)
# Option B: solos 2, 3, 4 are traditional (indices 1, 2, 3)
# Option C: solos 3, 4 are traditional (indices 2, 3)
# Option D: solos 3, 5 are traditional (indices 2, 4)
# Option E: solos 4, 5 are traditional (indices 3, 4)

def make_option_constraint(trad_indices):
    """Create constraint that exactly the given indices are traditional."""
    constraints = []
    for i in range(5):
        if i in trad_indices:
            constraints.append(piece[i] == 1)
        else:
            constraints.append(piece[i] == 0)
    return And(constraints)

options = {
    "A": make_option_constraint([0, 2, 3]),
    "B": make_option_constraint([1, 2, 3]),
    "C": make_option_constraint([2, 3]),
    "D": make_option_constraint([2, 4]),
    "E": make_option_constraint([3, 4]),
}

found_options = []
for letter, constr in options.items():
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