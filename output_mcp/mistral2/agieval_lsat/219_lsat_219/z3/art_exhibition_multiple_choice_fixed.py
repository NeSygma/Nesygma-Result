from z3 import *

# Define students and painting types as EnumSort
Student = Datatype('Student')
Student.declare('Franz')
Student.declare('Greene')
Student.declare('Hidalgo')
Student.declare('Isaacs')
Student = Student.create()

PaintingType = Datatype('PaintingType')
PaintingType.declare('Oil')
PaintingType.declare('Watercolor')
PaintingType = PaintingType.create()

# Extract the constants
Franz = Student.Franz
Greene = Student.Greene
Hidalgo = Student.Hidalgo
Isaacs = Student.Isaacs

Oil = PaintingType.Oil
Watercolor = PaintingType.Watercolor

# Define walls and positions
Wall = IntSort()
Position = Datatype('Position')
Position.declare('Upper')
Position.declare('Lower')
Position = Position.create()

Upper = Position.Upper
Lower = Position.Lower

# Create solver
solver = Solver()

# Decision variables:
# - upper[w]: painting in upper position on wall w (tuple of student and type)
# - lower[w]: painting in lower position on wall w (tuple of student and type)
# We represent paintings as tuples (student, type)
# Use a custom sort for paintings
Painting = TupleSort(Student, PaintingType)
upper = [Const('upper_%d' % w, Painting) for w in range(4)]
lower = [Const('lower_%d' % w, Painting) for w in range(4)]

# Helper functions to extract student and type from a painting tuple
student = Function('student', Painting, Student)
type_ = Function('type_', Painting, PaintingType)

# Constraint 1: No wall has only watercolors
for w in range(4):
    solver.add(Or(
        type_(upper[w]) == Oil,
        type_(lower[w]) == Oil
    ))

# Constraint 2: No wall has only one student's work (i.e., at least two different students per wall)
for w in range(4):
    solver.add(Or(
        student(upper[w]) != student(lower[w])
    ))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(
        Or(student(upper[w]) == Franz, student(lower[w]) == Franz),
        Or(student(upper[w]) == Isaacs, student(lower[w]) == Isaacs)
    )))

# Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
# Find the wall where Franz's oil is displayed (either upper or lower)
franz_oil_wall = Int('franz_oil_wall')
solver.add(franz_oil_wall >= 0, franz_oil_wall <= 3)
# Franz's oil is either upper or lower on franz_oil_wall
solver.add(Or(
    And(student(upper[franz_oil_wall]) == Franz, type_(upper[franz_oil_wall]) == Oil),
    And(student(lower[franz_oil_wall]) == Franz, type_(lower[franz_oil_wall]) == Oil)
))
# Greene's watercolor is in the upper position of franz_oil_wall
solver.add(student(upper[franz_oil_wall]) == Greene)
solver.add(type_(upper[franz_oil_wall]) == Watercolor)

# Constraint 5: Isaacs's oil is in the lower position of wall 4 (index 3)
solver.add(student(lower[3]) == Isaacs)
solver.add(type_(lower[3]) == Oil)

# Helper to create a painting tuple
make_painting = Function('make_painting', Student, PaintingType, Painting)

# Define the options as constraints on the lower paintings
# Option A: Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil
opt_a_constr = And(
    make_painting(Franz, Oil) == lower[0],
    make_painting(Franz, Watercolor) == lower[1],
    make_painting(Greene, Oil) == lower[2],
    make_painting(Isaacs, Oil) == lower[3]
)

# Option B: Franz's oil, Hidalgo's watercolor, Isaacs's watercolor, Isaacs's oil
opt_b_constr = And(
    make_painting(Franz, Oil) == lower[0],
    make_painting(Hidalgo, Watercolor) == lower[1],
    make_painting(Isaacs, Watercolor) == lower[2],
    make_painting(Isaacs, Oil) == lower[3]
)

# Option C: Greene's oil, Franz's oil, Isaacs's oil, Hidalgo's oil
opt_c_constr = And(
    make_painting(Greene, Oil) == lower[0],
    make_painting(Franz, Oil) == lower[1],
    make_painting(Isaacs, Oil) == lower[2],
    make_painting(Hidalgo, Oil) == lower[3]
)

# Option D: Hidalgo's oil, Greene's oil, Greene's watercolor, Isaacs's oil
opt_d_constr = And(
    make_painting(Hidalgo, Oil) == lower[0],
    make_painting(Greene, Oil) == lower[1],
    make_painting(Greene, Watercolor) == lower[2],
    make_painting(Isaacs, Oil) == lower[3]
)

# Option E: Hidalgo's watercolor, Franz's oil, Greene's oil, Isaacs's oil
opt_e_constr = And(
    make_painting(Hidalgo, Watercolor) == lower[0],
    make_painting(Franz, Oil) == lower[1],
    make_painting(Greene, Oil) == lower[2],
    make_painting(Isaacs, Oil) == lower[3]
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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