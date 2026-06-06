from z3 import *

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# All batch days
all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Domain constraints: 0-4
for v in all_batches:
    solver.add(v >= 0, v <= 4)

# No two batches of same kind on same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday
solver.add(Or([v == 0 for v in all_batches]))

# O2 same day as P1
solver.add(O2 == P1)

# S2 on Thursday (day 3)
solver.add(S2 == 3)

# Given: P1 on Tuesday (day 1)
solver.add(P1 == 1)

# Now test each option

# Option A: Two different kinds have their first batch on Monday
# Since P1=1 (Tue), we need O1=0 and S1=0
opt_a = And(O1 == 0, S1 == 0)

# Option B: Two different kinds have their first batch on Tuesday
# P1=1 already, so need O1=1 or S1=1
opt_b = Or(O1 == 1, S1 == 1)

# Option C: Two different kinds have their second batch on Wednesday (day 2)
# O2=1, S2=3, so need P2=2 and either O2=2 or S2=2, but O2=1,S2=3 => need P2=2 and (another)
# Actually need at least two of {O2,P2,S2} on Wed.
# O2=1, S2=3, so impossible. Write constraint anyway.
opt_c = Or(
    And(O2 == 2, P2 == 2),
    And(O2 == 2, S2 == 2),
    And(P2 == 2, S2 == 2)
)

# Option D: Two different kinds have their second batch on Thursday (day 3)
# S2=3, so need O2=3 or P2=3. But O2=1.
opt_d = Or(
    And(O2 == 3, P2 == 3),
    And(O2 == 3, S2 == 3),
    And(P2 == 3, S2 == 3)
)

# Option E: Two different kinds have their third batch on Friday (day 4)
opt_e = Or(
    And(O3 == 4, P3 == 4),
    And(O3 == 4, S3 == 4),
    And(P3 == 4, S3 == 4)
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        # print(f"Option {letter}: SAT")
    # else:
        # print(f"Option {letter}: UNSAT")
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