from z3 import *

solver = Solver()

# Constants
STUDENTS = 4  # 0=Franz, 1=Greene, 2=Hidalgo, 3=Isaacs
WALLS = 4     # 1,2,3,4
POSITIONS = 2 # 0=upper, 1=lower
TYPES = 2     # 0=oil, 1=watercolor

# Variables: for each wall (0-indexed) and position, we have student and type
student = [[Int(f"student_{w+1}_{p}") for p in range(POSITIONS)] for w in range(WALLS)]
type_ = [[Int(f"type_{w+1}_{p}") for p in range(POSITIONS)] for w in range(WALLS)]

# Domain constraints
for w in range(WALLS):
    for p in range(POSITIONS):
        solver.add(And(student[w][p] >= 0, student[w][p] < STUDENTS))
        solver.add(And(type_[w][p] >= 0, type_[w][p] < TYPES))

# Each student has exactly one oil and one watercolor
for s in range(STUDENTS):
    oil_count = Sum([If(And(student[w][p] == s, type_[w][p] == 0), 1, 0) for w in range(WALLS) for p in range(POSITIONS)])
    water_count = Sum([If(And(student[w][p] == s, type_[w][p] == 1), 1, 0) for w in range(WALLS) for p in range(POSITIONS)])
    solver.add(oil_count == 1)
    solver.add(water_count == 1)

# Constraint 1: No wall has only watercolors (each wall has at least one oil)
for w in range(WALLS):
    solver.add(Or([type_[w][p] == 0 for p in range(POSITIONS)]))

# Constraint 2: No wall has the work of only one student (two different students on each wall)
for w in range(WALLS):
    solver.add(student[w][0] != student[w][1])

# Constraint 3: No wall has both Franz and Isaacs
for w in range(WALLS):
    solver.add(Not(And(student[w][0] == 0, student[w][1] == 3)))
    solver.add(Not(And(student[w][0] == 3, student[w][1] == 0)))

# Constraint 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
for w in range(WALLS):
    franz_oil_on_this_wall = Or([And(student[w][p] == 0, type_[w][p] == 0) for p in range(POSITIONS)])
    solver.add(Implies(franz_oil_on_this_wall, And(student[w][0] == 1, type_[w][0] == 1)))

# Constraint 5: Isaacs's oil is displayed in the lower position of wall 4
solver.add(student[3][1] == 3)  # wall index 3 = wall 4, position 1 = lower
solver.add(type_[3][1] == 0)    # oil

# Given: Hidalgo's oil is displayed on wall 2
solver.add(Or([And(student[1][p] == 2, type_[1][p] == 0) for p in range(POSITIONS)]))  # wall index 1 = wall 2

# Now test each option
options = {
    "A": (0, 0),  # Franz's oil
    "B": (1, 1),  # Greene's watercolor
    "C": (1, 0),  # Greene's oil
    "D": (2, 1),  # Hidalgo's watercolor
    "E": (3, 1),  # Isaacs's watercolor
}

found_options = []
for letter, (s, t) in options.items():
    solver.push()
    # Add constraint: this painting is on wall 2 (any position)
    solver.add(Or([And(student[1][p] == s, type_[1][p] == t) for p in range(POSITIONS)]))
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