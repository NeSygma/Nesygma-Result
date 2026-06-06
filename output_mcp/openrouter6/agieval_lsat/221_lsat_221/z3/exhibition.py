from z3 import *

solver = Solver()

# Define student indices
FRANZ = 0
GREENE = 1
HIDALGO = 2
ISAACS = 3

# Define types
OIL = 0
WATERCOLOR = 1

# Variables: wall[s][t] and pos[s][t] for each student s and type t
wall = [[Int(f"wall_{s}_{t}") for t in range(2)] for s in range(4)]
pos = [[Int(f"pos_{s}_{t}") for t in range(2)] for s in range(4)]

# Domain constraints for wall and pos
for s in range(4):
    for t in range(2):
        solver.add(wall[s][t] >= 1, wall[s][t] <= 4)
        solver.add(pos[s][t] >= 0, pos[s][t] <= 1)

# Per-wall constraints: exactly one upper and one lower painting per wall
for w in range(1, 5):
    # Count upper paintings on wall w
    upper_count = Sum([If(And(wall[s][t] == w, pos[s][t] == 0), 1, 0) for s in range(4) for t in range(2)])
    solver.add(upper_count == 1)
    # Count lower paintings on wall w
    lower_count = Sum([If(And(wall[s][t] == w, pos[s][t] == 1), 1, 0) for s in range(4) for t in range(2)])
    solver.add(lower_count == 1)

# Condition 1: No wall has only watercolors (at least one oil per wall)
for w in range(1, 5):
    oil_count = Sum([If(And(wall[s][t] == w, t == OIL), 1, 0) for s in range(4) for t in range(2)])
    solver.add(oil_count >= 1)

# Condition 2: No wall has the work of only one student.
# For any two paintings on the same wall, their student indices must differ.
for s1 in range(4):
    for t1 in range(2):
        for s2 in range(4):
            for t2 in range(2):
                if (s1, t1) < (s2, t2):  # avoid duplicate pairs
                    solver.add(Implies(wall[s1][t1] == wall[s2][t2], s1 != s2))

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs.
for t1 in range(2):
    for t2 in range(2):
        solver.add(wall[FRANZ][t1] != wall[ISAACS][t2])

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
solver.add(wall[GREENE][WATERCOLOR] == wall[FRANZ][OIL])
solver.add(pos[GREENE][WATERCOLOR] == 0)

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[ISAACS][OIL] == 4)
solver.add(pos[ISAACS][OIL] == 1)

# Given: Hidalgo's oil is displayed on wall 2.
solver.add(wall[HIDALGO][OIL] == 2)

# Now test each option
options = [
    ("A", wall[FRANZ][OIL] == 2),
    ("B", wall[GREENE][WATERCOLOR] == 2),
    ("C", wall[GREENE][OIL] == 2),
    ("D", wall[HIDALGO][WATERCOLOR] == 2),
    ("E", wall[ISAACS][WATERCOLOR] == 2)
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