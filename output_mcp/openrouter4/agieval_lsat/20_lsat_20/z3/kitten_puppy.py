from z3 import *

solver = Solver()

# Constants for breeds
# Kitten: 0=Himalayan, 1=Manx, 2=Siamese
# Puppy: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

# Variables for each day (1-indexed, using 0..6 for day indices)
kitten = [Int(f'kitten_{i}') for i in range(7)]
puppy = [Int(f'puppy_{i}') for i in range(7)]

# Domain constraints
for i in range(7):
    solver.add(And(kitten[i] >= 0, kitten[i] <= 2))
    solver.add(And(puppy[i] >= 0, puppy[i] <= 2))

# 1. Greyhounds are featured on day 1.
solver.add(puppy[0] == 0)  # Greyhound = 0

# 2. No breed is featured on any two consecutive days.
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed featured on day 1 is not featured on day 7.
solver.add(kitten[6] != kitten[0])
solver.add(puppy[6] != puppy[0])

# 4. Himalayans are featured on exactly three days, but not on day 1.
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(kitten[0] != 0)  # Himalayan not on day 1

# 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans.
solver.add(puppy[6] != 2)  # Rottweiler not on day 7
# For any day with Himalayan (kitten[i]==0), puppy[i] != 2
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Additional: If Himalayans are not featured on day 2
solver.add(kitten[1] != 0)  # day 2 is index 1

# Now evaluate each option
# (A) Manx are featured on day 3. (day 3 is index 2)
opt_a = (kitten[2] == 1)
# (B) Siamese are featured on day 4. (day 4 is index 3)
opt_b = (kitten[3] == 2)
# (C) Rottweilers are featured on day 5. (day 5 is index 4)
opt_c = (puppy[4] == 2)
# (D) Himalayans are featured on day 6. (day 6 is index 5)
opt_d = (kitten[5] == 0)
# (E) Greyhounds are featured on day 7. (day 7 is index 6)
opt_e = (puppy[6] == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == sat:
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