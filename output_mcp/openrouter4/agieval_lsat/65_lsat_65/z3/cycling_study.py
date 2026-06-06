from z3 import *

solver = Solver()

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Days: 0=first, 1=second

# assign[day][rider] = bicycle
assign = [[Int(f"assign_{d}_{r}") for r in range(4)] for d in range(2)]

# Domain: each assignment is a bicycle (0 to 3)
for d in range(2):
    for r in range(4):
        solver.add(assign[d][r] >= 0, assign[d][r] <= 3)

# Constraint 1: Each day, all four bicycles are tested (each rider gets a distinct bicycle each day)
for d in range(2):
    solver.add(Distinct([assign[d][r] for r in range(4)]))

# Constraint 2: Each rider tests a different bicycle on day 2 than day 1
for r in range(4):
    solver.add(assign[0][r] != assign[1][r])

# Constraint 3: Reynaldo (r=0) cannot test F (b=0)
solver.add(assign[0][0] != 0)
solver.add(assign[1][0] != 0)

# Constraint 4: Yuki (r=3) cannot test J (b=3)
solver.add(assign[0][3] != 3)
solver.add(assign[1][3] != 3)

# Constraint 5: Theresa (r=2) must test H (b=2) on at least one day
solver.add(Or(assign[0][2] == 2, assign[1][2] == 2))

# Constraint 6: The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(assign[0][3] == assign[1][1])

# Now test each option
# Each option says "Both X and Y test Z" meaning each of the two riders tests bicycle Z at some point.

options = []

# (A) Both Reynaldo and Seamus test J (b=3)
opt_a = And(
    Or(assign[0][0] == 3, assign[1][0] == 3),
    Or(assign[0][1] == 3, assign[1][1] == 3)
)
options.append(("A", opt_a))

# (B) Both Reynaldo and Theresa test J (b=3)
opt_b = And(
    Or(assign[0][0] == 3, assign[1][0] == 3),
    Or(assign[0][2] == 3, assign[1][2] == 3)
)
options.append(("B", opt_b))

# (C) Both Reynaldo and Yuki test G (b=1)
opt_c = And(
    Or(assign[0][0] == 1, assign[1][0] == 1),
    Or(assign[0][3] == 1, assign[1][3] == 1)
)
options.append(("C", opt_c))

# (D) Both Seamus and Theresa test G (b=1)
opt_d = And(
    Or(assign[0][1] == 1, assign[1][1] == 1),
    Or(assign[0][2] == 1, assign[1][2] == 1)
)
options.append(("D", opt_d))

# (E) Both Theresa and Yuki test F (b=0)
opt_e = And(
    Or(assign[0][2] == 0, assign[1][2] == 0),
    Or(assign[0][3] == 0, assign[1][3] == 0)
)
options.append(("E", opt_e))

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