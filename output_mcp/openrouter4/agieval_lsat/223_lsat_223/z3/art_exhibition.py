from z3 import *

# Students: 0=Franz, 1=Greene, 2=Hidalgo, 3=Isaacs
# Types: 0=oil, 1=watercolor
# Total paintings: 8

walls = [[Int(f"wall_{s}_{t}") for t in range(2)] for s in range(4)]
positions = [[Int(f"pos_{s}_{t}") for t in range(2)] for s in range(4)]

solver = Solver()

# Domain constraints: walls in 1..4, positions in 0..1 (0=upper, 1=lower)
for s in range(4):
    for t in range(2):
        solver.add(walls[s][t] >= 1, walls[s][t] <= 4)
        solver.add(positions[s][t] >= 0, positions[s][t] <= 1)

# Condition: Each wall has exactly one upper and one lower painting.
for w in range(1, 5):
    upper_count = Sum([If(And(walls[s][t] == w, positions[s][t] == 0), 1, 0) for s in range(4) for t in range(2)])
    lower_count = Sum([If(And(walls[s][t] == w, positions[s][t] == 1), 1, 0) for s in range(4) for t in range(2)])
    solver.add(upper_count == 1)
    solver.add(lower_count == 1)

# Condition 1: No wall has only watercolors -> each wall has at least one oil.
for w in range(1, 5):
    oil_count = Sum([If(And(walls[s][0] == w), 1, 0) for s in range(4)])  # oil is type 0
    solver.add(oil_count >= 1)

# Condition 2: No wall has work of only one student -> each wall has paintings by exactly 2 different students.
for w in range(1, 5):
    # For each student, check if they have at least one painting on wall w
    student_on_wall = [Or([walls[s][t] == w for t in range(2)]) for s in range(4)]
    # Count how many students are on this wall — must be exactly 2
    solver.add(Sum([If(student_on_wall[s], 1, 0) for s in range(4)]) == 2)

# Condition 3: No wall has both Franz (s=0) and Isaacs (s=3).
for w in range(1, 5):
    franz_on_wall = Or([walls[0][t] == w for t in range(2)])
    isaacs_on_wall = Or([walls[3][t] == w for t in range(2)])
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Condition 4: Greene's watercolor (s=1, t=1) is in upper position of the wall on which Franz's oil (s=0, t=0) is displayed.
solver.add(walls[1][1] == walls[0][0])  # same wall
solver.add(positions[1][1] == 0)  # upper position

# Condition 5: Isaacs's oil (s=3, t=0) is in lower position of wall 4.
solver.add(walls[3][0] == 4)
solver.add(positions[3][0] == 1)

# Additional condition from Q: Franz's oil is displayed on wall 1.
solver.add(walls[0][0] == 1)

# Now evaluate each option
options = [
    ("A", walls[0][1] == 4),   # Franz's watercolor on wall 4
    ("B", walls[1][0] == 2),   # Greene's oil on wall 2
    ("C", walls[1][1] == 2),   # Greene's watercolor on wall 2
    ("D", walls[2][1] == 3),   # Hidalgo's watercolor on wall 3
    ("E", walls[3][0] == 1),   # Isaacs's oil on wall 1
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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