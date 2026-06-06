from z3 import *

solver = Solver()

# Days 1-7
days = range(1, 8)

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
kitten = [Int(f'kitten_{d}') for d in days]
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
puppy = [Int(f'puppy_{d}') for d in days]

# Domain constraints
for d in days:
    solver.add(Or(kitten[d-1] == 0, kitten[d-1] == 1, kitten[d-1] == 2))
    solver.add(Or(puppy[d-1] == 0, puppy[d-1] == 1, puppy[d-1] == 2))

# Greyhounds are featured on day 1
solver.add(puppy[0] == 0)

# No breed is featured on any two consecutive days
for d in range(1, 7):
    solver.add(kitten[d-1] != kitten[d])
    solver.add(puppy[d-1] != puppy[d])

# Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Himalayans are featured on exactly three days, but not on day 1
solver.add(kitten[0] != 0)  # Not on day 1
solver.add(Sum([If(kitten[d-1] == 0, 1, 0) for d in days]) == 3)

# Rottweilers are not featured on day 7
solver.add(puppy[6] != 2)
# Rottweilers are not featured on any day that features Himalayans
for d in days:
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Define option constraints for kitten sequences
# (A) Himalayan, Manx, Siamese, Himalayan, Manx, Himalayan, Siamese
opt_a = And(kitten[0]==0, kitten[1]==1, kitten[2]==2, kitten[3]==0, kitten[4]==1, kitten[5]==0, kitten[6]==2)
# (B) Manx, Himalayan, Siamese, Himalayan, Manx, Himalayan, Manx
opt_b = And(kitten[0]==1, kitten[1]==0, kitten[2]==2, kitten[3]==0, kitten[4]==1, kitten[5]==0, kitten[6]==1)
# (C) Manx, Himalayan, Manx, Himalayan, Siamese, Manx, Siamese
opt_c = And(kitten[0]==1, kitten[1]==0, kitten[2]==1, kitten[3]==0, kitten[4]==2, kitten[5]==1, kitten[6]==2)
# (D) Siamese, Himalayan, Manx, Himalayan, Siamese, Siamese, Himalayan
opt_d = And(kitten[0]==2, kitten[1]==0, kitten[2]==1, kitten[3]==0, kitten[4]==2, kitten[5]==2, kitten[6]==0)
# (E) Siamese, Himalayan, Siamese, Himalayan, Manx, Siamese, Himalayan
opt_e = And(kitten[0]==2, kitten[1]==0, kitten[2]==2, kitten[3]==0, kitten[4]==1, kitten[5]==2, kitten[6]==0)

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