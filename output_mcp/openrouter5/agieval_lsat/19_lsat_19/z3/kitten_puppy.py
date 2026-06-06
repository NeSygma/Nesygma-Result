from z3 import *

# Days 1 through 7
days = list(range(7))  # 0-indexed: day0=day1, ..., day6=day7

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = IntVector('kitten', 7)
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = IntVector('puppy', 7)

solver = Solver()

# Domain constraints
for d in days:
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Greyhounds are featured on day 1 (day index 0)
solver.add(puppy[0] == 0)

# No breed is featured on any two consecutive days
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Any breed featured on day 1 is not featured on day 7
# Day 1 is index 0, day 7 is index 6
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)
solver.add(kitten[0] != 0)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans
# Rottweiler = 2
solver.add(puppy[6] != 2)
for d in days:
    # If kitten[d] == 0 (Himalayan), then puppy[d] != 2 (Rottweiler)
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Now evaluate each option
# Each option gives the kitten order from day 1 to day 7 (7 entries)
# Option A: Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese
# 0=Himalayan, 1=Manx, 2=Siamese
opt_a = [0, 1, 2, 0, 1, 0, 2]
# Option B: Manx, Himalayan, Siamese, Himalayan, Manx, Himalayan, Manx
opt_b = [1, 0, 2, 0, 1, 0, 1]
# Option C: Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese
opt_c = [1, 0, 1, 0, 2, 1, 2]
# Option D: Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan
opt_d = [2, 0, 1, 0, 2, 2, 0]
# Option E: Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan
opt_e = [2, 0, 2, 0, 1, 2, 0]

found_options = []
for letter, opt in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # Add constraint that kitten sequence matches this option
    for d in days:
        solver.add(kitten[d] == opt[d])
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