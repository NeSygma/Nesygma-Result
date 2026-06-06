from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the solver
solver = Solver()

# We have 5 solos, indexed 1 to 5
# Each solo has:
# - pianist: 0 for Wayne, 1 for Zara
# - piece_type: 0 for Modern, 1 for Traditional

# Declare variables
pianists = [Int(f'pianist_{i}') for i in range(1, 6)]
piece_types = [Int(f'piece_type_{i}') for i in range(1, 6)]

# Helper to convert 0/1 to Wayne/Zara and Modern/Traditional
def pianist_str(p):
    return "Wayne" if p == 0 else "Zara"

def piece_str(t):
    return "Modern" if t == 0 else "Traditional"

# Base constraints

# 1. The third solo is a traditional piece
solver.add(piece_types[2] == 1)  # Index 2 corresponds to solo 3

# 2. Exactly two of the traditional pieces are performed consecutively
# This means there is exactly one pair of consecutive solos where both are traditional
# and no other consecutive traditional pairs
consecutive_traditional_pairs = []
for i in range(4):  # pairs (1,2), (2,3), (3,4), (4,5)
    consecutive_traditional_pairs.append(And(piece_types[i] == 1, piece_types[i+1] == 1))

# Exactly one such pair exists
solver.add(Sum([If(p, 1, 0) for p in consecutive_traditional_pairs]) == 1)

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece
solver.add(Or(
    And(pianists[3] == 0, piece_types[3] == 1),  # Wayne performs traditional
    And(pianists[3] == 1, piece_types[3] == 0)   # Zara performs modern
))

# 4. The pianist who performs the second solo does not perform the fifth solo
solver.add(pianists[1] != pianists[4])  # Index 1 is solo 2, index 4 is solo 5

# 5. No traditional piece is performed until Wayne performs at least one modern piece
# This means: For any solo where Wayne performs a traditional piece, there must be a prior solo where Wayne performs a modern piece
# We can encode this as: For all solos i, if pianist[i] == Wayne and piece_type[i] == Traditional, then there exists j < i such that pianist[j] == Wayne and piece_type[j] == Modern
# We'll encode this by ensuring that the first time Wayne performs a traditional piece, it must be after he has performed a modern piece
# To do this, we can iterate through the solos and track whether Wayne has performed a modern piece before any traditional piece

# Let's encode this constraint explicitly
for i in range(5):
    # If Wayne performs a traditional piece at solo i+1, then there must be a prior solo where Wayne performs a modern piece
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

# Define the options as constraints on piece_types
# Option A: first, third, fourth are traditional
opt_a_constr = And(
    piece_types[0] == 1,  # solo 1
    piece_types[2] == 1,  # solo 3
    piece_types[3] == 1,  # solo 4
    piece_types[1] == 0,  # solo 2 not traditional
    piece_types[4] == 0   # solo 5 not traditional
)

# Option B: second, third, fourth are traditional
opt_b_constr = And(
    piece_types[1] == 1,  # solo 2
    piece_types[2] == 1,  # solo 3
    piece_types[3] == 1,  # solo 4
    piece_types[0] == 0,  # solo 1 not traditional
    piece_types[4] == 0   # solo 5 not traditional
)

# Option C: third and fourth are traditional
opt_c_constr = And(
    piece_types[2] == 1,  # solo 3
    piece_types[3] == 1,  # solo 4
    piece_types[0] == 0,  # solo 1 not traditional
    piece_types[1] == 0,  # solo 2 not traditional
    piece_types[4] == 0   # solo 5 not traditional
)

# Option D: third and fifth are traditional
opt_d_constr = And(
    piece_types[2] == 1,  # solo 3
    piece_types[4] == 1,  # solo 5
    piece_types[0] == 0,  # solo 1 not traditional
    piece_types[1] == 0,  # solo 2 not traditional
    piece_types[3] == 0   # solo 4 not traditional
)

# Option E: fourth and fifth are traditional
opt_e_constr = And(
    piece_types[3] == 1,  # solo 4
    piece_types[4] == 1,  # solo 5
    piece_types[0] == 0,  # solo 1 not traditional
    piece_types[1] == 0,  # solo 2 not traditional
    piece_types[2] == 0   # solo 3 not traditional
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