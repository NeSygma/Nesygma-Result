from z3 import *

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Cookie types: O=oatmeal, P=peanut butter, S=sugar
# Batches: 1, 2, 3

# Declare variables
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

solver = Solver()

# Base constraints
# All days must be between 1 and 5
for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]:
    solver.add(var >= 1, var <= 5)

# No two batches of same kind on same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# At least one batch on Monday
solver.add(Or([var == 1 for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))

# Second batch of oatmeal on same day as first batch of peanut butter
solver.add(O2 == P1)

# Second batch of sugar on Thursday
solver.add(S2 == 4)

# Given: First batch of peanut butter on Tuesday
solver.add(P1 == 2)

# Now test each option for impossibility
# Option A: Two different kinds of cookie have their first batch made on Monday
opt_a = Or(
    And(O1 == 1, P1 == 1),
    And(O1 == 1, S1 == 1),
    And(P1 == 1, S1 == 1)
)

# Option B: Two different kinds of cookie have their first batch made on Tuesday
opt_b = Or(
    And(O1 == 2, P1 == 2),
    And(O1 == 2, S1 == 2),
    And(P1 == 2, S1 == 2)
)

# Option C: Two different kinds of cookie have their second batch made on Wednesday
opt_c = Or(
    And(O2 == 3, P2 == 3),
    And(O2 == 3, S2 == 3),
    And(P2 == 3, S2 == 3)
)

# Option D: Two different kinds of cookie have their second batch made on Thursday
opt_d = Or(
    And(O2 == 4, P2 == 4),
    And(O2 == 4, S2 == 4),
    And(P2 == 4, S2 == 4)
)

# Option E: Two different kinds of cookie have their third batch made on Friday
opt_e = Or(
    And(O3 == 5, P3 == 5),
    And(O3 == 5, S3 == 5),
    And(P3 == 5, S3 == 5)
)

# Test each option for impossibility
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")