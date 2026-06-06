from z3 import *

solver = Solver()

# Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

for b in all_batches:
    solver.add(b >= 1, b <= 5)

solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

solver.add(Or([b == 1 for b in all_batches]))
solver.add(O2 == P1)
solver.add(S2 == 4)
solver.add(P1 == 2)

# Option A: Two different kinds have their first batch on Monday
opt_a = Or(
    And(O1 == 1, P1 == 1),
    And(O1 == 1, S1 == 1),
    And(P1 == 1, S1 == 1)
)

# Option B: Two different kinds have their first batch on Tuesday
opt_b = Or(
    And(O1 == 2, P1 == 2),
    And(O1 == 2, S1 == 2),
    And(P1 == 2, S1 == 2)
)

# Option C: Two different kinds have their second batch on Wednesday
opt_c = Or(
    And(O2 == 3, P2 == 3),
    And(O2 == 3, S2 == 3),
    And(P2 == 3, S2 == 3)
)

# Option D: Two different kinds have their second batch on Thursday
opt_d = Or(
    And(O2 == 4, P2 == 4),
    And(O2 == 4, S2 == 4),
    And(P2 == 4, S2 == 4)
)

# Option E: Two different kinds have their third batch on Friday
opt_e = Or(
    And(O3 == 5, P3 == 5),
    And(O3 == 5, S3 == 5),
    And(P3 == 5, S3 == 5)
)

# Find which options CANNOT be true (are UNSAT)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

print(f"Impossible options (CANNOT be true): {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")