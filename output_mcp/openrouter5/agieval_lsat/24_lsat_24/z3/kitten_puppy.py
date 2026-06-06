from z3 import *

solver = Solver()

# Days 1 through 7
days = list(range(1, 8))

# Breeds of kitten: Himalayan (H), Manx (M), Siamese (S)
# Breeds of puppy: Greyhound (G), Newfoundland (N), Rottweiler (R)

# We'll use integer variables for each day for kitten and puppy breeds.
# Kitten: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

kitten = IntVector('kitten', 8)  # index 1..7
puppy = IntVector('puppy', 8)    # index 1..7

for d in days:
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Greyhounds are featured on day 1.
solver.add(puppy[1] == 0)

# No breed is featured on any two consecutive days.
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Any breed featured on day 1 is not featured on day 7.
# Day 1 has kitten breed and puppy breed. So:
solver.add(kitten[7] != kitten[1])
solver.add(puppy[7] != puppy[1])

# Himalayans are featured on exactly three days, but not on day 1.
solver.add(kitten[1] != 0)  # not on day 1
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans.
solver.add(puppy[7] != 2)  # not on day 7
# On any day that features Himalayans (kitten[d]==0), puppy[d] != 2 (Rottweiler)
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Additional condition from the question: "If Himalayans are not featured on day 7"
# This is already implied by the rule "Any breed featured on day 1 is not featured on day 7"
# and "Himalayans are not on day 1". But let's add it explicitly to be safe.
solver.add(kitten[7] != 0)

# Now evaluate each option

# Option A: Greyhounds are featured on days 3 and 5.
opt_a = And(puppy[3] == 0, puppy[5] == 0)

# Option B: Newfoundlands are featured on day 3.
opt_b = (puppy[3] == 1)

# Option C: Rottweilers are featured on day 6.
opt_c = (puppy[6] == 2)

# Option D: Rottweilers are featured only on day 3.
# "only on day 3" means Rottweiler on day 3, and NOT Rottweiler on all other days.
opt_d = And(puppy[3] == 2, And([puppy[d] != 2 for d in days if d != 3]))

# Option E: Rottweilers are featured on exactly three days.
opt_e = (Sum([If(puppy[d] == 2, 1, 0) for d in days]) == 3)

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