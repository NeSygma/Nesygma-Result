from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# For each cookie type, we have 3 batches (1st, 2nd, 3rd)
# Each batch is assigned a day (0-4)
O1, O2, O3 = Ints('O1 O2 O3')  # oatmeal batches 1,2,3
P1, P2, P3 = Ints('P1 P2 P3')  # peanut butter batches 1,2,3
S1, S2, S3 = Ints('S1 S2 S3')  # sugar batches 1,2,3

solver = Solver()

# Base constraints: all batches must be on valid days (0-4)
solver.add(O1 >= 0, O1 <= 4)
solver.add(O2 >= 0, O2 <= 4)
solver.add(O3 >= 0, O3 <= 4)
solver.add(P1 >= 0, P1 <= 4)
solver.add(P2 >= 0, P2 <= 4)
solver.add(P3 >= 0, P3 <= 4)
solver.add(S1 >= 0, S1 <= 4)
solver.add(S2 >= 0, S2 <= 4)
solver.add(S3 >= 0, S3 <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

# At least one batch on Monday (day 0)
solver.add(Or(O1 == 0, O2 == 0, O3 == 0,
              P1 == 0, P2 == 0, P3 == 0,
              S1 == 0, S2 == 0, S3 == 0))

# Second batch of oatmeal = first batch of peanut butter
solver.add(O2 == P1)

# Second batch of sugar is on Thursday (day 3)
solver.add(S2 == 3)

# Now test each answer choice
found_options = []

# Option A: oatmeal: Monday, Wednesday, Thursday; peanut butter: Wednesday, Thursday, Friday; sugar: Monday, Thursday, Friday
opt_a = And(
    O1 == 0, O2 == 2, O3 == 3,  # Monday, Wednesday, Thursday
    P1 == 2, P2 == 3, P3 == 4,  # Wednesday, Thursday, Friday
    S1 == 0, S2 == 3, S3 == 4   # Monday, Thursday, Friday
)

# Option B: oatmeal: Monday, Tuesday, Thursday; peanut butter: Tuesday, Wednesday, Thursday; sugar: Monday, Wednesday, Thursday
opt_b = And(
    O1 == 0, O2 == 1, O3 == 3,  # Monday, Tuesday, Thursday
    P1 == 1, P2 == 2, P3 == 3,  # Tuesday, Wednesday, Thursday
    S1 == 0, S2 == 3, S3 == 2   # Monday, Wednesday, Thursday
)

# Option C: oatmeal: Tuesday, Wednesday, Thursday; peanut butter: Wednesday, Thursday, Friday; sugar: Tuesday, Thursday, Friday
opt_c = And(
    O1 == 1, O2 == 2, O3 == 3,  # Tuesday, Wednesday, Thursday
    P1 == 2, P2 == 3, P3 == 4,  # Wednesday, Thursday, Friday
    S1 == 1, S2 == 3, S3 == 4   # Tuesday, Thursday, Friday
)

# Option D: oatmeal: Monday, Tuesday, Thursday; peanut butter: Monday, Wednesday, Thursday; sugar: Monday, Thursday, Friday
opt_d = And(
    O1 == 0, O2 == 1, O3 == 3,  # Monday, Tuesday, Thursday
    P1 == 0, P2 == 2, P3 == 3,  # Monday, Wednesday, Thursday
    S1 == 0, S2 == 3, S3 == 4   # Monday, Thursday, Friday
)

# Option E: oatmeal: Monday, Thursday, Friday; peanut butter: Tuesday, Wednesday, Thursday; sugar: Monday, Thursday, Friday
opt_e = And(
    O1 == 0, O2 == 3, O3 == 4,  # Monday, Thursday, Friday
    P1 == 1, P2 == 2, P3 == 3,  # Tuesday, Wednesday, Thursday
    S1 == 0, S2 == 3, S3 == 4   # Monday, Thursday, Friday
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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