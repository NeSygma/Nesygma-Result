from z3 import *

solver = Solver()

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Days: 0=first, 1=second

assign = [[Int(f"assign_{d}_{r}") for r in range(4)] for d in range(2)]

for d in range(2):
    for r in range(4):
        solver.add(assign[d][r] >= 0, assign[d][r] <= 3)

# Each day, all four bicycles are tested (distinct per day)
for d in range(2):
    solver.add(Distinct([assign[d][r] for r in range(4)]))

# Each rider tests a different bicycle on day 1 vs day 2
for r in range(4):
    solver.add(assign[0][r] != assign[1][r])

# Reynaldo cannot test F (bicycle 0) on either day
solver.add(assign[0][0] != 0)
solver.add(assign[1][0] != 0)

# Yuki cannot test J (bicycle 3) on either day
solver.add(assign[0][3] != 3)
solver.add(assign[1][3] != 3)

# Theresa must be one of the testers for H (bicycle 2)
solver.add(Or(assign[0][2] == 2, assign[1][2] == 2))

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(assign[0][3] == assign[1][1])

# Evaluate each option
options = [
    ("A", And(Or(assign[0][0]==3, assign[1][0]==3), Or(assign[0][1]==3, assign[1][1]==3))),
    ("B", And(Or(assign[0][0]==3, assign[1][0]==3), Or(assign[0][2]==3, assign[1][2]==3))),
    ("C", And(Or(assign[0][0]==1, assign[1][0]==1), Or(assign[0][3]==1, assign[1][3]==1))),
    ("D", And(Or(assign[0][1]==1, assign[1][1]==1), Or(assign[0][2]==1, assign[1][2]==1))),
    ("E", And(Or(assign[0][2]==0, assign[1][2]==0), Or(assign[0][3]==0, assign[1][3]==0)))
]

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