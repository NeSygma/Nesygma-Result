from z3 import *

solver = Solver()

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

kitten = [Int(f'kitten_{d}') for d in range(1, 8)]  # 1-indexed
puppy = [Int(f'puppy_{d}') for d in range(1, 8)]    # 1-indexed

# Domain constraints
for d in range(1, 8):
    solver.add(And(kitten[d-1] >= 0, kitten[d-1] <= 2))
    solver.add(And(puppy[d-1] >= 0, puppy[d-1] <= 2))

# 1. Greyhounds are featured on day 1
solver.add(puppy[0] == 0)

# 2. No breed is featured on any two consecutive days
for d in range(1, 7):
    solver.add(kitten[d-1] != kitten[d])
    solver.add(puppy[d-1] != puppy[d])

# 3. Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# 4. Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([If(kitten[d-1] == 0, 1, 0) for d in range(1, 8)]) == 3)
solver.add(kitten[0] != 0)

# 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != 2)
for d in range(1, 8):
    # If kitten on day d is Himalayan, then puppy on day d is not Rottweiler
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Additional condition from question: Himalayans are not featured on day 7
solver.add(kitten[6] != 0)

# Now test each option pair
# Each option asks about a pair of days (day X and day Y) featuring both the same breed of kitten
# and the same breed of puppy.

options = [
    ("A", (1, 3)),
    ("B", (2, 6)),
    ("C", (3, 5)),
    ("D", (4, 6)),
    ("E", (5, 7))
]

found_options = []

for letter, (day_a, day_b) in options:
    solver.push()
    # Constraint: day_a and day_b feature the same kitten breed AND the same puppy breed
    solver.add(And(kitten[day_a-1] == kitten[day_b-1], puppy[day_a-1] == puppy[day_b-1]))
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