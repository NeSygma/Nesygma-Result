from z3 import *

# Define constants for breeds
K_H, K_M, K_S = 0, 1, 2  # kitten breeds: Himalayan, Manx, Siamese
P_G, P_N, P_R = 0, 1, 2  # puppy breeds: Greyhound, Newfoundland, Rottweiler

solver = Solver()

# Variables for each day (1..7) indexed 0..6
K = [Int(f'K{i+1}') for i in range(7)]
P = [Int(f'P{i+1}') for i in range(7)]

# Domain constraints
for i in range(7):
    solver.add(Or(K[i] == K_H, K[i] == K_M, K[i] == K_S))
    solver.add(Or(P[i] == P_G, P[i] == P_N, P[i] == P_R))

# Base constraints
solver.add(P[0] == P_G)  # Greyhounds on day 1
# No breed consecutive days
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])
# Day1 breed not on day7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])
# Himalayans exactly three days, not on day1
solver.add(Sum([If(K[i] == K_H, 1, 0) for i in range(7)]) == 3)
solver.add(K[0] != K_H)
# Rottweilers not on day7
solver.add(P[6] != P_R)
# Rottweilers not on any day with Himalayans
for i in range(7):
    solver.add(Or(K[i] != K_H, P[i] != P_R))
# Additional condition for the question: Himalayans not on day7
solver.add(K[6] != K_H)

# Define option constraints
opt_a_constr = And(P[2] == P_G, P[4] == P_G)  # days 3 and 5 Greyhounds
opt_b_constr = P[2] == P_N               # day 3 Newfoundland
opt_c_constr = P[5] == P_R               # day 6 Rottweiler
opt_d_constr = And(P[2] == P_R, And([P[i] != P_R for i in range(7) if i != 2]))
opt_e_constr = Sum([If(P[i] == P_R, 1, 0) for i in range(7)]) == 3

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