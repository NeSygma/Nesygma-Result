from z3 import *

solver = Solver()

# Days 1..7 indexed 0..6
K = [Int(f'K{i+1}') for i in range(7)]  # kitten breed: 0=H,1=M,2=S
P = [Int(f'P{i+1}') for i in range(7)]  # puppy breed: 0=G,1=N,2=R

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
# Day1 breed not on day7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])
# Himalayans exactly three days, not on day1
solver.add(Sum([If(K[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(K[0] != 0)
# Additional condition: Himalayans not on day2
solver.add(K[1] != 0)
# Rottweilers not on day7
solver.add(P[6] != 2)
# Rottweilers not on any day with Himalayans
for i in range(7):
    solver.add(Implies(K[i] == 0, P[i] != 2))

# Define option constraints
opt_a = K[2] == 1  # Manx on day3
opt_b = K[3] == 2  # Siamese on day4
opt_c = P[4] == 2  # Rottweilers on day5
opt_d = K[5] == 0  # Himalayans on day6
opt_e = P[6] == 0  # Greyhounds on day7

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