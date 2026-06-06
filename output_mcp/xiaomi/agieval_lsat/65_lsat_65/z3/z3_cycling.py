from z3 import *

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Days: 1 and 2

# Variables: bike[r][d] = bicycle tested by rider r on day d
bike = [[Int(f"bike_{r}_{d}") for d in range(2)] for r in range(4)]

solver = Solver()

# Each bike assignment is in {0,1,2,3}
for r in range(4):
    for d in range(2):
        solver.add(bike[r][d] >= 0, bike[r][d] <= 3)

# Each rider tests a different bike on day 1 vs day 2
for r in range(4):
    solver.add(bike[r][0] != bike[r][1])

# All four bikes are tested each day (each day is a permutation)
for d in range(2):
    solver.add(Distinct([bike[r][d] for r in range(4)]))

# Condition 1: Reynaldo cannot test F (bike 0)
for d in range(2):
    solver.add(bike[0][d] != 0)

# Condition 2: Yuki cannot test J (bike 3)
for d in range(2):
    solver.add(bike[3][d] != 3)

# Condition 3: Theresa must be one of the testers for H (bike 2)
solver.add(Or(bike[2][0] == 2, bike[2][1] == 2))

# Condition 4: The bike Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(bike[1][1] == bike[3][0])

# Now evaluate each option
# (A) Both Reynaldo and Seamus test J (bike 3)
opt_a = Or(
    And(bike[0][0] == 3, bike[1][0] == 3),
    And(bike[0][0] == 3, bike[1][1] == 3),
    And(bike[0][1] == 3, bike[1][0] == 3),
    And(bike[0][1] == 3, bike[1][1] == 3)
)

# (B) Both Reynaldo and Theresa test J (bike 3)
opt_b = Or(
    And(bike[0][0] == 3, bike[2][0] == 3),
    And(bike[0][0] == 3, bike[2][1] == 3),
    And(bike[0][1] == 3, bike[2][0] == 3),
    And(bike[0][1] == 3, bike[2][1] == 3)
)

# (C) Both Reynaldo and Yuki test G (bike 1)
opt_c = Or(
    And(bike[0][0] == 1, bike[3][0] == 1),
    And(bike[0][0] == 1, bike[3][1] == 1),
    And(bike[0][1] == 1, bike[3][0] == 1),
    And(bike[0][1] == 1, bike[3][1] == 1)
)

# (D) Both Seamus and Theresa test G (bike 1)
opt_d = Or(
    And(bike[1][0] == 1, bike[2][0] == 1),
    And(bike[1][0] == 1, bike[2][1] == 1),
    And(bike[1][1] == 1, bike[2][0] == 1),
    And(bike[1][1] == 1, bike[2][1] == 1)
)

# (E) Both Theresa and Yuki test F (bike 0)
opt_e = Or(
    And(bike[2][0] == 0, bike[3][0] == 0),
    And(bike[2][0] == 0, bike[3][1] == 0),
    And(bike[2][1] == 0, bike[3][0] == 0),
    And(bike[2][1] == 0, bike[3][1] == 0)
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