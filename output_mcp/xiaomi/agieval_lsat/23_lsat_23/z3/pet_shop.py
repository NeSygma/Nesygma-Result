from z3 import *

solver = Solver()

# Days 1-7
days = range(1, 8)

# Kitten breeds: H=Himalayan, M=Manx, S=Siamese
# Puppy breeds: G=Greyhound, N=Newfoundland, R=Rottweiler

# Variables: kitten[d] and puppy[d] for each day d
kitten = {d: Int(f'kitten_{d}') for d in days}
puppy = {d: Int(f'puppy_{d}') for d in days}

# Domain: 0=Himalayan, 1=Manx, 2=Siamese for kittens
#         0=Greyhound, 1=Newfoundland, 2=Rottweiler for puppies
for d in days:
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Condition 1: Greyhounds are featured on day 1
solver.add(puppy[1] == 0)

# Condition 2: No breed is featured on any two consecutive days
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Condition 3: Any breed featured on day 1 is not featured on day 7
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Condition 4: Himalayans are featured on exactly three days, but not on day 1
solver.add(kitten[1] != 0)  # Not on day 1
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in days]) == 3)

# Condition 5: Rottweilers are not featured on day 7
solver.add(puppy[7] != 2)

# Condition 6: Rottweilers are not featured on any day that features Himalayans
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Now evaluate each option
found_options = []

# Option A: There are exactly four breeds that are each featured on three days.
# We need to count how many breeds (out of 6 total) are featured on exactly 3 days.
breed_counts = []
for b in range(3):  # kitten breeds
    breed_counts.append(Sum([If(kitten[d] == b, 1, 0) for d in days]))
for b in range(3):  # puppy breeds
    breed_counts.append(Sum([If(puppy[d] == b, 1, 0) for d in days]))

opt_a_constr = (Sum([If(bc == 3, 1, 0) for bc in breed_counts]) == 4)

# Option B: Greyhounds are featured on every day that Himalayans are.
# For all days: if kitten[d]==0 (Himalayan) then puppy[d]==0 (Greyhound)
opt_b_constr = And([Implies(kitten[d] == 0, puppy[d] == 0) for d in days])

# Option C: Himalayans are featured on every day that Greyhounds are.
# For all days: if puppy[d]==0 (Greyhound) then kitten[d]==0 (Himalayan)
opt_c_constr = And([Implies(puppy[d] == 0, kitten[d] == 0) for d in days])

# Option D: Himalayans are featured on every day that Rottweilers are not.
# For all days: if puppy[d]!=2 (not Rottweiler) then kitten[d]==0 (Himalayan)
opt_d_constr = And([Implies(puppy[d] != 2, kitten[d] == 0) for d in days])

# Option E: Rottweilers are featured on every day that Himalayans are not.
# For all days: if kitten[d]!=0 (not Himalayan) then puppy[d]==2 (Rottweiler)
opt_e_constr = And([Implies(kitten[d] != 0, puppy[d] == 2) for d in days])

options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]

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