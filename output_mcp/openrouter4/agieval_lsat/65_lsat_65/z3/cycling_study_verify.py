from z3 import *

solver = Solver()

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Days: 0=first, 1=second

assign = [[Int(f"assign_{d}_{r}") for r in range(4)] for d in range(2)]

for d in range(2):
    for r in range(4):
        solver.add(assign[d][r] >= 0, assign[d][r] <= 3)

for d in range(2):
    solver.add(Distinct([assign[d][r] for r in range(4)]))

for r in range(4):
    solver.add(assign[0][r] != assign[1][r])

solver.add(assign[0][0] != 0)
solver.add(assign[1][0] != 0)

solver.add(assign[0][3] != 3)
solver.add(assign[1][3] != 3)

solver.add(Or(assign[0][2] == 2, assign[1][2] == 2))

solver.add(assign[0][3] == assign[1][1])

# Check each option explicitly
options = [
    ("A", "Both Reynaldo and Seamus test J", 
     And(Or(assign[0][0]==3, assign[1][0]==3), Or(assign[0][1]==3, assign[1][1]==3))),
    ("B", "Both Reynaldo and Theresa test J",
     And(Or(assign[0][0]==3, assign[1][0]==3), Or(assign[0][2]==3, assign[1][2]==3))),
    ("C", "Both Reynaldo and Yuki test G",
     And(Or(assign[0][0]==1, assign[1][0]==1), Or(assign[0][3]==1, assign[1][3]==1))),
    ("D", "Both Seamus and Theresa test G",
     And(Or(assign[0][1]==1, assign[1][1]==1), Or(assign[0][2]==1, assign[1][2]==1))),
    ("E", "Both Theresa and Yuki test F",
     And(Or(assign[0][2]==0, assign[1][2]==0), Or(assign[0][3]==0, assign[1][3]==0)))
]

for letter, desc, constr in options:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == sat:
        m = solver.model()
        print(f"Option {letter} ({desc}): SAT (POSSIBLE)")
        # Print model
        for d in range(2):
            for r in range(4):
                print(f"  Day {d+1}, rider {['Reynaldo','Seamus','Theresa','Yuki'][r]}: bicycle {['F','G','H','J'][m[assign[d][r]].as_long()]}")
    else:
        print(f"Option {letter} ({desc}): UNSAT (IMPOSSIBLE)")
    solver.pop()