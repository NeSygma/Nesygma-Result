from z3 import *

solver = Solver()

# Variables for each position (1-5)
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]  # 0 = Wayne, 1 = Zara
piece_type = [Int(f'type_{i}') for i in range(1, 6)]   # 0 = Modern, 1 = Traditional

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Constraint 1: Third solo is traditional
solver.add(piece_type[2] == 1)  # index 2 corresponds to position 3

# Constraint 2: Exactly two traditional pieces are performed consecutively
# This means: There is exactly one pair of consecutive positions where both are traditional
# AND there are no other traditional pieces that are consecutive to anything else
# Actually, let's think: If we have exactly two traditional pieces that are consecutive,
# that means we have exactly one pair of consecutive traditional pieces.
# But we also need to ensure there are no other traditional pieces that are consecutive to anything.
# Let's count total traditional pieces and consecutive pairs.

# First, let's count total traditional pieces
traditional_count = Sum([If(piece_type[i] == 1, 1, 0) for i in range(5)])

# Count consecutive traditional pairs
consecutive_pairs = []
for i in range(4):
    consecutive_pairs.append(And(piece_type[i] == 1, piece_type[i+1] == 1))
consecutive_count = Sum([If(cp, 1, 0) for cp in consecutive_pairs])

# The constraint "exactly two of the traditional pieces are performed consecutively"
# likely means: There are exactly two traditional pieces that are consecutive to each other.
# This implies: consecutive_count == 1 (one pair of consecutive traditional pieces)
# AND traditional_count >= 2 (at least two traditional pieces total)
# But we also need to ensure that there are no other traditional pieces that are isolated?
# Actually, the phrasing is ambiguous. Let me interpret as:
# There is exactly one pair of consecutive traditional pieces, and no other traditional pieces.
# OR: There are exactly two traditional pieces total, and they are consecutive.
# Let's try the second interpretation first.

# Actually, re-reading: "Exactly two of the traditional pieces are performed consecutively."
# This could mean: Among all traditional pieces, exactly two of them are consecutive (i.e., form a pair).
# This doesn't necessarily mean there are only two traditional pieces total.
# It could mean: There is one pair of consecutive traditional pieces, and any other traditional pieces are isolated.
# Let's implement: consecutive_count == 1, and for any traditional piece not in the pair, it's not adjacent to another traditional piece.

# Let's define which positions are in the consecutive pair
# We'll use a more direct approach: ensure exactly one consecutive pair exists
solver.add(consecutive_count == 1)

# Also ensure that if there are more than 2 traditional pieces, they are not adjacent to the pair
# Actually, let's think differently: The constraint might simply mean there are exactly two traditional pieces total, and they are consecutive.
# Let's try that interpretation first.

# Interpretation 1: Exactly two traditional pieces total, and they are consecutive
# solver.add(traditional_count == 2)
# solver.add(consecutive_count == 1)

# Interpretation 2: There is exactly one pair of consecutive traditional pieces, and no other traditional pieces are consecutive to anything
# This is more complex. Let's try Interpretation 1 first.

# Actually, let me re-read the problem statement more carefully:
# "Exactly two of the traditional pieces are performed consecutively."
# This most naturally means: There are exactly two traditional pieces that are consecutive to each other.
# It doesn't say "exactly two traditional pieces total", so there could be more traditional pieces,
# but exactly two of them form a consecutive pair.

# Let's implement: consecutive_count == 1
# And we need to ensure that no other traditional pieces are adjacent to each other or to the pair
# Actually, if consecutive_count == 1, that means there's exactly one pair of consecutive traditional pieces.
# Any other traditional pieces would be isolated (not adjacent to another traditional piece).
# This seems reasonable.

# Constraint 3: Fourth solo condition
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),  # Wayne traditional
    And(pianist[3] == 1, piece_type[3] == 0)   # Zara modern
))

# Constraint 4: Pianist of second solo ≠ pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# This means: Before the first traditional piece appears, Wayne must have performed at least one modern piece.
# Let's find the first position where type == 1 (traditional)
# For all positions i where type[i] == 1, there must be some j < i with pianist[j] == 0 and type[j] == 0
for i in range(5):
    # For each position i, if it's traditional, there must be a Wayne modern before it
    has_wayne_modern_before = Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])
    solver.add(Implies(piece_type[i] == 1, has_wayne_modern_before))

# Additional condition: Fifth solo is Wayne performing traditional
solver.add(pianist[4] == 0)  # Wayne
solver.add(piece_type[4] == 1)  # Traditional

# Now evaluate each answer choice
found_options = []

# Option A: Zara performs the first solo
opt_a = pianist[0] == 1  # Zara
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Wayne performs the second solo
opt_b = pianist[1] == 0  # Wayne
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Zara performs the third solo
opt_c = pianist[2] == 1  # Zara
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The second solo is a modern piece
opt_d = piece_type[1] == 0  # Modern
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The fourth solo is a traditional piece
opt_e = piece_type[3] == 1  # Traditional
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")