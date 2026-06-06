from z3 import *

# Days 0-6
days = 7
# Kitten breeds: 0: H, 1: M, 2: S
# Puppy breeds: 0: G, 1: N, 2: R
K = [Int(f'K_{i}') for i in range(days)]
P = [Int(f'P_{i}') for i in range(days)]

solver = Solver()

# Domains
for i in range(days):
    solver.add(K[i] >= 0, K[i] <= 2)
    solver.add(P[i] >= 0, P[i] <= 2)

# 1. G on day 1 (index 0)
solver.add(P[0] == 0)

# 2. No breed on consecutive days
for i in range(days - 1):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])

# 3. Breed on day 1 != Breed on day 7
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# 4. H (0) on exactly 3 days
solver.add(Sum([If(K[i] == 0, 1, 0) for i in range(days)]) == 3)

# 5. H not on day 1
solver.add(K[0] != 0)

# 6. R (2) not on day 7
solver.add(P[6] != 2)

# 7. R not on any day with H
for i in range(days):
    solver.add(Implies(P[i] == 2, K[i] != 0))

# Question condition: H not on day 7
solver.add(K[6] != 0)

# Options
options = [
    ("A", And(P[2] == 0, P[4] == 0)),
    ("B", P[2] == 1),
    ("C", P[5] == 2),
    ("D", And(P[2] == 2, P[0] != 2, P[1] != 2, P[3] != 2, P[4] != 2, P[5] != 2, P[6] != 2)),
    ("E", Sum([If(P[i] == 2, 1, 0) for i in range(days)]) == 3)
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