from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
days = 5

# For each cookie type, we have 3 batches (batch 1, 2, 3)
# Each batch is assigned a day (0-4)
# No two batches of the same kind on the same day

# Define variables for each batch of each cookie type
o = [Int(f'o_{i}') for i in range(3)]  # oatmeal batches 1,2,3
pb = [Int(f'pb_{i}') for i in range(3)]  # peanut butter batches 1,2,3
s = [Int(f's_{i}') for i in range(3)]  # sugar batches 1,2,3

solver = Solver()

# Domain constraints: each batch is on a day 0-4
for v in o + pb + s:
    solver.add(v >= 0, v <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct(o))
solver.add(Distinct(pb))
solver.add(Distinct(s))

# At least one batch on Monday (day 0)
all_batches = o + pb + s
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal is made on the same day as the first batch of peanut butter
solver.add(o[1] == pb[0])

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(s[1] == 3)

# Now define each option as constraints
# Option A: oatmeal: Monday(0), Wednesday(2), Thursday(3); peanut butter: Wednesday(2), Thursday(3), Friday(4); sugar: Monday(0), Thursday(3), Friday(4)
opt_a = And(
    Distinct(o[0], o[1], o[2]),
    Or(And(o[0]==0, o[1]==2, o[2]==3), And(o[0]==0, o[1]==3, o[2]==2),
       And(o[0]==2, o[1]==0, o[2]==3), And(o[0]==2, o[1]==3, o[2]==0),
       And(o[0]==3, o[1]==0, o[2]==2), And(o[0]==3, o[1]==2, o[2]==0)),
    Distinct(pb[0], pb[1], pb[2]),
    Or(And(pb[0]==2, pb[1]==3, pb[2]==4), And(pb[0]==2, pb[1]==4, pb[2]==3),
       And(pb[0]==3, pb[1]==2, pb[2]==4), And(pb[0]==3, pb[1]==4, pb[2]==2),
       And(pb[0]==4, pb[1]==2, pb[2]==3), And(pb[0]==4, pb[1]==3, pb[2]==2)),
    Distinct(s[0], s[1], s[2]),
    Or(And(s[0]==0, s[1]==3, s[2]==4), And(s[0]==0, s[1]==4, s[2]==3),
       And(s[0]==3, s[1]==0, s[2]==4), And(s[0]==3, s[1]==4, s[2]==0),
       And(s[0]==4, s[1]==0, s[2]==3), And(s[0]==4, s[1]==3, s[2]==0))
)

# Option B: oatmeal: Monday(0), Tuesday(1), Thursday(3); peanut butter: Tuesday(1), Wednesday(2), Thursday(3); sugar: Monday(0), Wednesday(2), Thursday(3)
opt_b = And(
    Distinct(o[0], o[1], o[2]),
    Or(And(o[0]==0, o[1]==1, o[2]==3), And(o[0]==0, o[1]==3, o[2]==1),
       And(o[0]==1, o[1]==0, o[2]==3), And(o[0]==1, o[1]==3, o[2]==0),
       And(o[0]==3, o[1]==0, o[2]==1), And(o[0]==3, o[1]==1, o[2]==0)),
    Distinct(pb[0], pb[1], pb[2]),
    Or(And(pb[0]==1, pb[1]==2, pb[2]==3), And(pb[0]==1, pb[1]==3, pb[2]==2),
       And(pb[0]==2, pb[1]==1, pb[2]==3), And(pb[0]==2, pb[1]==3, pb[2]==1),
       And(pb[0]==3, pb[1]==1, pb[2]==2), And(pb[0]==3, pb[1]==2, pb[2]==1)),
    Distinct(s[0], s[1], s[2]),
    Or(And(s[0]==0, s[1]==2, s[2]==3), And(s[0]==0, s[1]==3, s[2]==2),
       And(s[0]==2, s[1]==0, s[2]==3), And(s[0]==2, s[1]==3, s[2]==0),
       And(s[0]==3, s[1]==0, s[2]==2), And(s[0]==3, s[1]==2, s[2]==0))
)

# Option C: oatmeal: Tuesday(1), Wednesday(2), Thursday(3); peanut butter: Wednesday(2), Thursday(3), Friday(4); sugar: Tuesday(1), Thursday(3), Friday(4)
opt_c = And(
    Distinct(o[0], o[1], o[2]),
    Or(And(o[0]==1, o[1]==2, o[2]==3), And(o[0]==1, o[1]==3, o[2]==2),
       And(o[0]==2, o[1]==1, o[2]==3), And(o[0]==2, o[1]==3, o[2]==1),
       And(o[0]==3, o[1]==1, o[2]==2), And(o[0]==3, o[1]==2, o[2]==1)),
    Distinct(pb[0], pb[1], pb[2]),
    Or(And(pb[0]==2, pb[1]==3, pb[2]==4), And(pb[0]==2, pb[1]==4, pb[2]==3),
       And(pb[0]==3, pb[1]==2, pb[2]==4), And(pb[0]==3, pb[1]==4, pb[2]==2),
       And(pb[0]==4, pb[1]==2, pb[2]==3), And(pb[0]==4, pb[1]==3, pb[2]==2)),
    Distinct(s[0], s[1], s[2]),
    Or(And(s[0]==1, s[1]==3, s[2]==4), And(s[0]==1, s[1]==4, s[2]==3),
       And(s[0]==3, s[1]==1, s[2]==4), And(s[0]==3, s[1]==4, s[2]==1),
       And(s[0]==4, s[1]==1, s[2]==3), And(s[0]==4, s[1]==3, s[2]==1))
)

# Option D: oatmeal: Monday(0), Tuesday(1), Thursday(3); peanut butter: Monday(0), Wednesday(2), Thursday(3); sugar: Monday(0), Thursday(3), Friday(4)
opt_d = And(
    Distinct(o[0], o[1], o[2]),
    Or(And(o[0]==0, o[1]==1, o[2]==3), And(o[0]==0, o[1]==3, o[2]==1),
       And(o[0]==1, o[1]==0, o[2]==3), And(o[0]==1, o[1]==3, o[2]==0),
       And(o[0]==3, o[1]==0, o[2]==1), And(o[0]==3, o[1]==1, o[2]==0)),
    Distinct(pb[0], pb[1], pb[2]),
    Or(And(pb[0]==0, pb[1]==2, pb[2]==3), And(pb[0]==0, pb[1]==3, pb[2]==2),
       And(pb[0]==2, pb[1]==0, pb[2]==3), And(pb[0]==2, pb[1]==3, pb[2]==0),
       And(pb[0]==3, pb[1]==0, pb[2]==2), And(pb[0]==3, pb[1]==2, pb[2]==0)),
    Distinct(s[0], s[1], s[2]),
    Or(And(s[0]==0, s[1]==3, s[2]==4), And(s[0]==0, s[1]==4, s[2]==3),
       And(s[0]==3, s[1]==0, s[2]==4), And(s[0]==3, s[1]==4, s[2]==0),
       And(s[0]==4, s[1]==0, s[2]==3), And(s[0]==4, s[1]==3, s[2]==0))
)

# Option E: oatmeal: Monday(0), Thursday(3), Friday(4); peanut butter: Tuesday(1), Wednesday(2), Thursday(3); sugar: Monday(0), Thursday(3), Friday(4)
opt_e = And(
    Distinct(o[0], o[1], o[2]),
    Or(And(o[0]==0, o[1]==3, o[2]==4), And(o[0]==0, o[1]==4, o[2]==3),
       And(o[0]==3, o[1]==0, o[2]==4), And(o[0]==3, o[1]==4, o[2]==0),
       And(o[0]==4, o[1]==0, o[2]==3), And(o[0]==4, o[1]==3, o[2]==0)),
    Distinct(pb[0], pb[1], pb[2]),
    Or(And(pb[0]==1, pb[1]==2, pb[2]==3), And(pb[0]==1, pb[1]==3, pb[2]==2),
       And(pb[0]==2, pb[1]==1, pb[2]==3), And(pb[0]==2, pb[1]==3, pb[2]==1),
       And(pb[0]==3, pb[1]==1, pb[2]==2), And(pb[0]==3, pb[1]==2, pb[2]==1)),
    Distinct(s[0], s[1], s[2]),
    Or(And(s[0]==0, s[1]==3, s[2]==4), And(s[0]==0, s[1]==4, s[2]==3),
       And(s[0]==3, s[1]==0, s[2]==4), And(s[0]==3, s[1]==4, s[2]==0),
       And(s[0]==4, s[1]==0, s[2]==3), And(s[0]==4, s[1]==3, s[2]==0))
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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