from z3 import *

solver = Solver()

# Days 1 through 7
days = list(range(7))  # 0-indexed: day0 = day1, ..., day6 = day7

# Breeds of kitten: 0=Himalayan, 1=Manx, 2=Siamese
kitten = IntVector('kitten', 7)
for d in days:
    solver.add(kitten[d] >= 0, kitten[d] <= 2)

# Breeds of puppy: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = IntVector('puppy', 7)
for d in days:
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Greyhounds are featured on day 1 (day0)
solver.add(puppy[0] == 0)

# No breed is featured on any two consecutive days (for both kittens and puppies)
for d in range(6):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Any breed featured on day 1 is not featured on day 7
# Day 1 = day0, day 7 = day6
# For kittens: the breed on day1 is not on day7
solver.add(kitten[0] != kitten[6])
# For puppies: the breed on day1 is not on day7
solver.add(puppy[0] != puppy[6])

# Himalayans are featured on exactly three days, but not on day 1
# Himalayan = 0
solver.add(kitten[0] != 0)
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# Rottweilers are not featured on day 7, nor on any day that features Himalayans
# Rottweiler = 2
solver.add(puppy[6] != 2)
# On any day where kitten is Himalayan (0), puppy cannot be Rottweiler (2)
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Now evaluate each option

# Option A: There are exactly four breeds that are each featured on three days.
# Total breeds: 3 kitten + 3 puppy = 6 breeds. "Exactly four breeds each featured on three days"
# means count of breeds (among the 6) that appear exactly 3 times = 4.
# We need to count for each breed how many days it appears.
opt_a_constr = BoolVal(True)  # placeholder, we'll build it properly
# Let's build: for each breed (kitten 0,1,2 and puppy 0,1,2), count days featured, then count how many have count==3, assert that == 4
kitten_counts = [Sum([If(kitten[d] == b, 1, 0) for d in days]) for b in range(3)]
puppy_counts = [Sum([If(puppy[d] == b, 1, 0) for d in days]) for b in range(3)]
all_counts = kitten_counts + puppy_counts
# Count how many breeds have count == 3
opt_a_constr = (Sum([If(c == 3, 1, 0) for c in all_counts]) == 4)

# Option B: Greyhounds are featured on every day that Himalayans are.
# Greyhound = 0, Himalayan = 0
# For every day d, if kitten[d] == 0 (Himalayan), then puppy[d] == 0 (Greyhound)
opt_b_constr = And([Implies(kitten[d] == 0, puppy[d] == 0) for d in days])

# Option C: Himalayans are featured on every day that Greyhounds are.
# For every day d, if puppy[d] == 0 (Greyhound), then kitten[d] == 0 (Himalayan)
opt_c_constr = And([Implies(puppy[d] == 0, kitten[d] == 0) for d in days])

# Option D: Himalayans are featured on every day that Rottweilers are not.
# Rottweiler = 2. For every day d, if puppy[d] != 2 (not Rottweiler), then kitten[d] == 0 (Himalayan)
opt_d_constr = And([Implies(puppy[d] != 2, kitten[d] == 0) for d in days])

# Option E: Rottweilers are featured on every day that Himalayans are not.
# For every day d, if kitten[d] != 0 (not Himalayan), then puppy[d] == 2 (Rottweiler)
opt_e_constr = And([Implies(kitten[d] != 0, puppy[d] == 2) for d in days])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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