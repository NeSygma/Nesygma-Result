from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the solver
solver = Solver()

# We have 5 solos, indexed 0 to 4 for Z3 convenience (0=1st, 1=2nd, 2=3rd, 3=4th, 4=5th)
# Each solo has:
# - pianist: 0 for Wayne, 1 for Zara
# - piece_type: 0 for Modern, 1 for Traditional

# Declare variables
pianists = [Int(f'pianist_{i}') for i in range(5)]
piece_types = [Int(f'piece_type_{i}') for i in range(5)]

# Base constraints

# 1. The third solo is a traditional piece (index 2)
solver.add(piece_types[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively
# This means there are exactly two traditional pieces in total, and they are consecutive
# So, we need to enforce:
# - Exactly two solos are traditional
# - The two traditional solos are consecutive

# Count the number of traditional pieces
num_traditional = Sum([If(t == 1, 1, 0) for t in piece_types])
solver.add(num_traditional == 2)

# Ensure the two traditional pieces are consecutive
consecutive_pairs = []
for i in range(4):
    consecutive_pairs.append(And(piece_types[i] == 1, piece_types[i+1] == 1))

# Exactly one pair of consecutive traditional pieces
solver.add(Sum([If(p, 1, 0) for p in consecutive_pairs]) == 1)

# 3. In the fourth solo (index 3), either Wayne performs a traditional piece or Zara performs a modern piece
solver.add(Or(
    And(pianists[3] == 0, piece_types[3] == 1),  # Wayne performs traditional
    And(pianists[3] == 1, piece_types[3] == 0)   # Zara performs modern
))

# 4. The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4)
solver.add(pianists[1] != pianists[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece
# This means: For any solo where Wayne performs a traditional piece, there must be a prior solo where Wayne performs a modern piece
# We'll encode this by ensuring that the first time Wayne performs a traditional piece, it must be after he has performed a modern piece
for i in range(5):
    # If Wayne performs a traditional piece at solo i, then there must be a prior solo where Wayne performs a modern piece
    solver.add(Implies(
        And(pianists[i] == 0, piece_types[i] == 1),
        Or(
            *[And(pianists[j] == 0, piece_types[j] == 0) for j in range(i)]  # j < i
        )
    ))

# Additionally, Wayne must perform at least one modern piece
solver.add(Or(*[pianists[i] == 0 and piece_types[i] == 0 for i in range(5)]))

# Now, evaluate the multiple-choice options
# Each option specifies a set of solos that are traditional pieces
# We will test each option by constraining the piece_types accordingly

# Option A: first, third, and fourth are traditional
# But we now enforce exactly two traditional pieces, so this is invalid
opt_a_constr = And(
    piece_types[0] == 1,  # solo 1
    piece_types[2] == 1,  # solo 3
    piece_types[3] == 1,  # solo 4
    num_traditional == 2
)

# Option B: second, third, and fourth are traditional
# Also invalid due to num_traditional == 2
opt_b_constr = And(
    piece_types[1] == 1,  # solo 2
    piece_types[2] == 1,  # solo 3
    piece_types[3] == 1,  # solo 4
    num_traditional == 2
)

# Option C: third and fourth are traditional
opt_c_constr = And(
    piece_types[2] == 1,  # solo 3
    piece_types[3] == 1,  # solo 4
    num_traditional == 2
)

# Option D: third and fifth are traditional
opt_d_constr = And(
    piece_types[2] == 1,  # solo 3
    piece_types[4] == 1,  # solo 5
    num_traditional == 2
)

# Option E: fourth and fifth are traditional
opt_e_constr = And(
    piece_types[3] == 1,  # solo 4
    piece_types[4] == 1,  # solo 5
    num_traditional == 2
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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