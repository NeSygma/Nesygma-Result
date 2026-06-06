from z3 import *

# Represent kitten breeds as integers: 0=Himalayan, 1=Manx, 2=Siamese
# Represent puppy breeds as integers: 0=Greyhound, 1=Newfoundland, 2=Rottweiler
K = [Int(f'K_{d}') for d in range(1, 8)]
P = [Int(f'P_{d}') for d in range(1, 8)]

solver = Solver()

# Domain constraints: each breed variable must be in {0,1,2}
for d in range(7):
    solver.add(Or([K[d] == i for i in range(3)]))
    solver.add(Or([P[d] == i for i in range(3)]))

# 1. Greyhounds on day 1 (Greyhound = 0)
solver.add(P[0] == 0)

# 2. No breed on consecutive days (for each breed type)
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])

# 3. Any breed on day 1 not on day 7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# 4. Himalayans exactly three days, not on day 1
himalayan_count = Sum([If(K[d] == 0, 1, 0) for d in range(7)])
solver.add(himalayan_count == 3)
solver.add(K[0] != 0)

# 5. Rottweilers not on day 7, nor on any day that features Himalayans
solver.add(P[6] != 2)  # Rottweiler = 2
for d in range(7):
    solver.add(Implies(K[d] == 0, P[d] != 2))

# Define option constraints
# day indices: day 2 -> index 1, day 7 -> index 6, day 4 -> index 3, day 5 -> index 4, day 6 -> index 5
opt_a_constr = And(P[1] == 0, K[1] == 2)  # Greyhounds and Siamese on day 2
opt_b_constr = And(P[6] == 0, K[6] == 0)  # Greyhounds and Himalayans on day 7
opt_c_constr = And(P[3] == 2, K[3] == 0)  # Rottweilers and Himalayans on day 4
opt_d_constr = And(P[4] == 2, K[4] == 1)  # Rottweilers and Manx on day 5
opt_e_constr = And(P[5] == 1, K[5] == 1)  # Newfoundlands and Manx on day 6

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