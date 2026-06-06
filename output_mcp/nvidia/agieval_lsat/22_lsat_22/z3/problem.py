from z3 import *

solver = Solver()

# Variables
k = [Int(f'k{i}') for i in range(7)]  # kitten breed: 0=Himalayan, 1=Manx, 2=Siamese
p = [Int(f'p{i}') for i in range(7)]  # puppy breed: 0=Greyhound, 1=Newfoundland, 2=Rottweiler

# Domain constraints
for i in range(7):
    solver.add(k[i] >= 0, k[i] <= 2)
    solver.add(p[i] >= 0, p[i] <= 2)

# Day1 puppy is Greyhound
solver.add(p[0] == 0)

# No consecutive same kitten
for i in range(6):
    solver.add(k[i] != k[i+1])

# No consecutive same puppy
for i in range(6):
    solver.add(p[i] != p[i+1])

# Any breed on day1 not on day7
solver.add(k[0] != k[6])
solver.add(p[0] != p[6])

# Exactly three Himalayans (kitten==0) and not on day1
solver.add(Sum([If(k[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(k[0] != 0)

# Rottweilers not on day7 nor on any day with Himalayans
solver.add(p[6] != 2)
for i in range(7):
    solver.add(Implies(k[i] == 0, p[i] != 2))

# Himalayans not on day7
solver.add(k[6] != 0)

# Define option constraints (equality of kitten and puppy breeds)
opt_a_constr = And(k[0] == k[2], p[0] == p[2])
opt_b_constr = And(k[1] == k[5], p[1] == p[5])
opt_c_constr = And(k[2] == k[4], p[2] == p[4])
opt_d_constr = And(k[3] == k[5], p[3] == p[5])
opt_e_constr = And(k[4] == k[6], p[4] == p[6])

# Multiple choice evaluation skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
    solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")