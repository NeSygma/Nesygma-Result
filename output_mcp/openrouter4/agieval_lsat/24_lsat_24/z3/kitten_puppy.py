from z3 import *

# Days: 1..7 (we'll use 0-indexed, so days 0..6)
NUM_DAYS = 7

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
H, Mx, S = 0, 1, 2
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
G, N, R = 0, 1, 2

kitten = [Int(f'kitten_{d}') for d in range(NUM_DAYS)]
puppy = [Int(f'puppy_{d}') for d in range(NUM_DAYS)]

solver = Solver()

# Domain constraints
for d in range(NUM_DAYS):
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Constraint 1: Greyhounds on day 1 (index 0)
solver.add(puppy[0] == G)

# Constraint 2: No breed on any two consecutive days (for both kittens and puppies)
for d in range(NUM_DAYS - 1):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7 (index 6)
# So kitten[0] != kitten[6] and puppy[0] != puppy[6]
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])  # puppy[0]=G, so puppy[6] != G

# Constraint 4: Himalayans on exactly three days, not on day 1
solver.add(kitten[0] != H)
solver.add(Sum([If(kitten[d] == H, 1, 0) for d in range(NUM_DAYS)]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != R)
for d in range(NUM_DAYS):
    solver.add(Implies(kitten[d] == H, puppy[d] != R))

# Additional: Himalayans are not featured on day 7 (from the question)
solver.add(kitten[6] != H)

# Now evaluate each option
found_options = []

# Option A: Greyhounds are featured on days 3 and 5 (indices 2 and 4)
opt_a = And(puppy[2] == G, puppy[4] == G)

# Option B: Newfoundlands are featured on day 3 (index 2)
opt_b = puppy[2] == N

# Option C: Rottweilers are featured on day 6 (index 5)
opt_c = puppy[5] == R

# Option D: Rottweilers are featured only on day 3 (index 2)
# Rottweilers on day 3 and not on any other day
opt_d_constrs = [puppy[2] == R]
for d in range(NUM_DAYS):
    if d != 2:
        opt_d_constrs.append(puppy[d] != R)
opt_d = And(opt_d_constrs)

# Option E: Rottweilers are featured on exactly three days
opt_e = Sum([If(puppy[d] == R, 1, 0) for d in range(NUM_DAYS)]) == 3

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