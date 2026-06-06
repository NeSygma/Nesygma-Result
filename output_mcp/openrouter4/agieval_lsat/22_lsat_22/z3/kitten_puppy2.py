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
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Additional condition from question: Himalayans are not featured on day 7
solver.add(kitten[6] != 0)

# Now test each option pair.
# The question asks: which pair of days CANNOT feature both the same breed of kitten
# and the same breed of puppy?
# So we check: for each pair, can they have same kitten AND same puppy?
# The pair that CANNOT satisfy this is the answer (the one that returns unsat).

options = [
    ("A", (1, 3)),
    ("B", (2, 6)),
    ("C", (3, 5)),
    ("D", (4, 6)),
    ("E", (5, 7))
]

impossible_options = []

for letter, (day_a, day_b) in options:
    solver.push()
    # Constraint: day_a and day_b feature the same kitten breed AND the same puppy breed
    solver.add(And(kitten[day_a-1] == kitten[day_b-1], puppy[day_a-1] == puppy[day_b-1]))
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

# The pair that CANNOT have same breeds is the one that returns unsat when we try
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found (all pairs can have same breeds)")