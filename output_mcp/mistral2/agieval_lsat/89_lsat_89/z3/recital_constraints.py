from z3 import *

# We have 5 solos, indexed 0 to 4 (0-based for convenience)
# Each solo has two attributes:
# - pianist: Wayne (0) or Zara (1)
# - piece_type: modern (0) or traditional (1)

# Decision variables
pianists = [Int(f'pianist_{i}') for i in range(5)]  # 0: Wayne, 1: Zara
piece_types = [Int(f'piece_type_{i}') for i in range(5)]  # 0: modern, 1: traditional

solver = Solver()

# Constraints

# 1. The third solo is a traditional piece.
solver.add(piece_types[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively.
# We need to find exactly one pair of consecutive solos where both are traditional.
consecutive_traditional_pairs = []
for i in range(4):
    consecutive_traditional_pairs.append(And(piece_types[i] == 1, piece_types[i+1] == 1))

# Exactly one such pair must be true
solver.add(Sum([If(p, 1, 0) for p in consecutive_traditional_pairs]) == 1)

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
solver.add(Or(And(pianists[3] == 0, piece_types[3] == 1), 
              And(pianists[3] == 1, piece_types[3] == 0)))

# 4. The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianists[1] != pianists[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# This means that for all solos before Wayne's first modern piece, the piece_type must be modern.
# We need to find the first solo where Wayne performs a modern piece.
# Let's introduce a variable for the first index where Wayne performs a modern piece.
first_wayne_modern = Int('first_wayne_modern')
# Wayne performs a modern piece at this index
solver.add(And(first_wayne_modern >= 0, first_wayne_modern < 5))
# Use Or-Loop to constrain the first_wayne_modern index
solver.add(Or([And(first_wayne_modern == i, pianists[i] == 0, piece_types[i] == 0) for i in range(5)]))
# For all solos before this index, Wayne must not have performed a modern piece
for i in range(5):
    solver.add(Implies(i < first_wayne_modern, 
                       Or(pianists[i] != 0, piece_types[i] != 0)))

# Additional constraint: Wayne must perform at least one modern piece
solver.add(Or([And(pianists[i] == 0, piece_types[i] == 0) for i in range(5)]))

# Now, we need to find the minimum number of solos in which Wayne performs a traditional piece.
# We will check each option (A: 0, B: 1, C: 2, D: 3, E: 4) to see which is possible.

# We will count the number of solos where Wayne performs a traditional piece.
wayne_traditional_count = Sum([If(And(pianists[i] == 0, piece_types[i] == 1), 1, 0) for i in range(5)])

# Now, we will check each option to see if it is possible.
found_options = []

# Option A: zero
solver.push()
solver.add(wayne_traditional_count == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: one
solver.push()
solver.add(wayne_traditional_count == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: two
solver.push()
solver.add(wayne_traditional_count == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: three
solver.push()
solver.add(wayne_traditional_count == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: four
solver.push()
solver.add(wayne_traditional_count == 4)
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