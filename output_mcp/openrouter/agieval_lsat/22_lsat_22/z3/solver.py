from z3 import *

solver = Solver()

# Define variables for 7 days
K = [Int(f'K{i}') for i in range(1,8)]  # kitten breed per day
P = [Int(f'P{i}') for i in range(1,8)]  # puppy breed per day

# Domains: 0=Himalayan,1=Manx,2=Siamese for kittens; 0=Greyhound,1=Newfoundland,2=Rottweiler for puppies
for i in range(7):
    solver.add(And(K[i] >= 0, K[i] <= 2))
    solver.add(And(P[i] >= 0, P[i] <= 2))

# Greyhounds on day 1
solver.add(P[0] == 0)  # 0 = Greyhound

# No breed consecutive days (both kitten and puppy)
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])

# Any breed on day1 not on day7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# Himalayans exactly three days, not on day1
solver.add(Sum([If(K[i] == 0, 1, 0) for i in range(7)]) == 3)
solver.add(K[0] != 0)

# Rottweilers not on day7, nor on any day with Himalayans
solver.add(P[6] != 2)  # 2 = Rottweiler
for i in range(7):
    solver.add(Implies(K[i] == 0, P[i] != 2))

# Premise: Himalayans not on day7
solver.add(K[6] != 0)

# Define option constraints
options = {
    "A": (1, 3),
    "B": (2, 6),
    "C": (3, 5),
    "D": (4, 6),
    "E": (5, 7)
}

found_options = []
for letter, (d1, d2) in options.items():
    # convert to 0-index
    i1, i2 = d1-1, d2-1
    opt_constr = And(K[i1] == K[i2], P[i1] == P[i2])
    solver.push()
    solver.add(opt_constr)
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