from z3 import *

# Initialize solver
solver = Solver()

# Students and mediums
students = ['F', 'G', 'H', 'I']  # Franz, Greene, Hidalgo, Isaacs
mediums = ['O', 'W']  # Oil, Watercolor

# Walls and positions
walls = [1, 2, 3, 4]
positions = ['U', 'L']  # Upper, Lower

# Create a 3D array: wall x position x (student, medium)
# We'll use a dictionary of dictionaries of tuples
wall_paintings = {}
for w in walls:
    wall_paintings[w] = {}
    for p in positions:
        wall_paintings[w][p] = (Int(f'wall_{w}_{p}_student'), Int(f'wall_{w}_{p}_medium'))

# Helper functions to extract student and medium
def get_student(w, p):
    return wall_paintings[w][p][0]

def get_medium(w, p):
    return wall_paintings[w][p][1]

# Each student has exactly one oil and one watercolor
student_mediums = {}
for s in students:
    student_mediums[s] = {'O': Bool(f'{s}_has_O'), 'W': Bool(f'{s}_has_W')}
    solver.add(And(student_mediums[s]['O'], student_mediums[s]['W']))

# Each wall has exactly two paintings (one upper, one lower)
for w in walls:
    for s in students:
        solver.add(Or(
            get_student(w, 'U') == s,
            get_student(w, 'L') == s
        ))

# No wall has only watercolors
for w in walls:
    solver.add(Or(
        And(get_medium(w, 'U') == 'O', get_medium(w, 'L') == 'O'),
        And(get_medium(w, 'U') == 'O', get_medium(w, 'L') == 'W'),
        And(get_medium(w, 'U') == 'W', get_medium(w, 'L') == 'O')
    ))

# No wall has only one student's work
for w in walls:
    solver.add(Or(
        And(get_student(w, 'U') == 'F', get_student(w, 'L') != 'F'),
        And(get_student(w, 'U') == 'G', get_student(w, 'L') != 'G'),
        And(get_student(w, 'U') == 'H', get_student(w, 'L') != 'H'),
        And(get_student(w, 'U') == 'I', get_student(w, 'L') != 'I'),
        And(get_student(w, 'U') != 'F', get_student(w, 'L') == 'F'),
        And(get_student(w, 'U') != 'G', get_student(w, 'L') == 'G'),
        And(get_student(w, 'U') != 'H', get_student(w, 'L') == 'H'),
        And(get_student(w, 'U') != 'I', get_student(w, 'L') == 'I')
    ))

# No wall has both Franz and Isaacs
for w in walls:
    solver.add(Not(And(
        Or([get_student(w, p) == 'F' for p in positions]),
        Or([get_student(w, p) == 'I' for p in positions])
    )))

# Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
franz_oil_wall = Int('franz_oil_wall')
solver.add(franz_oil_wall >= 1, franz_oil_wall <= 4)
for w in walls:
    solver.add(Implies(
        get_student(w, 'U') == 'F',
        get_medium(w, 'U') == 'O'
    ))
    solver.add(Implies(
        get_student(w, 'U') == 'F',
        And(
            get_student(franz_oil_wall, 'U') == 'G',
            get_medium(franz_oil_wall, 'U') == 'W'
        )
    ))

# Isaacs's oil is in the lower position of wall 4
solver.add(get_student(4, 'L') == 'I')
solver.add(get_medium(4, 'L') == 'O')

# Isaacs's watercolor is on wall 2 (either upper or lower)
solver.add(Or(
    And(get_student(2, 'U') == 'I', get_medium(2, 'U') == 'W'),
    And(get_student(2, 'L') == 'I', get_medium(2, 'L') == 'W')
))

# Franz's oil is on wall 3 (either upper or lower)
solver.add(Or(
    And(get_student(3, 'U') == 'F', get_medium(3, 'U') == 'O'),
    And(get_student(3, 'L') == 'F', get_medium(3, 'L') == 'O')
))

# Now, evaluate the options for wall 1
# We need to check which option must be true on wall 1
# Options:
# (A) Franz's watercolor
# (B) Greene's oil
# (C) Greene's watercolor
# (D) Hidalgo's oil
# (E) Hidalgo's watercolor

# We'll check each option by adding a constraint that it is the only possible painting on wall 1
# and see if the solver can find a model.

found_options = []

# Option A: Franz's watercolor on wall 1
solver.push()
solver.add(And(
    get_student(1, 'U') == 'F',
    get_medium(1, 'U') == 'W'
))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Greene's oil on wall 1
solver.push()
solver.add(And(
    get_student(1, 'U') == 'G',
    get_medium(1, 'U') == 'O'
))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Greene's watercolor on wall 1
solver.push()
solver.add(And(
    get_student(1, 'U') == 'G',
    get_medium(1, 'U') == 'W'
))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hidalgo's oil on wall 1
solver.push()
solver.add(And(
    get_student(1, 'U') == 'H',
    get_medium(1, 'U') == 'O'
))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Hidalgo's watercolor on wall 1
solver.push()
solver.add(And(
    get_student(1, 'U') == 'H',
    get_medium(1, 'U') == 'W'
))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")