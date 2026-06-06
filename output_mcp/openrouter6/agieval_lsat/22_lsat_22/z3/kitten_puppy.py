from z3 import *

solver = Solver()

# Variables
kitten = [Int(f'k_{i}') for i in range(7)]
puppy = [Int(f'p_{i}') for i in range(7)]

# Domain constraints
for i in range(7):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# 1. Greyhounds on day 1
solver.add(puppy[0] == 0)  # 0 = Greyhound

# 2. No breed on consecutive days
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed on day 1 not on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])  # implies puppy[6] != 0

# 4. Himalayans exactly 3 days, not on day 1
sum_H = Sum([If(kitten[i] == 0, 1, 0) for i in range(7)])
solver.add(sum_H == 3)
solver.add(kitten[0] != 0)

# 5. Rottweilers not on day 7, and not on any day with Himalayans
solver.add(puppy[6] != 2)  # 2 = Rottweiler
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))

# Additional condition from question: Himalayans not on day 7
solver.add(kitten[6] != 0)

# Check base satisfiability (optional, but good for debugging)
# if solver.check() != sat:
#     print("Base constraints unsatisfiable")
#     exit()

# Options: (letter, (day_index1, day_index2))
options = [
    ("A", (0, 2)),  # day 1 and day 3
    ("B", (1, 5)),  # day 2 and day 6
    ("C", (2, 4)),  # day 3 and day 5
    ("D", (3, 5)),  # day 4 and day 6
    ("E", (4, 6))   # day 5 and day 7
]

found_options = []
for letter, (i, j) in options:
    solver.push()
    # Add condition: same kitten and same puppy on these two days
    solver.add(kitten[i] == kitten[j])
    solver.add(puppy[i] == puppy[j])
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