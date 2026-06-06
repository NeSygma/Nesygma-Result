from z3 import *

# Define breed constants
H, M, S = 0, 1, 2  # Himalayan, Manx, Siamese
G, N, R = 0, 1, 2  # Greyhound, Newfoundland, Rottweiler

# Days 1-7 (using 0-indexed for array, but we'll use 1-7 in logic)
kitten = [Int(f'kitten_{d}') for d in range(1, 8)]  # index 0 = day 1
puppy = [Int(f'puppy_{d}') for d in range(1, 8)]    # index 0 = day 1

solver = Solver()

# Base constraints
# 1. Greyhounds are featured on day 1
solver.add(puppy[0] == G)

# 2. No breed is featured on any two consecutive days
# For kittens
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
# For puppies
for i in range(6):
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# 4. Himalayans are featured on exactly three days, but not on day 1
himalayan_count = Sum([If(kitten[d] == H, 1, 0) for d in range(7)])
solver.add(himalayan_count == 3)
solver.add(kitten[0] != H)

# 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != R)
for d in range(7):
    solver.add(Implies(kitten[d] == H, puppy[d] != R))

# Additional constraint from question: Himalayans are not featured on day 7
solver.add(kitten[6] != H)

# Domain constraints: breeds must be one of the three
for d in range(7):
    solver.add(Or(kitten[d] == H, kitten[d] == M, kitten[d] == S))
    solver.add(Or(puppy[d] == G, puppy[d] == N, puppy[d] == R))

# Answer choices
# A: Greyhounds are featured on days 3 and 5 (days 3 and 5 are indices 2 and 4)
opt_a = And(puppy[2] == G, puppy[4] == G)

# B: Newfoundland are featured on day 3 (day 3 is index 2)
opt_b = (puppy[2] == N)

# C: Rottweilers are featured on day 6 (day 6 is index 5)
opt_c = (puppy[5] == R)

# D: Rottweilers are featured only on day 3
# This means Rottweilers on day 3, and NOT on any other day
opt_d = And(puppy[2] == R, 
            puppy[0] != R, puppy[1] != R, puppy[3] != R, 
            puppy[4] != R, puppy[5] != R, puppy[6] != R)

# E: Rottweilers are featured on exactly three days
r_count = Sum([If(puppy[d] == R, 1, 0) for d in range(7)])
opt_e = (r_count == 3)

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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