from z3 import *

# Define breeds
H, M, S = 0, 1, 2
G, N, R = 0, 1, 2

# Days 1-7
# Kitten breeds: K[0] to K[6]
# Puppy breeds: P[0] to P[6]

solver = Solver()

K = [Int(f'K_{i}') for i in range(7)]
P = [Int(f'P_{i}') for i in range(7)]

# Domains
for i in range(7):
    solver.add(K[i] >= 0, K[i] <= 2)
    solver.add(P[i] >= 0, P[i] <= 2)

# 1. Greyhounds are featured on day 1.
solver.add(P[0] == G)

# 2. No breed is featured on any two consecutive days.
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])

# 3. Any breed featured on day 1 is not featured on day 7.
solver.add(K[0] != K[6])
solver.add(P[0] != P[6])

# 4. Himalayans are featured on exactly three days, but not on day 1.
solver.add(Sum([If(K[i] == H, 1, 0) for i in range(7)]) == 3)
solver.add(K[0] != H)

# 5. Rottweilers are not featured on day 7.
solver.add(P[6] != R)

# 6. Rottweilers are not featured on any day that features Himalayans.
for i in range(7):
    solver.add(Implies(K[i] == H, P[i] != R))

# Options for K
# (A) H, M, S, H, M, H, S
# (B) M, H, S, H, M, H, M
# (C) M, H, M, H, S, M, S
# (D) S, H, M, H, S, S, H
# (E) S, H, S, H, M, S, H

options = [
    ("A", [H, M, S, H, M, H, S]),
    ("B", [M, H, S, H, M, H, M]),
    ("C", [M, H, M, H, S, M, S]),
    ("D", [S, H, M, H, S, S, H]),
    ("E", [S, H, S, H, M, S, H])
]

found_options = []
for letter, k_seq in options:
    solver.push()
    # Add constraint for this specific kitten sequence
    for i in range(7):
        solver.add(K[i] == k_seq[i])
    
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