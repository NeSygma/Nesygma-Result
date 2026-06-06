from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Types: Oil=0, Watercolor=1
# Walls: 1,2,3,4
# Positions: Upper=0, Lower=1

paintings = [[Int(f"paint_{s}_{t}") for t in range(2)] for s in range(4)]
positions = [[Int(f"pos_{s}_{t}") for t in range(2)] for s in range(4)]

# Domain constraints
for s in range(4):
    for t in range(2):
        solver.add(paintings[s][t] >= 1, paintings[s][t] <= 4)
        solver.add(Or(positions[s][t] == 0, positions[s][t] == 1))

# Each wall has exactly 2 paintings (one upper, one lower)
for w in range(1, 5):
    solver.add(Sum([If(paintings[s][t] == w, 1, 0) for s in range(4) for t in range(2)]) == 2)
    solver.add(Sum([If(And(paintings[s][t] == w, positions[s][t] == 0), 1, 0) for s in range(4) for t in range(2)]) == 1)
    solver.add(Sum([If(And(paintings[s][t] == w, positions[s][t] == 1), 1, 0) for s in range(4) for t in range(2)]) == 1)

# All paintings on different wall-position combinations
all_assignments = []
for s in range(4):
    for t in range(2):
        all_assignments.append((paintings[s][t], positions[s][t]))
for i in range(len(all_assignments)):
    for j in range(i+1, len(all_assignments)):
        solver.add(Or(all_assignments[i][0] != all_assignments[j][0],
                      all_assignments[i][1] != all_assignments[j][1]))

# Constraint 1: No wall has only watercolors
for w in range(1, 5):
    solver.add(Or([paintings[s][0] == w for s in range(4)]))

# Constraint 2: No wall has work of only one student
for w in range(1, 5):
    for s in range(4):
        solver.add(Sum([If(paintings[s][t] == w, 1, 0) for t in range(2)]) <= 1)

# Constraint 3: No wall has both Franz (0) and Isaacs (3)
for w in range(1, 5):
    solver.add(Not(And(
        Or(paintings[0][0] == w, paintings[0][1] == w),
        Or(paintings[3][0] == w, paintings[3][1] == w)
    )))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is
solver.add(paintings[1][1] == paintings[0][0])
solver.add(positions[1][1] == 0)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(paintings[3][0] == 4)
solver.add(positions[3][0] == 1)

# Test each option - find which CANNOT be true (UNSAT)
# The question asks "Which CANNOT be true?" - so we want the UNSAT option
impossible_options = []
for letter, constr in [("A", paintings[0][1] == paintings[1][0]),
                       ("B", paintings[0][1] == paintings[2][0]),
                       ("C", positions[1][0] == 0),
                       ("D", positions[2][1] == 1),
                       ("E", paintings[3][1] == paintings[2][0])]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
        print(f"Option {letter} is UNSAT - CANNOT be true")
    else:
        print(f"Option {letter} is SAT - CAN be true")
    solver.pop()

print()
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")