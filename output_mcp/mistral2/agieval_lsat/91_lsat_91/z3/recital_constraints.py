from z3 import *

# Initialize solver
solver = Solver()

# Number of solos
N = 5

# Pianists: 0 = Wayne, 1 = Zara
pianist = [Int(f'pianist_{i}') for i in range(N)]
# Piece types: 0 = Modern, 1 = Traditional
piece_type = [Int(f'piece_type_{i}') for i in range(N)]

# Constraints
solver.add(piece_type[2] == 1)  # Third solo is traditional

# Exactly two traditional pieces are consecutive
# This means there is exactly one pair of consecutive 1s in piece_type
consecutive_pairs = []
for i in range(N - 1):
    consecutive_pairs.append(And(piece_type[i] == 1, piece_type[i+1] == 1))
solver.add(Sum([If(p, 1, 0) for p in consecutive_pairs]) == 1)

# Fourth solo constraint: Wayne performs traditional OR Zara performs modern
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1),
              And(pianist[3] == 1, piece_type[3] == 0)))

# Pianist of second solo ≠ pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# For all i, if piece_type[i] == 1, then there exists j < i such that pianist[j] == 0 and piece_type[j] == 0
for i in range(N):
    solver.add(Implies(piece_type[i] == 1,
                       Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])))

# Fifth solo is traditional
solver.add(piece_type[4] == 1)

# Domain constraints for pianists and piece types
for i in range(N):
    solver.add(pianist[i] >= 0, pianist[i] <= 1)
    solver.add(piece_type[i] >= 0, piece_type[i] <= 1)

# Now, for each answer choice, we will check how many solos have a uniquely determined pianist
# We will model this by checking if the solver can find a model where the pianist for a solo is fixed
# and then count how many such solos exist.

# We will now evaluate each answer choice (A-E) to see which one matches the count of uniquely determined pianists.

found_options = []

# Define a function to count the number of solos with a uniquely determined pianist
def count_determined_pianists():
    determined_count = 0
    for i in range(N):
        # For each solo i, check if pianist[i] is uniquely determined
        # We do this by checking if the solver can find a model where pianist[i] is fixed to a value
        # and then checking if the other value is impossible
        for p in [0, 1]:
            solver.push()
            solver.add(pianist[i] == p)
            res = solver.check()
            if res == unsat:
                # The other value must be the only possibility
                determined_count += 1
                solver.pop()
                break
            else:
                solver.pop()
    return determined_count

# Now, for each answer choice, we will check if the count matches the choice
for letter, expected_count in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver.push()
    actual_count = count_determined_pianists()
    if actual_count == expected_count:
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