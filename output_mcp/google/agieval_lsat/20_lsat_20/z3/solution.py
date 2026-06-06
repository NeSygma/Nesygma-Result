from z3 import *

# Constants
DAYS = 7
# Kitten breeds: 0: Himalayan, 1: Manx, 2: Siamese
# Puppy breeds: 0: Greyhound, 1: Newfoundland, 2: Rottweiler

kitten = [Int(f'kitten_{i}') for i in range(DAYS)]
puppy = [Int(f'puppy_{i}') for i in range(DAYS)]

solver = Solver()

# Domains
for i in range(DAYS):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# 1. Greyhounds are featured on day 1.
solver.add(puppy[0] == 0)

# 2. No breed is featured on any two consecutive days.
for i in range(DAYS - 1):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed featured on day 1 is not featured on day 7.
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# 4. Himalayans are featured on exactly three days, but not on day 1.
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(DAYS)]) == 3)
solver.add(kitten[0] != 0)

# 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans.
solver.add(puppy[6] != 2)
for i in range(DAYS):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Question: If Himalayans are not featured on day 2
solver.add(kitten[1] != 0)

# Options
options = [
    ("A", kitten[2] == 1), # Manx on day 3
    ("B", kitten[3] == 2), # Siamese on day 4
    ("C", puppy[4] == 2),  # Rottweiler on day 5
    ("D", kitten[5] == 0), # Himalayan on day 6
    ("E", puppy[6] == 0)   # Greyhound on day 7
]

found_options = []
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