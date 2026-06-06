from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for kitten and puppy breeds
# 0: Himalayan, 1: Manx, 2: Siamese (for kittens)
# 0: Greyhound, 1: Newfoundland, 2: Rottweiler (for puppies)
kitten = [Int(f'kitten_{i}') for i in range(7)]
puppy = [Int(f'puppy_{i}') for i in range(7)]

solver = Solver()

# Constraint 1: Greyhounds are featured on day 1
solver.add(puppy[0] == 0)

# Constraint 2: No breed is featured on any two consecutive days
for i in range(6):
    solver.add(kitten[i] != kitten[i+1])
    solver.add(puppy[i] != puppy[i+1])

# Constraint 3: Any breed featured on day 1 is not featured on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# Constraint 4: Himalayans are featured on exactly three days, but not on day 1
# Count Himalayans (0) in kitten array, excluding day 1
solver.add(Sum([If(kitten[i] == 0, 1, 0) for i in range(1, 7)]) == 3)

# Constraint 5: Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != 2)  # Rottweiler not on day 7
for i in range(7):
    solver.add(Implies(kitten[i] == 0, puppy[i] != 2))  # No Rottweiler on Himalayan days

# Additional condition: Himalayans are not featured on day 2
solver.add(kitten[1] != 0)

# Base constraints are now set up
# Now evaluate each multiple-choice option

# Define the options as constraints
# (A) Manx are featured on day 3
opt_a_constr = (kitten[2] == 1)

# (B) Siamese are featured on day 4
opt_b_constr = (kitten[3] == 2)

# (C) Rottweilers are featured on day 5
opt_c_constr = (puppy[4] == 2)

# (D) Himalayans are featured on day 6
opt_d_constr = (kitten[5] == 0)

# (E) Greyhounds are featured on day 7
opt_e_constr = (puppy[6] == 0)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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