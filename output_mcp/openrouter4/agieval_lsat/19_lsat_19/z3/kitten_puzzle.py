from z3 import *

# Define sorts
# Kitten: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

# Variables
K = [Int(f'K_{i}') for i in range(1, 8)]  # day 1..7
P = [Int(f'P_{i}') for i in range(1, 8)]

# Base solver
solver = Solver()

# Domain constraints
for i in range(7):
    solver.add(And(K[i] >= 0, K[i] <= 2))
    solver.add(And(P[i] >= 0, P[i] <= 2))

# Constraint 1: Greyhounds on day 1
solver.add(P[0] == 0)

# Constraint 2: No breed on consecutive days
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])

# Constraint 3: Any breed featured on day 1 not on day 7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# Constraint 4: Himalayans exactly three days, not on day 1
solver.add(Sum([If(K[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(K[0] != 0)

# Constraint 5: Rottweilers not on day 7, nor on any day with Himalayans
solver.add(P[6] != 2)
for i in range(7):
    solver.add(Implies(K[i] == 0, P[i] != 2))

# Define option sequences
options = {
    "A": [0, 1, 2, 0, 1, 0, 2],  # Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese
    "B": [1, 0, 2, 0, 1, 0, 1],  # Manx, Himalayan, Siamese, Himalayan, Manx, Himalayan, Manx
    "C": [1, 0, 1, 0, 2, 1, 2],  # Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese
    "D": [2, 0, 1, 0, 2, 2, 0],  # Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan
    "E": [2, 0, 2, 0, 1, 2, 0],  # Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan
}

found_options = []
for letter, seq in options.items():
    solver.push()
    # Add constraints fixing the kitten sequence for this option
    for i in range(7):
        solver.add(K[i] == seq[i])
    if solver.check() == sat:
        found_options.append(letter)
    else:
        pass  # unsat, skip
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