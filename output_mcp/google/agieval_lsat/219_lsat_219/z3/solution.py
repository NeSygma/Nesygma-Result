from z3 import *

# Students: F, G, H, I
# Paintings: FO, FW, GO, GW, HO, HW, IO, IW
# Walls: 1, 2, 3, 4
# Positions: 0 (Upper), 1 (Lower)

# Define paintings
paintings = ['FO', 'FW', 'GO', 'GW', 'HO', 'HW', 'IO', 'IW']
students = {'FO': 'F', 'FW': 'F', 'GO': 'G', 'GW': 'G', 'HO': 'H', 'HW': 'H', 'IO': 'I', 'IW': 'I'}
is_oil = {'FO': True, 'FW': False, 'GO': True, 'GW': False, 'HO': True, 'HW': False, 'IO': True, 'IW': False}

solver = Solver()

# Variables: Wall[p] in {1, 2, 3, 4}, Pos[p] in {0, 1}
wall = {p: Int(f'wall_{p}') for p in paintings}
pos = {p: Int(f'pos_{p}') for p in paintings}

for p in paintings:
    solver.add(wall[p] >= 1, wall[p] <= 4)
    solver.add(pos[p] >= 0, pos[p] <= 1)

# Each painting has a unique (wall, pos)
for i in range(len(paintings)):
    for j in range(i + 1, len(paintings)):
        p1, p2 = paintings[i], paintings[j]
        solver.add(Not(And(wall[p1] == wall[p2], pos[p1] == pos[p2])))

# C1: No wall has only watercolors (each wall must have at least one oil)
for w in range(1, 5):
    solver.add(Or([And(wall[p] == w, is_oil[p]) for p in paintings]))

# C2: No wall has only one student's work (each wall must have two different students)
for w in range(1, 5):
    # There are exactly 2 paintings per wall. They must be from different students.
    # Let p1, p2 be the two paintings on wall w.
    # We can express this by saying for any two paintings p1, p2, if they are on the same wall, their students must be different.
    for i in range(len(paintings)):
        for j in range(i + 1, len(paintings)):
            p1, p2 = paintings[i], paintings[j]
            solver.add(Implies(And(wall[p1] == w, wall[p2] == w), students[p1] != students[p2]))

# C3: No wall has both F and I
for w in range(1, 5):
    has_F = Or([And(wall[p] == w, students[p] == 'F') for p in paintings])
    has_I = Or([And(wall[p] == w, students[p] == 'I') for p in paintings])
    solver.add(Not(And(has_F, has_I)))

# C4: Greene's watercolor (GW) is in the upper position of the wall on which Franz's oil (FO) is in the lower position.
solver.add(wall['GW'] == wall['FO'])
solver.add(pos['GW'] == 0)
solver.add(pos['FO'] == 1)

# C5: Isaacs's oil (IO) is in the lower position of wall 4.
solver.add(wall['IO'] == 4)
solver.add(pos['IO'] == 1)

# Define the answer choices
# Each choice is a list of 4 paintings (for lower positions of walls 1, 2, 3, 4)
choices = {
    'A': ['FO', 'FW', 'GO', 'IO'],
    'B': ['FO', 'HW', 'IW', 'IO'],
    'C': ['GO', 'FO', 'IO', 'HO'],
    'D': ['HO', 'GO', 'GW', 'IO'],
    'E': ['HW', 'FO', 'GO', 'IO']
}

found_options = []
for letter, choice in choices.items():
    solver.push()
    # Add constraints for the choice:
    # The lower position of wall w is choice[w-1]
    for w in range(1, 5):
        p_lower = choice[w-1]
        solver.add(wall[p_lower] == w)
        solver.add(pos[p_lower] == 1)
    
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