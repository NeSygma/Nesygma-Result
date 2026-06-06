from z3 import *

solver = Solver()

# Singers: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
# Position variables: pos[singer] = position (1-6)
pos = [Int(f'pos_{n}') for n in range(6)]
names = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']

# Each singer gets a unique position from 1 to 6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(pos))

# Recorded singers: Kammer (0) and Lugo (1)
# Not recorded: Trillo (2), Waite (3), Yoshida (4), Zinn (5)

# Constraint 1: Fourth audition cannot be recorded
# So position 4 is NOT Kammer and NOT Lugo
solver.add(pos[0] != 4)  # Kammer not at 4
solver.add(pos[1] != 4)  # Lugo not at 4

# Constraint 2: Fifth audition must be recorded
# So position 5 IS Kammer OR Lugo
solver.add(Or(pos[0] == 5, pos[1] == 5))

# Constraint 3: Waite must be earlier than both recorded auditions
# Waite (3) < Kammer (0) AND Waite (3) < Lugo (1)
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Constraint 4: Kammer must be earlier than Trillo
solver.add(pos[0] < pos[2])

# Constraint 5: Zinn must be earlier than Yoshida
solver.add(pos[5] < pos[4])

# Question: Which one could be the sixth audition?
# Test each option
options = [
    ("A", pos[0] == 6),  # Kammer
    ("B", pos[1] == 6),  # Lugo
    ("C", pos[2] == 6),  # Trillo
    ("D", pos[3] == 6),  # Waite
    ("E", pos[5] == 6),  # Zinn
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