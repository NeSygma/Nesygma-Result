from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Days are 0-indexed for Python, representing days 1-7
# kitten[i] = 0: Himalayan, 1: Manx, 2: Siamese
# puppy[i] = 0: Greyhound, 1: Newfoundland, 2: Rottweiler
kitten = [Int(f'kitten_{i}') for i in range(7)]
puppy = [Int(f'puppy_{i}') for i in range(7)]

# Domains: breeds are 0, 1, 2
for i in range(7):
    solver.add(kitten[i] >= 0, kitten[i] <= 2)
    solver.add(puppy[i] >= 0, puppy[i] <= 2)

# 1. Greyhounds are featured on day 1 (day 0 in 0-index)
solver.add(puppy[0] == 0)

# 2. No breed is featured on any two consecutive days
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
# We interpret this as: for each breed b, if kitten[0]==b or puppy[0]==b, then kitten[6]!=b and puppy[6]!=b
for b in range(3):
    solver.add(Implies(kitten[0] == b, kitten[6] != b))
    solver.add(Implies(puppy[0] == b, puppy[6] != b))

# 4. Himalayans are featured on exactly three days, but not on day 1
solver.add(Sum([kitten[i] == 0 for i in range(7)]) == 3)
solver.add(kitten[0] != 0)

# 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != 2)  # Rottweilers not on day 7
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))  # Rottweilers not on Himalayan days

# 6. Himalayans are not featured on day 7 (given in the question)
solver.add(kitten[6] != 0)

# Base constraints are set. Now evaluate the multiple-choice options.
# For each option, we will add constraints that the two days have the same kitten and puppy breeds.
# The correct answer is the option that is UNSATISFIABLE.

found_options = []

# Option A: day 1 and day 3 (0-indexed: 0 and 2)
opt_a_constr = And(kitten[0] == kitten[2], puppy[0] == puppy[2])
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: day 2 and day 6 (0-indexed: 1 and 5)
opt_b_constr = And(kitten[1] == kitten[5], puppy[1] == puppy[5])
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: day 3 and day 5 (0-indexed: 2 and 4)
opt_c_constr = And(kitten[2] == kitten[4], puppy[2] == puppy[4])
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: day 4 and day 6 (0-indexed: 3 and 5)
opt_d_constr = And(kitten[3] == kitten[5], puppy[3] == puppy[5])
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: day 5 and day 7 (0-indexed: 4 and 6)
opt_e_constr = And(kitten[4] == kitten[6], puppy[4] == puppy[6])
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")