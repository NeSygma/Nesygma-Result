from z3 import *

# Students
STUDENTS = ['F', 'G', 'H', 'I']
# Paintings
PAINTINGS = ['FO', 'FW', 'GO', 'GW', 'HO', 'HW', 'IO', 'IW']

# Variables
# Wall[p] in {1, 2, 3, 4}
# Pos[p] in {0, 1} (0: Lower, 1: Upper)
wall = {p: Int(f'wall_{p}') for p in PAINTINGS}
pos = {p: Int(f'pos_{p}') for p in PAINTINGS}

solver = Solver()

# Domain constraints
for p in PAINTINGS:
    solver.add(wall[p] >= 1, wall[p] <= 4)
    solver.add(pos[p] >= 0, pos[p] <= 1)

# Each position (wall, pos) is occupied by exactly one painting
# There are 8 positions (4 walls * 2 positions)
for p1 in PAINTINGS:
    for p2 in PAINTINGS:
        if p1 != p2:
            solver.add(Not(And(wall[p1] == wall[p2], pos[p1] == pos[p2])))

# No wall has only watercolors (must have at least one oil)
for w in range(1, 5):
    solver.add(Or([And(wall[p] == w, p.endswith('O')) for p in PAINTINGS]))

# No wall has only one student
for w in range(1, 5):
    # Get all paintings on wall w
    paintings_on_w = [p for p in PAINTINGS if True] # Placeholder, will use Or-loop
    # Actually, we need to check if there are at least two distinct students on wall w
    # Students on wall w:
    students_on_w = [If(wall[p] == w, 1, 0) for p in PAINTINGS] # This is not quite right
    # Let's use a more direct approach:
    # For each wall, there must be at least two students.
    # Let's define a boolean for each student on each wall
    for w in range(1, 5):
        student_on_wall = [Or([And(wall[p] == w, p.startswith(s)) for p in PAINTINGS]) for s in STUDENTS]
        solver.add(Sum([If(s_on_w, 1, 0) for s_on_w in student_on_wall]) >= 2)

# No wall has both F and I
for w in range(1, 5):
    f_on_w = Or([And(wall[p] == w, p.startswith('F')) for p in PAINTINGS])
    i_on_w = Or([And(wall[p] == w, p.startswith('I')) for p in PAINTINGS])
    solver.add(Not(And(f_on_w, i_on_w)))

# Greene's watercolor (GW) is in the upper position of the wall where Franz's oil (FO) is in the lower position
solver.add(wall['GW'] == wall['FO'])
solver.add(pos['GW'] == 1)
solver.add(pos['FO'] == 0)

# Isaacs's oil (IO) is in the lower position of wall 4
solver.add(wall['IO'] == 4)
solver.add(pos['IO'] == 0)

# Q: If Greene's oil (GO) is displayed on the same wall as Franz's watercolor (FW)
solver.push()
solver.add(wall['GO'] == wall['FW'])

# Answer Choices
# (A) Greene's oil is displayed in an upper position.
# (B) Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.
# (C) Hidalgo's oil is displayed in an upper position.
# (D) Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.
# (E) Isaacs's watercolor is displayed in a lower position.

options = {
    "A": pos['GO'] == 1,
    "B": wall['HW'] == wall['IW'],
    "C": pos['HO'] == 1,
    "D": wall['HO'] == wall['IW'],
    "E": pos['IW'] == 0
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

print(f"found_options: {found_options}")
solver.pop()