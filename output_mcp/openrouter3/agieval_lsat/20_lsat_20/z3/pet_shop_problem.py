from z3 import *

# Days: 1-7
days = range(1, 8)

# Kitten breeds: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy breeds: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

# Create symbolic variables for each day
kitten = [Int(f'kitten_{d}') for d in days]
puppy = [Int(f'puppy_{d}') for d in days]

solver = Solver()

# Domain constraints: each variable must be in {0,1,2}
for d in days:
    solver.add(kitten[d-1] >= 0, kitten[d-1] <= 2)
    solver.add(puppy[d-1] >= 0, puppy[d-1] <= 2)

# Constraint 1: Greyhounds (0) on day 1
solver.add(puppy[0] == 0)

# Constraint 2: No breed featured on two consecutive days
# For kittens
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
# For puppies
for i in range(6):
    solver.add(puppy[i] != puppy[i+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
# For kittens: kitten on day 1 != kitten on day 7
solver.add(kitten[0] != kitten[6])
# For puppies: puppy on day 1 != puppy on day 7
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans (0) featured on exactly 3 days, but not on day 1
# Count Himalayan days
himalayan_count = Sum([If(kitten[d-1] == 0, 1, 0) for d in days])
solver.add(himalayan_count == 3)
solver.add(kitten[0] != 0)  # Not on day 1

# Constraint 5: Rottweilers (2) not on day 7, and not on any day that features Himalayans
solver.add(puppy[6] != 2)  # Not on day 7
# Not on any day that features Himalayans
for d in days:
    solver.add(Implies(kitten[d-1] == 0, puppy[d-1] != 2))

# Additional condition: Himalayans not on day 2
solver.add(kitten[1] != 0)

# Now evaluate each answer choice
# Answer choices:
# (A) Manx are featured on day 3. (Manx = 1, day 3 = index 2)
# (B) Siamese are featured on day 4. (Siamese = 2, day 4 = index 3)
# (C) Rottweilers are featured on day 5. (Rottweilers = 2, day 5 = index 4)
# (D) Himalayans are featured on day 6. (Himalayan = 0, day 6 = index 5)
# (E) Greyhounds are featured on day 7. (Greyhound = 0, day 7 = index 6)

found_options = []

# Test option A: Manx on day 3
solver.push()
solver.add(kitten[2] == 1)  # Manx on day 3
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Test option B: Siamese on day 4
solver.push()
solver.add(kitten[3] == 2)  # Siamese on day 4
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Test option C: Rottweilers on day 5
solver.push()
solver.add(puppy[4] == 2)  # Rottweilers on day 5
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Test option D: Himalayans on day 6
solver.push()
solver.add(kitten[5] == 0)  # Himalayans on day 6
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Test option E: Greyhounds on day 7
solver.push()
solver.add(puppy[6] == 0)  # Greyhounds on day 7
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")