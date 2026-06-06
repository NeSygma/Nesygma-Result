from z3 import *

solver = Solver()

# Define variables for days (0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday)
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

# Bounds: days must be between 0 and 4 inclusive
for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]:
    solver.add(var >= 0, var <= 4)

# Base constraints
# 1. No two batches of the same kind on the same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# 2. At least one batch on Monday
solver.add(Or(O1 == 0, O2 == 0, O3 == 0,
              P1 == 0, P2 == 0, P3 == 0,
              S1 == 0, S2 == 0, S3 == 0))

# 3. Second batch of oatmeal on same day as first batch of peanut butter
solver.add(O2 == P1)

# 4. Second batch of sugar on Thursday (day 3)
solver.add(S2 == 3)

# 5. Given: first batch of peanut butter on Tuesday (day 1)
solver.add(P1 == 1)

# Now evaluate each answer choice
# We want to find which choice makes the problem unsatisfiable (cannot be true)
unsat_options = []

# Choice A: Two different kinds have their first batch made on Monday.
# That means O1 == 0 and S1 == 0 (since P1 is Tuesday)
opt_a = And(O1 == 0, S1 == 0)

# Choice B: Two different kinds have their first batch made on Tuesday.
# Since P1 == 1, we need at least one more of O1 or S1 to be 1.
# But O1 cannot be 1 because O2 == 1 (distinct). So only S1 can be 1.
opt_b = S1 == 1

# Choice C: Two different kinds have their second batch made on Wednesday.
# We need two of {O2, P2, S2} to be 2.
# Since O2 == 1 and S2 == 3, the only possible pair is P2 and S2, but S2 is 3.
# So we check all pairs.
opt_c = Or(
    And(O2 == 2, P2 == 2),
    And(O2 == 2, S2 == 2),
    And(P2 == 2, S2 == 2)
)

# Choice D: Two different kinds have their second batch made on Thursday.
# Since O2 == 1 and S2 == 3, we need P2 == 3.
opt_d = P2 == 3

# Choice E: Two different kinds have their third batch made on Friday.
# Need at least two of O3, P3, S3 to be 4.
opt_e = Or(
    And(O3 == 4, P3 == 4),
    And(O3 == 4, S3 == 4),
    And(P3 == 4, S3 == 4)
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found unsat {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found unsat")