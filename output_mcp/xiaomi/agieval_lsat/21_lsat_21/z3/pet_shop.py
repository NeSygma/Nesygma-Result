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
solver.add(kitten[0] != 0)
solver.add(Sum([If(kitten[d-1] == 0, 1, 0) for d in days]) == 3)

# Rottweilers are not featured on day 7
solver.add(puppy[6] != 2)

# Rottweilers are not featured on any day that features Himalayans
for d in days:
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Now evaluate each option
found_options = []

# (A) Greyhounds and Siamese are both featured on day 2
opt_a = And(puppy[1] == 0, kitten[1] == 2)

# (B) Greyhounds and Himalayans are both featured on day 7
opt_b = And(puppy[6] == 0, kitten[6] == 0)

# (C) Rottweilers and Himalayans are both featured on day 4
opt_c = And(puppy[3] == 2, kitten[3] == 0)

# (D) Rottweilers and Manx are both featured on day 5
opt_d = And(puppy[4] == 2, kitten[4] == 1)

# (E) Newfoundlands and Manx are both featured on day 6
opt_e = And(puppy[5] == 1, kitten[5] == 1)

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