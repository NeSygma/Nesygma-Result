from z3 import *

# Days: 1-7
days = range(1, 8)

# Kitten breeds: Himalayan (H), Manx (M), Siamese (S)
# Puppy breeds: Greyhound (G), Newfoundland (N), Rottweiler (R)

# Create symbolic variables for each day
kitten = [Int(f'kitten_{d}') for d in days]  # 0=H, 1=M, 2=S
puppy = [Int(f'puppy_{d}') for d in days]    # 0=G, 1=N, 2=R

solver = Solver()

# Domain constraints: each variable must be 0, 1, or 2
for d in days:
    solver.add(kitten[d-1] >= 0, kitten[d-1] <= 2)
    solver.add(puppy[d-1] >= 0, puppy[d-1] <= 2)

# Constraint 1: Greyhounds are featured on day 1
# Greyhound = 0
solver.add(puppy[0] == 0)

# Constraint 2: No breed is featured on any two consecutive days
# For kittens: no two consecutive days have the same kitten breed
for i in range(len(days)-1):
    solver.add(kitten[i] != kitten[i+1])
# For puppies: no two consecutive days have the same puppy breed
for i in range(len(days)-1):
    solver.add(puppy[i] != puppy[i+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
# This applies to both kitten and puppy breeds
solver.add(kitten[0] != kitten[6])  # kitten day 1 ≠ kitten day 7
solver.add(puppy[0] != puppy[6])    # puppy day 1 ≠ puppy day 7

# Constraint 4: Himalayans are featured on exactly three days, but not on day 1
# Himalayan = 0
himalayan_count = Sum([If(kitten[d-1] == 0, 1, 0) for d in days])
solver.add(himalayan_count == 3)
solver.add(kitten[0] != 0)  # not on day 1

# Constraint 5: Rottweilers are not featured on day 7, nor on any day that features Himalayans
# Rottweiler = 2
solver.add(puppy[6] != 2)  # not on day 7
# For each day, if kitten is Himalayan (0), then puppy cannot be Rottweiler (2)
for d in days:
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Now evaluate each answer choice
found_options = []

# Option A: Greyhounds and Siamese are both featured on day 2
# Greyhound = 0, Siamese = 2
opt_a = And(puppy[1] == 0, kitten[1] == 2)

# Option B: Greyhounds and Himalayans are both featured on day 7
# Greyhound = 0, Himalayan = 0
opt_b = And(puppy[6] == 0, kitten[6] == 0)

# Option C: Rottweilers and Himalayans are both featured on day 4
# Rottweiler = 2, Himalayan = 0
opt_c = And(puppy[3] == 2, kitten[3] == 0)

# Option D: Rottweilers and Manx are both featured on day 5
# Rottweiler = 2, Manx = 1
opt_d = And(puppy[4] == 2, kitten[4] == 1)

# Option E: Newfoundlands and Manx are both featured on day 6
# Newfoundland = 1, Manx = 1
opt_e = And(puppy[5] == 1, kitten[5] == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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