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

# Let's check if there's a constraint I missed.
# "No two batches of the same kind of cookie are made on the same day."
# This is already covered by Distinct(O), Distinct(P), Distinct(S).

# Maybe there's a constraint on the total number of batches per day?
# "Exactly three batches of each kind of cookie are made each week"
# 9 batches total, 5 days. 9/5 = 1.8.
# Maybe there's a limit on the total number of batches per day?
# The problem doesn't say.

# Let's re-check the options.
# (A) S1 = Monday (0)
# (B) O1 = Tuesday (1)
# (C) O3 = Friday (4)
# (D) P1 = Wednesday (2)
# (E) P2 = Tuesday (1)

# Let's print a model for each option to see if they are indeed possible.
for letter, constr in [("A", S[0] == 0), ("B", O[0] == 1), ("C", O[2] == 4), ("D", P[0] == 2), ("E", P[1] == 1)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        print(f"Option {letter} is possible.")
        print(solver.model())
    else:
        print(f"Option {letter} is NOT possible.")
    solver.pop()