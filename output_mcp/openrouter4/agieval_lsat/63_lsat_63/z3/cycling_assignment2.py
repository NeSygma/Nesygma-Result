from z3 import *

solver = Solver()

# Map: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Days: 0=first, 1=second

riders = 4
days = 2
assign = [[Int(f"r{r}_d{d}") for r in range(riders)] for d in range(days)]

# Domain constraints
for d in range(days):
    for r in range(riders):
        solver.add(assign[d][r] >= 0, assign[d][r] <= 3)

# Each day, all bicycles are tested (distinct)
for d in range(days):
    solver.add(Distinct(assign[d][0], assign[d][1], assign[d][2], assign[d][3]))

# Each rider tests a different bicycle on day2 than day1
for r in range(riders):
    solver.add(assign[0][r] != assign[1][r])

# Reynaldo cannot test F (bike 0)
solver.add(assign[0][0] != 0)
solver.add(assign[1][0] != 0)

# Yuki cannot test J (bike 3)
solver.add(assign[0][3] != 3)
solver.add(assign[1][3] != 3)

# Theresa must be one of the testers for H (bike 2)
solver.add(Or(assign[0][2] == 2, assign[1][2] == 2))

# Yuki's first day bicycle = Seamus's second day bicycle
solver.add(assign[0][3] == assign[1][1])

# Now test each option
# (A) Reynaldo tests G on the second day: assign[1][0] == 1
# (B) Seamus tests F on the first day: assign[0][1] == 0
# (C) Theresa tests F on the second day: assign[1][2] == 0
# (D) Reynaldo tests H on the first day: assign[0][0] == 2
# (E) Yuki tests F on the second day: assign[1][3] == 0

# We want the option that CANNOT be true -> makes the system UNSAT
impossible_options = []
for letter, constr in [
    ("A", assign[1][0] == 1),
    ("B", assign[0][1] == 0),
    ("C", assign[1][2] == 0),
    ("D", assign[0][0] == 2),
    ("E", assign[1][3] == 0)
]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
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