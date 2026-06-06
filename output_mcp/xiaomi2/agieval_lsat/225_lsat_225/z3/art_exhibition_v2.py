from z3 import *

solver = Solver()

# Students: Franz(0), Greene(1), Hidalgo(2), Isaacs(3)
# Types: Oil(0), Watercolor(1)
# Walls: 1,2,3,4
# Position: Upper(1), Lower(0)

paintings = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)]
names = {0: 'Franz', 1: 'Greene', 2: 'Hidalgo', 3: 'Isaacs'}
types = {0: 'Oil', 1: 'Watercolor'}

wall = {p: Int(f'wall_{names[p[0]]}_{types[p[1]]}') for p in paintings}
position = {p: Int(f'pos_{names[p[0]]}_{types[p[1]]}') for p in paintings}

for p in paintings:
    solver.add(wall[p] >= 1, wall[p] <= 4)
    solver.add(Or(position[p] == 0, position[p] == 1))

for w in range(1, 5):
    solver.add(Sum([If(wall[p] == w, 1, 0) for p in paintings]) == 2)
    solver.add(Sum([If(And(wall[p] == w, position[p] == 1), 1, 0) for p in paintings]) == 1)
    solver.add(Sum([If(And(wall[p] == w, position[p] == 0), 1, 0) for p in paintings]) == 1)

for i in range(len(paintings)):
    for j in range(i+1, len(paintings)):
        pi, pj = paintings[i], paintings[j]
        solver.add(Not(And(wall[pi] == wall[pj], position[pi] == position[pj])))

# Constraint 1: No wall has only watercolors
for w in range(1, 5):
    solver.add(Or([And(wall[p] == w, p[1] == 0) for p in paintings]))

# Constraint 2: No wall has work of only one student
for w in range(1, 5):
    for s in range(4):
        solver.add(Not(Sum([If(And(wall[p] == w, p[0] == s), 1, 0) for p in paintings]) == 2))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    franz_on_w = Or([wall[p] == w for p in paintings if p[0] == 0])
    isaacs_on_w = Or([wall[p] == w for p in paintings if p[0] == 3])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 4: Greene's watercolor upper, same wall as Franz's oil (lower)
GW = (1, 1)
FO = (0, 0)
solver.add(wall[GW] == wall[FO])
solver.add(position[GW] == 1)
solver.add(position[FO] == 0)

# Constraint 5: Isaacs's oil lower on wall 4
IO = (3, 0)
solver.add(wall[IO] == 4)
solver.add(position[IO] == 0)

# Answer choices - question asks which CANNOT be true
FW = (0, 1)
GO = (1, 0)
HO = (2, 0)
HW = (2, 1)
IW = (3, 1)

options = [
    ("A", wall[FW] == wall[GO]),       # Franz's watercolor same wall as Greene's oil
    ("B", wall[FW] == wall[HO]),       # Franz's watercolor same wall as Hidalgo's oil
    ("C", position[GO] == 1),          # Greene's oil in upper position
    ("D", position[HW] == 0),          # Hidalgo's watercolor in lower position
    ("E", wall[IW] == wall[HO]),       # Isaacs's watercolor same wall as Hidalgo's oil
]

# For "CANNOT be true" question: the correct answer is the one that is UNSAT
cannot_be_true = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        cannot_be_true.append(letter)
        print(f"Option {letter}: CANNOT be true (UNSAT)")
    elif result == sat:
        print(f"Option {letter}: CAN be true (SAT)")
    else:
        print(f"Option {letter}: UNKNOWN")
    solver.pop()

print()
if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple CANNOT-be-true options found {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No CANNOT-be-true options found")