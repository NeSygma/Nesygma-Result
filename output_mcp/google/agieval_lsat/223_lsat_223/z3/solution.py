from z3 import *

# Students: F=0, G=1, H=2, I=3
# Types: O=0, W=1
# Walls: 0, 1, 2, 3
# Positions: 0 (U), 1 (L)

solver = Solver()

# Variables: student_at[wall][pos], type_at[wall][pos]
student_at = [[Int(f"s_{w}_{p}") for p in range(2)] for w in range(4)]
type_at = [[Int(f"t_{w}_{p}") for p in range(2)] for w in range(4)]

# Domain constraints
for w in range(4):
    for p in range(2):
        solver.add(student_at[w][p] >= 0, student_at[w][p] <= 3)
        solver.add(type_at[w][p] >= 0, type_at[w][p] <= 1)

# Each student has exactly one oil and one watercolor
for s in range(4):
    # Count occurrences of (s, 0) and (s, 1)
    solver.add(Sum([If(And(student_at[w][p] == s, type_at[w][p] == 0), 1, 0) for w in range(4) for p in range(2)]) == 1)
    solver.add(Sum([If(And(student_at[w][p] == s, type_at[w][p] == 1), 1, 0) for w in range(4) for p in range(2)]) == 1)

# No wall has only watercolors (each wall must have at least one oil)
for w in range(4):
    solver.add(Or(type_at[w][0] == 0, type_at[w][1] == 0))

# No wall has only one student
for w in range(4):
    solver.add(student_at[w][0] != student_at[w][1])

# No wall has both F and I
for w in range(4):
    solver.add(Not(And(student_at[w][0] == 0, student_at[w][1] == 3)))
    solver.add(Not(And(student_at[w][0] == 3, student_at[w][1] == 0)))

# Isaacs's oil (IO) is in the lower position of wall 4 (index 3)
solver.add(student_at[3][1] == 3, type_at[3][1] == 0)

# If Franz's oil (FO) is on wall 1 (index 0)
# FO is (0, 0)
# Greene's watercolor (GW) is in the upper position of the wall on which Franz's oil (FO) is
# GW is (1, 1)
# Let's add the condition: FO is on wall 0
# Find where (0, 0) is
fo_wall = Int('fo_wall')
solver.add(fo_wall >= 0, fo_wall <= 3)
solver.add(Or([And(student_at[w][p] == 0, type_at[w][p] == 0, fo_wall == w) for w in range(4) for p in range(2)]))
solver.add(fo_wall == 0)

# Greene's watercolor (GW) is in the upper position of the wall on which Franz's oil (FO) is
# GW is (1, 1)
solver.add(student_at[0][0] == 1, type_at[0][0] == 1)

# Options
# (A) Franz's watercolor (FW) is on wall 4 (index 3)
# (B) Greene's oil (GO) is on wall 2 (index 1)
# (C) Greene's watercolor (GW) is on wall 2 (index 1)
# (D) Hidalgo's watercolor (HW) is on wall 3 (index 2)
# (E) Isaacs's oil (IO) is on wall 1 (index 0)

options = [
    ("A", And(student_at[3][0] == 0, type_at[3][0] == 1)),
    ("B", And(student_at[1][0] == 1, type_at[1][0] == 0)),
    ("C", And(student_at[1][0] == 1, type_at[1][0] == 1)),
    ("D", And(student_at[2][0] == 2, type_at[2][0] == 1)),
    ("E", And(student_at[0][0] == 3, type_at[0][0] == 0))
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