from z3 import *

solver = Solver()

# Days 1 through 7
days = list(range(1, 8))

# Breeds of kittens: Himalayan (H), Manx (M), Siamese (S)
# Breeds of puppies: Greyhound (G), Newfoundland (N), Rottweiler (R)

# For each day, we have a kitten breed and a puppy breed.
# Use integer variables: 0=Himalayan, 1=Manx, 2=Siamese for kittens
# 0=Greyhound, 1=Newfoundland, 2=Rottweiler for puppies

kitten = [Int(f'kitten_{d}') for d in days]
puppy = [Int(f'puppy_{d}') for d in days]

# Domain constraints
for d in days:
    solver.add(And(kitten[d-1] >= 0, kitten[d-1] <= 2))
    solver.add(And(puppy[d-1] >= 0, puppy[d-1] <= 2))

# Greyhounds are featured on day 1.
solver.add(puppy[0] == 0)

# No breed is featured on any two consecutive days.
# For kittens
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d-1])
# For puppies
for d in range(1, 7):
    solver.add(puppy[d] != puppy[d-1])

# Any breed featured on day 1 is not featured on day 7.
# Day 1 kitten breed != day 7 kitten breed
solver.add(kitten[0] != kitten[6])
# Day 1 puppy breed != day 7 puppy breed
solver.add(puppy[0] != puppy[6])

# Himalayans are featured on exactly three days, but not on day 1.
# Himalayan = 0
solver.add(kitten[0] != 0)
solver.add(Sum([If(kitten[d-1] == 0, 1, 0) for d in days]) == 3)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans.
# Rottweiler = 2
solver.add(puppy[6] != 2)
# On any day where kitten is Himalayan (0), puppy cannot be Rottweiler (2)
for d in days:
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Additional condition: If Himalayans are not featured on day 2
solver.add(kitten[1] != 0)

# Now evaluate each option
# Option A: Manx are featured on day 3. Manx = 1
opt_a = (kitten[2] == 1)

# Option B: Siamese are featured on day 4. Siamese = 2
opt_b = (kitten[3] == 2)

# Option C: Rottweilers are featured on day 5. Rottweiler = 2
opt_c = (puppy[4] == 2)

# Option D: Himalayans are featured on day 6. Himalayan = 0
opt_d = (kitten[5] == 0)

# Option E: Greyhounds are featured on day 7. Greyhound = 0
opt_e = (puppy[6] == 0)

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