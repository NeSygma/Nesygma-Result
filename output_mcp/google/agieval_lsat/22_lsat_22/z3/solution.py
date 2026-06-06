from z3 import *

# Constants
DAYS = 7
H, M, S = 0, 1, 2
G, N, R = 0, 1, 2

# Variables
kitten = [Int(f'kitten_{i}') for i in range(DAYS)]
puppy = [Int(f'puppy_{i}') for i in range(DAYS)]

solver = Solver()

# Domains
for i in range(DAYS):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# C1: Greyhounds are featured on day 1.
solver.add(puppy[0] == G)

# C2: No breed is featured on any two consecutive days.
for i in range(DAYS - 1):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# C3: Any breed featured on day 1 is not featured on day 7.
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# C4: Himalayans are featured on exactly three days.
solver.add(Sum([If(kitten[i] == H, 1, 0) for i in range(DAYS)]) == 3)

# C5: Himalayans are not featured on day 1.
solver.add(kitten[0] != H)

# C6: Rottweilers are not featured on day 7.
solver.add(puppy[6] != R)

# C7: Rottweilers are not featured on any day that features Himalayans.
for i in range(DAYS):
    solver.add(Implies(kitten[i] == H, puppy[i] != R))

# Question condition: Himalayans are not featured on day 7.
solver.add(kitten[6] != H)

# Options
options = [
    ("A", 0, 2), # day 1 and day 3
    ("B", 1, 5), # day 2 and day 6
    ("C", 2, 4), # day 3 and day 5
    ("D", 3, 5), # day 4 and day 6
    ("E", 4, 6)  # day 5 and day 7
]

found_options = []
for letter, d1, d2 in options:
    solver.push()
    # The condition we want to test: "can they have the same breed of kitten AND same breed of puppy?"
    # We want to find which one CANNOT.
    # So we check if it's possible to have the same. If it's NOT possible, that's our answer.
    solver.add(kitten[d1] == kitten[d2])
    solver.add(puppy[d1] == puppy[d2])
    
    if solver.check() == unsat:
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