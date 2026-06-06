from z3 import *

solver = Solver()

# Variables for each day: kitten (0=H,1=M,2=S) and puppy (0=G,1=N,2=R)
K = [Int(f'K{i}') for i in range(1,8)]
P = [Int(f'P{i}') for i in range(1,8)]

# Domains
for i in range(7):
    solver.add(And(K[i] >= 0, K[i] <= 2))
    solver.add(And(P[i] >= 0, P[i] <= 2))

# Greyhounds on day1
solver.add(P[0] == 0)

# No breed on consecutive days
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
solver.add(P[6] != 2)
for i in range(7):
    solver.add(Implies(K[i] == 0, P[i] != 2))

# Premise: Himalayans not on day7
solver.add(K[6] != 0)

# Options mapping
options = {
    "A": (1,3),
    "B": (2,6),
    "C": (3,5),
    "D": (4,6),
    "E": (5,7)
}

unsat_options = []
for letter, (d1,d2) in options.items():
    i1, i2 = d1-1, d2-1
    # Constraint that both kitten and puppy are the same on the two days
    same_constraint = And(K[i1] == K[i2], P[i1] == P[i2])
    solver.push()
    solver.add(same_constraint)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options impossible {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")