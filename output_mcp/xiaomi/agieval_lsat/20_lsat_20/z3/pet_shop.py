from z3 import *

solver = Solver()

# Variables: kitten[i] and puppy[i] for days 1-7 (index 0-6)
# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

kitten = [Int(f'kitten_{i}') for i in range(7)]
puppy = [Int(f'puppy_{i}') for i in range(7)]

# Domain constraints
for i in range(7):
    solver.add(And(kitten[i] >= 0, kitten[i] <= 2))
    solver.add(And(puppy[i] >= 0, puppy[i] <= 2))

# Constraint 1: Greyhounds on day 1
solver.add(puppy[0] == 0)

# Constraint 2: No breed on two consecutive days
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Constraint 3: Any breed on day 1 is not on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans on exactly 3 days, not on day 1
solver.add(kitten[0] != 0)  # Not on day 1
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(7)]) == 3)

# Constraint 5: Rottweilers not on day 7, nor on any day with Himalayans
solver.add(puppy[6] != 2)  # Not on day 7
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Additional condition: Himalayans not on day 2
solver.add(kitten[1] != 0)

# Define option constraints
opt_a = (kitten[2] == 1)  # Manx on day 3
opt_b = (kitten[3] == 2)  # Siamese on day 4
opt_c = (puppy[4] == 2)   # Rottweilers on day 5
opt_d = (kitten[5] == 0)  # Himalayans on day 6
opt_e = (puppy[6] == 0)   # Greyhounds on day 7

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