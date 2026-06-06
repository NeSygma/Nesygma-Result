from z3 import *

# Days: 1-7
days = range(1, 8)

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

# Variables: kitten[d] and puppy[d] for each day d
kitten = {d: Int(f'kitten_{d}') for d in days}
puppy = {d: Int(f'puppy_{d}') for d in days}

solver = Solver()

# Domain constraints: each variable must be 0, 1, or 2
for d in days:
    solver.add(kitten[d] >= 0, kitten[d] <= 2)
    solver.add(puppy[d] >= 0, puppy[d] <= 2)

# Constraint 1: Greyhounds are featured on day 1
solver.add(puppy[1] == 0)  # Greyhound = 0

# Constraint 2: No breed is featured on any two consecutive days (for kittens and puppies separately)
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
# This applies to both kitten and puppy breeds
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Constraint 4: Himalayans are featured on exactly three days, but not on day 1
# Himalayan = 0
himalayan_count = Sum([If(kitten[d] == 0, 1, 0) for d in days])
solver.add(himalayan_count == 3)
solver.add(kitten[1] != 0)  # not on day 1

# Constraint 5: Rottweilers are not featured on day 7, nor on any day that features Himalayans
# Rottweiler = 2
solver.add(puppy[7] != 2)  # not on day 7
for d in days:
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))  # if Himalayan, then not Rottweiler

# Additional constraint from Q: "If Himalayans are not featured on day 7"
# This is an extra assumption for the question
solver.add(kitten[7] != 0)

# Now, for each option, check if it's possible to have same kitten and same puppy on both days
options = [
    ("A", (1, 3)),
    ("B", (2, 6)),
    ("C", (3, 5)),
    ("D", (4, 6)),
    ("E", (5, 7))
]

found_options = []
for letter, (day1, day2) in options:
    solver.push()
    # Add constraint: same kitten breed AND same puppy breed on both days
    solver.add(kitten[day1] == kitten[day2])
    solver.add(puppy[day1] == puppy[day2])
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