from z3 import *

solver = Solver()

# Days 1-7
# kitten[d] ∈ {0=Himalayan, 1=Manx, 2=Siamese}
# puppy[d] ∈ {0=Greyhound, 1=Newfoundland, 2=Rottweiler}
kitten = [Int(f'kitten_{d}') for d in range(8)]  # index 1..7
puppy = [Int(f'puppy_{d}') for d in range(8)]    # index 1..7

# Domain constraints
for d in range(1, 8):
    solver.add(And(kitten[d] >= 0, kitten[d] <= 2))
    solver.add(And(puppy[d] >= 0, puppy[d] <= 2))

# Constraint 1: Greyhounds featured on day 1
solver.add(puppy[1] == 0)

# Constraint 2: No breed featured on two consecutive days
for d in range(1, 7):
    solver.add(kitten[d] != kitten[d+1])
    solver.add(puppy[d] != puppy[d+1])

# Constraint 3: Any breed on day 1 not on day 7
solver.add(kitten[1] != kitten[7])
solver.add(puppy[1] != puppy[7])

# Constraint 4: Himalayans on exactly 3 days, not on day 1
solver.add(kitten[1] != 0)
solver.add(Sum([If(kitten[d] == 0, 1, 0) for d in range(1, 8)]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day with Himalayans
solver.add(puppy[7] != 2)
for d in range(1, 8):
    solver.add(Implies(kitten[d] == 0, puppy[d] != 2))

# Additional condition: Himalayans not on day 7
solver.add(kitten[7] != 0)

# Now check each option
# Option: pair (d1, d2) CANNOT feature both same kitten AND same puppy
# We check if it's POSSIBLE for each pair. The impossible one is the answer.

options = [
    ("A", 1, 3),
    ("B", 2, 6),
    ("C", 3, 5),
    ("D", 4, 6),
    ("E", 5, 7),
]

found_options = []
for letter, d1, d2 in options:
    solver.push()
    # Add constraint: same kitten AND same puppy on both days
    solver.add(kitten[d1] == kitten[d2])
    solver.add(puppy[d1] == puppy[d2])
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