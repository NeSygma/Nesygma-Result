from z3 import *

solver = Solver()

# Enumerations
# Kitten: 0=Himalayan,1=Manx,2=Siamese
# Puppy: 0=Greyhound,1=Newfoundland,2=Rottweiler
K = [Int(f'K{i}') for i in range(1,8)]  # days 1..7
P = [Int(f'P{i}') for i in range(1,8)]

# Domain constraints
for i in range(7):
    solver.add(And(K[i] >= 0, K[i] <= 2))
    solver.add(And(P[i] >= 0, P[i] <= 2))

# Base constraints
# Greyhounds on day1
solver.add(P[0] == 0)
# No breed consecutive days
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])
# Any breed on day1 not on day7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])
# Himalayans exactly three days, not on day1
solver.add(Sum([If(K[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(K[0] != 0)
# Rottweilers not on day7
solver.add(P[6] != 2)
# Rottweilers not on any day that features Himalayans
for i in range(7):
    solver.add(Implies(K[i] == 0, P[i] != 2))

# Define option constraints
opt_a = And(P[1] == 0, K[1] == 2)  # day2 Greyhound (0) and Siamese (2)
opt_b = And(P[6] == 0, K[6] == 0)  # day7 Greyhound and Himalayan
opt_c = And(P[3] == 2, K[3] == 0)  # day4 Rottweiler and Himalayan
opt_d = And(P[4] == 2, K[4] == 1)  # day5 Rottweiler and Manx
opt_e = And(P[5] == 1, K[5] == 1)  # day6 Newfoundland and Manx

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