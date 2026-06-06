from z3 import *

# Define constants for kitten breeds
H, M, S = 0, 1, 2
# Define constants for puppy breeds
G, N, R = 0, 1, 2

# Number of days
D = 7

# Declare variables
kitten = [Int(f'kitten_{i+1}') for i in range(D)]
puppy = [Int(f'puppy_{i+1}') for i in range(D)]

solver = Solver()

# Domain constraints
for i in range(D):
    solver.add(Or(kitten[i] == H, kitten[i] == M, kitten[i] == S))
    solver.add(Or(puppy[i] == G, puppy[i] == N, puppy[i] == R))

# Base constraints
# 1. Greyhounds on day 1
solver.add(puppy[0] == G)
# 2. No breed consecutive days (both categories)
for i in range(D-1):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])
# 3. Day1 breed not on day7 (both categories)
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])
# 4. Himalayans exactly three days, not on day1
solver.add(Sum([If(kitten[i] == H, 1, 0) for i in range(D)]) == 3)
solver.add(kitten[0] != H)
# 5. Rottweilers not on day7, nor on any day with Himalayans
solver.add(puppy[6] != R)
for i in range(D):
    solver.add(Implies(kitten[i] == H, puppy[i] != R))

# Prepare option constraints for kitten sequences
options = {
    "A": [H, M, S, H, M, H, S],
    "B": [M, H, S, H, M, H, M],
    "C": [M, H, M, H, S, M, S],
    "D": [S, H, M, H, S, S, H],
    "E": [S, H, S, H, M, S, H]
}

found_options = []
for letter, seq in options.items():
    solver.push()
    # Constrain kitten variables to this sequence
    for i in range(D):
        solver.add(kitten[i] == seq[i])
    # Check satisfiability (puppy variables free to satisfy constraints)
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