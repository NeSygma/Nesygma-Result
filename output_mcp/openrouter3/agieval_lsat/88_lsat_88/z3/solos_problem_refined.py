from z3 import *

# Create solver
solver = Solver()

# Define variables
# For each position (1-5), we have a pianist and a piece type
# Pianist: 0 = Wayne, 1 = Zara
# Type: 0 = modern, 1 = traditional
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]
piece_type = [Int(f'piece_type_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Constraint 1: Third solo is traditional
solver.add(piece_type[2] == 1)  # position 3 (index 2)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively
# This means there is exactly one pair of consecutive traditional pieces
# We need to count consecutive traditional pairs
consecutive_traditional_pairs = []
for i in range(4):  # positions 1-4 can start a consecutive pair
    # Check if positions i and i+1 are both traditional
    is_pair = If(And(piece_type[i] == 1, piece_type[i+1] == 1), 1, 0)
    consecutive_traditional_pairs.append(is_pair)

# Exactly one such pair
solver.add(Sum(consecutive_traditional_pairs) == 1)

# Constraint 3: Fourth solo: either Wayne performs traditional OR Zara performs modern
# Wayne = 0, Zara = 1, traditional = 1, modern = 0
# Either (pianist[3] == 0 AND piece_type[3] == 1) OR (pianist[3] == 1 AND piece_type[3] == 0)
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),
    And(pianist[3] == 1, piece_type[3] == 0)
))

# Constraint 4: Pianist who performs second solo does not perform fifth solo
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# This means: for any position i where piece_type[i] == 1 (traditional),
# there must exist some position j < i where pianist[j] == 0 (Wayne) AND piece_type[j] == 0 (modern)
# OR if there is no such j, then piece_type[i] cannot be 1 (traditional)
# Actually, the constraint means: the first traditional piece must occur after Wayne has played at least one modern piece
# So if position 0 is traditional, it's invalid (no prior position)
# If position 1 is traditional, then position 0 must have Wayne playing modern
# If position 2 is traditional, then either position 0 or 1 must have Wayne playing modern
# etc.

# Let's implement this more carefully:
# For each position i, if it's traditional, then there must be some j < i with Wayne playing modern
for i in range(5):
    # If position i is traditional
    # Then there must exist some j < i with pianist[j] == 0 and piece_type[j] == 0
    if i == 0:
        # First position cannot be traditional (no prior position for Wayne to play modern)
        solver.add(piece_type[0] == 0)
    else:
        # For positions 1-4, if it's traditional, there must be some earlier Wayne modern
        earlier_modern_wayne = []
        for j in range(i):
            earlier_modern_wayne.append(And(pianist[j] == 0, piece_type[j] == 0))
        # If piece_type[i] is traditional (1), then Or(earlier_modern_wayne) must be true
        # We can write: Implies(piece_type[i] == 1, Or(earlier_modern_wayne))
        solver.add(Implies(piece_type[i] == 1, Or(earlier_modern_wayne)))

# Now test each answer choice
# Answer choices refer to which positions are traditional pieces
# We need to check which set of positions could be ALL the traditional pieces

# Define the options as constraints that specify exactly which positions are traditional
# Option A: positions 1, 3, and 4 are traditional (others are modern)
opt_a_constr = And(
    piece_type[0] == 1,  # position 1
    piece_type[1] == 0,  # position 2
    piece_type[2] == 1,  # position 3 (already constrained)
    piece_type[3] == 1,  # position 4
    piece_type[4] == 0   # position 5
)

# Option B: positions 2, 3, and 4 are traditional
opt_b_constr = And(
    piece_type[0] == 0,  # position 1
    piece_type[1] == 1,  # position 2
    piece_type[2] == 1,  # position 3
    piece_type[3] == 1,  # position 4
    piece_type[4] == 0   # position 5
)

# Option C: positions 3 and 4 are traditional
opt_c_constr = And(
    piece_type[0] == 0,  # position 1
    piece_type[1] == 0,  # position 2
    piece_type[2] == 1,  # position 3
    piece_type[3] == 1,  # position 4
    piece_type[4] == 0   # position 5
)

# Option D: positions 3 and 5 are traditional
opt_d_constr = And(
    piece_type[0] == 0,  # position 1
    piece_type[1] == 0,  # position 2
    piece_type[2] == 1,  # position 3
    piece_type[3] == 0,  # position 4
    piece_type[4] == 1   # position 5
)

# Option E: positions 4 and 5 are traditional
opt_e_constr = And(
    piece_type[0] == 0,  # position 1
    piece_type[1] == 0,  # position 2
    piece_type[2] == 1,  # position 3
    piece_type[3] == 1,  # position 4
    piece_type[4] == 1   # position 5
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")