from z3 import *

solver = Solver()

# Days 1 through 7
days = list(range(1, 8))

# Breeds of kittens: 0=Himalayan, 1=Manx, 2=Siamese
kitten = IntVector('kitten', 8)  # index 1..7, ignore index 0
for d in days:
    solver.add(kitten[d] >= 0, kitten[d] <= 2)

# Breeds of puppies: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = IntVector('puppy', 8)  # index 1..7, ignore index 0
for d in days:
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Greyhounds are featured on day 1.
solver.add(puppy[1] == 0)

# No breed is featured on any two consecutive days.
# For kittens
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
# For puppies
for d in range(1, 7):
    solver.add(puppy[d] != puppy[d+1])

# Any breed featured on day 1 is not featured on day 7.
# Day 1 has kitten breed k1 and puppy breed p1 (puppy[1]=0=Greyhound)
# So the kitten breed on day 1 cannot appear on day 7, and Greyhound (puppy breed 0) cannot appear on day 7.
solver.add(kitten[7] != kitten[1])
solver.add(puppy[7] != puppy[1])  # puppy[1]=0, so puppy[7] != 0

# Himalayans are featured on exactly three days, but not on day 1.
# Himalayan = 0
solver.add(kitten[1] != 0)
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans.
# Rottweiler = 2
solver.add(puppy[7] != 2)
# On any day where kitten is Himalayan (0), puppy cannot be Rottweiler (2)
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Now evaluate each option

# Option A: Greyhounds and Siamese are both featured on day 2.
# Greyhound = 0, Siamese = 2
opt_a = And(puppy[2] == 0, kitten[2] == 2)

# Option B: Greyhounds and Himalayans are both featured on day 7.
# Greyhound = 0, Himalayan = 0
opt_b = And(puppy[7] == 0, kitten[7] == 0)

# Option C: Rottweilers and Himalayans are both featured on day 4.
# Rottweiler = 2, Himalayan = 0
opt_c = And(puppy[4] == 2, kitten[4] == 0)

# Option D: Rottweilers and Manx are both featured on day 5.
# Rottweiler = 2, Manx = 1
opt_d = And(puppy[5] == 2, kitten[5] == 1)

# Option E: Newfoundlands and Manx are both featured on day 6.
# Newfoundland = 1, Manx = 1
opt_e = And(puppy[6] == 1, kitten[6] == 1)

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