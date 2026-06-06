from z3 import *

# Painting IDs
# 0: Franz_oil, 1: Franz_watercolor, 2: Greene_oil, 3: Greene_watercolor,
# 4: Hidalgo_oil, 5: Hidalgo_watercolor, 6: Isaacs_oil, 7: Isaacs_watercolor

# Student mapping
def student(p):
    # p is an integer expression
    # return student index: 0 Franz, 1 Greene, 2 Hidalgo, 3 Isaacs
    return If(Or(p == 0, p == 1), 0,
           If(Or(p == 2, p == 3), 1,
           If(Or(p == 4, p == 5), 2, 3)))

# Oil painting check
def is_oil(p):
    return Or(p == 0, p == 2, p == 4, p == 6)

# Watercolor painting check
def is_watercolor(p):
    return Or(p == 1, p == 3, p == 5, p == 7)

# Create solver
solver = Solver()

# Variables for each wall: upper and lower
upper = [Int(f'upper_{w}') for w in range(1,5)]
lower = [Int(f'lower_{w}') for w in range(1,5)]

# Domain constraints: each painting ID between 0 and 7
for w in range(4):
    solver.add(upper[w] >= 0, upper[w] <= 7)
    solver.add(lower[w] >= 0, lower[w] <= 7)

# All 8 paintings are distinct
all_paintings = upper + lower
solver.add(Distinct(all_paintings))

# Constraint: No wall has only watercolors
for w in range(4):
    solver.add(Not(And(is_watercolor(upper[w]), is_watercolor(lower[w]))))

# Constraint: No wall has the work of only one student
for w in range(4):
    solver.add(student(upper[w]) != student(lower[w]))

# Constraint: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(Or(student(upper[w]) == 0, student(lower[w]) == 0),
                       Or(student(upper[w]) == 3, student(lower[w]) == 3))))

# Constraint: Greene's watercolor is upper on the wall where Franz's oil is displayed
# That means there exists a wall w such that upper[w] == 3 and lower[w] == 0
solver.add(Or([And(upper[w] == 3, lower[w] == 0) for w in range(4)]))

# Constraint: Isaacs's oil is lower on wall 4
solver.add(lower[3] == 6)  # index 3 corresponds to wall 4

# Now define the answer choices
options = [
    ("A", [0, 1, 2, 6]),   # lower walls 1,2,3,4
    ("B", [0, 5, 7, 6]),
    ("C", [2, 0, 6, 4]),
    ("D", [4, 2, 3, 6]),
    ("E", [5, 0, 2, 6])
]

found_options = []
for letter, lower_list in options:
    solver.push()
    # Set lower positions according to the option
    for w in range(4):
        solver.add(lower[w] == lower_list[w])
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")