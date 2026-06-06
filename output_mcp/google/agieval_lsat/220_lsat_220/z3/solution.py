from z3 import *

# Students
students = ['F', 'G', 'H', 'I']
paintings = [(s, t) for s in students for t in ['O', 'W']]

wall = {p: Int(f"wall_{p[0]}_{p[1]}") for p in paintings}
pos = {p: Int(f"pos_{p[0]}_{p[1]}") for p in paintings}

solver = Solver()

for p in paintings:
    solver.add(wall[p] >= 1, wall[p] <= 4)
    solver.add(pos[p] >= 0, pos[p] <= 1)

for w in range(1, 5):
    solver.add(Sum([If(And(wall[p] == w, pos[p] == 0), 1, 0) for p in paintings]) == 1)
    solver.add(Sum([If(And(wall[p] == w, pos[p] == 1), 1, 0) for p in paintings]) == 1)

for w in range(1, 5):
    solver.add(Sum([If(And(wall[p] == w, p[1] == 'O'), 1, 0) for p in paintings]) >= 1)

for w in range(1, 5):
    for i in range(len(paintings)):
        for j in range(i + 1, len(paintings)):
            p1 = paintings[i]
            p2 = paintings[j]
            solver.add(Implies(wall[p1] == wall[p2], p1[0] != p2[0]))

for w in range(1, 5):
    has_F = Or([wall[p] == w for p in paintings if p[0] == 'F'])
    has_I = Or([wall[p] == w for p in paintings if p[0] == 'I'])
    solver.add(Not(And(has_F, has_I)))

solver.add(wall[('G', 'W')] == wall[('F', 'O')])
solver.add(pos[('G', 'W')] == 0)
solver.add(pos[('F', 'O')] == 1)

solver.add(wall[('I', 'O')] == 4)
solver.add(pos[('I', 'O')] == 1)

solver.add(wall[('I', 'W')] == 2)
solver.add(wall[('F', 'O')] == 3)

options = [
    ('A', ('F', 'W')),
    ('B', ('G', 'O')),
    ('C', ('G', 'W')),
    ('D', ('H', 'O')),
    ('E', ('H', 'W'))
]

# Check which option MUST be on wall 1
# This means for a given option, it is NOT possible that it is NOT on wall 1.
# So we check if (NOT (option is on wall 1)) is UNSAT.

for letter, p in options:
    solver.push()
    solver.add(wall[p] != 1)
    if solver.check() == unsat:
        print(f"Option {letter} must be on wall 1")
    solver.pop()