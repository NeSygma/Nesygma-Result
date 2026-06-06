from z3 import *

# Define integer constants for breeds
H, M, S = 0, 1, 2  # kitten breeds
G, N, R = 0, 1, 2  # puppy breeds

# Create solver
solver = Solver()

# Declare variables for kitten and puppy per day (0-indexed for days 0..6)
k = [Int(f'k_{i}') for i in range(7)]
p = [Int(f'p_{i}') for i in range(7)]

# Base constraints common to all options
# 1. Greyhounds on day 1 (day index 0)
solver.add(p[0] == G)

# 2. No breed on consecutive days (for both kittens and puppies)
for i in range(6):
    solver.add(k[i] != k[i+1])
    solver.add(p[i] != p[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
solver.add(k[0] != k[6])
solver.add(p[0] != p[6])

# 4. Himalayans exactly three days, not on day 1
solver.add(Sum([If(k[i] == H, 1, 0) for i in range(7)]) == 3)
solver.add(k[0] != H)

# 5. Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(p[6] != R)
for i in range(7):
    solver.add(Implies(k[i] == H, p[i] != R))

# Domain constraints: each breed variable must be in {0,1,2}
for i in range(7):
    solver.add(Or(k[i] == H, k[i] == M, k[i] == S))
    solver.add(Or(p[i] == G, p[i] == N, p[i] == R))

# Now define the answer choices as kitten sequences
choices = [
    ("A", [H, M, S, H, M, H, S]),  # Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese
    ("B", [M, H, S, H, M, H, M]),  # Manx, Himalayan, Siamese, Himalayan, Manx, Himalayan, Manx
    ("C", [M, H, M, H, S, M, S]),  # Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese
    ("D", [S, H, M, H, S, S, H]),  # Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan
    ("E", [S, H, S, H, M, S, H])   # Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan
]

found_options = []
for letter, seq in choices:
    solver.push()
    # Add constraints for this specific kitten sequence
    for i in range(7):
        solver.add(k[i] == seq[i])
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")