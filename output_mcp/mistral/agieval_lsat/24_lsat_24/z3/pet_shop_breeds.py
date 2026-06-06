from z3 import *

# Breed constants
H, M, S = 0, 1, 2  # Kittens: Himalayan, Manx, Siamese
G, N, R = 0, 1, 2  # Puppies: Greyhound, Newfoundland, Rottweiler

solver = Solver()

# Days 1-7 (1-indexed, stored as 0-indexed list for Python)
kitten = [Int(f'kitten_{i}') for i in range(7)]  # days 1-7 -> indices 0-6
puppy = [Int(f'puppy_{i}') for i in range(7)]    # days 1-7 -> indices 0-6

# Each day has exactly one kitten breed and one puppy breed
for i in range(7):
    solver.add(Or(kitten[i] == H, kitten[i] == M, kitten[i] == S))
    solver.add(Or(puppy[i] == G, puppy[i] == N, puppy[i] == R))

# Constraint 1: Greyhounds on day 1 (index 0)
solver.add(puppy[0] == G)

# Constraint 2: No consecutive same breed
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Constraint 3: Breed on day 1 not on day 7 (index 6)
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans on exactly 3 days, not on day 1 (index 0)
solver.add(Sum([If(kitten[i] == H, 1, 0) for i in range(7)]) == 3)
solver.add(kitten[0] != H)

# Constraint 5: Rottweilers not on day 7 (index 6)
solver.add(puppy[6] != R)

# Constraint 6: Rottweilers not on days with Himalayans
for i in range(7):
    solver.add(Implies(kitten[i] == H, puppy[i] != R))

# Additional condition: Himalayans not on day 7 (index 6)
solver.add(kitten[6] != H)

# Define the options as constraints
opt_A = And(puppy[2] == G, puppy[4] == G)  # Greyhounds on days 3 and 5 (indices 2 and 4)
opt_B = (puppy[2] == N)                    # Newfoundlands on day 3 (index 2)
opt_C = (puppy[5] == R)                    # Rottweilers on day 6 (index 5)
opt_D = And(puppy[2] == R, 
            And([puppy[i] != R for i in range(7) if i != 2]))  # Rottweilers only on day 3 (index 2)
opt_E = (Sum([If(puppy[i] == R, 1, 0) for i in range(7)]) == 3)  # Rottweilers on exactly 3 days

# Test each option
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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