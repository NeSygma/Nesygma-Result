from z3 import *

# Constants
DAYS = 7
H, M, S = 0, 1, 2
G, N, R = 0, 1, 2

# Variables
# K[t] is kitten breed on day t (0-indexed, so 0-6)
# P[t] is puppy breed on day t (0-indexed, so 0-6)
K = [Int(f'K_{t}') for t in range(DAYS)]
P = [Int(f'P_{t}') for t in range(DAYS)]

solver = Solver()

# Domains
for t in range(DAYS):
    solver.add(K[t] >= 0, K[t] <= 2)
    solver.add(P[t] >= 0, P[t] <= 2)

# C1: Greyhounds are featured on day 1.
solver.add(P[0] == G)

# C2: No breed is featured on any two consecutive days.
for t in range(DAYS - 1):
    solver.add(K[t] != K[t+1])
    solver.add(P[t] != P[t+1])

# C3: Any breed featured on day 1 is not featured on day 7.
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# C4: Himalayans are featured on exactly three days, but not on day 1.
solver.add(Sum([If(K[t] == H, 1, 0) for t in range(DAYS)]) == 3)
solver.add(K[0] != H)

# C5: Rottweilers are not featured on day 7.
solver.add(P[6] != R)

# C6: Rottweilers are not featured on any day that features Himalayans.
for t in range(DAYS):
    solver.add(Implies(P[t] == R, K[t] != H))

# Answer Choices
# (A) Greyhounds and Siamese are both featured on day 2.
# (B) Greyhounds and Himalayans are both featured on day 7.
# (C) Rottweilers and Himalayans are both featured on day 4.
# (D) Rottweilers and Manx are both featured on day 5.
# (E) Newfoundlands and Manx are both featured on day 6.

options = [
    ("A", And(P[1] == G, K[1] == S)),
    ("B", And(P[6] == G, K[6] == H)),
    ("C", And(P[3] == R, K[3] == H)),
    ("D", And(P[4] == R, K[4] == M)),
    ("E", And(P[5] == N, K[5] == M))
]

found_options = []
for letter, constr in options:
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