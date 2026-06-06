from z3 import *

solver = Solver()

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Batches: O1, O2, O3, P1, P2, P3, S1, S2, S3
O = [Int(f'O{i}') for i in range(1, 4)]
P = [Int(f'P{i}') for i in range(1, 4)]
S = [Int(f'S{i}') for i in range(1, 4)]

all_batches = O + P + S

# Domain: 0 to 4
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# Constraint: No two batches of the same kind on the same day
solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))

# Constraint: At least one batch on Monday (0)
solver.add(Or([b == 0 for b in all_batches]))

# Constraint: O2 = P1
solver.add(O[1] == P[0])

# Constraint: S2 = Thursday (3)
solver.add(S[1] == 3)

# Constraint: Number of batches on Friday (4) is exactly 1
solver.add(Sum([If(b == 4, 1, 0) for b in all_batches]) == 1)

# Options
options = [
    ("A", O[0] == 0), # Wait, A is "The first batch of sugar cookies is made on Monday" -> S[0] == 0
    ("B", O[0] == 1),
    ("C", O[2] == 4),
    ("D", P[0] == 2),
    ("E", P[1] == 1)
]

# Correcting Option A: "The first batch of sugar cookies is made on Monday"
options[0] = ("A", S[0] == 0)

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")