from z3 import *

# Define students and painting types
Student = EnumSort('Student', ['Franz', 'Greene', 'Hidalgo', 'Isaacs'])
PaintingType = EnumSort('PaintingType', ['Oil', 'Watercolor'])

Franz, Greene, Hidalgo, Isaacs = Student
Oil, Watercolor = PaintingType

# Define walls and positions
Wall = IntSort()
Position = EnumSort('Position', ['Upper', 'Lower'])
Upper, Lower = Position

# Create solver
solver = Solver()

# Decision variables:
# - upper[w]: painting in upper position on wall w
# - lower[w]: painting in lower position on wall w
# Each painting is a tuple (student, painting_type)
upper = [Tuple('upper_%d' % w, Student, PaintingType) for w in range(1, 5)]
lower = [Tuple('lower_%d' % w, Student, PaintingType) for w in range(1, 5)]

# Helper functions to extract student and type from a painting tuple
student = Function('student', TupleSort(Student, PaintingType), Student)
type_ = Function('type_', TupleSort(Student, PaintingType), PaintingType)

# Add constraints for each wall
for w in range(1, 5):
    solver.add(upper[w-1][0] != lower[w-1][0])  # Different students on the same wall
    
# Constraint 1: No wall has only watercolors
for w in range(1, 5):
    solver.add(Or(
        type_(upper[w-1]) == Oil,
        type_(lower[w-1]) == Oil
    ))

# Constraint 2: No wall has only one student's work
for w in range(1, 5):
    solver.add(Or(
        student(upper[w-1]) != student(lower[w-1]),
        False  # This is a placeholder; we need to ensure at least two students per wall
    ))
    # Actually, the above is redundant because we already enforce different students per wall.
    # So this constraint is already satisfied by the first constraint.

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    solver.add(Not(And(
        Or(student(upper[w-1]) == Franz, student(lower[w-1]) == Franz),
        Or(student(upper[w-1]) == Isaacs, student(lower[w-1]) == Isaacs)
    )))

# Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
# Find the wall where Franz's oil is displayed (either upper or lower)
franz_oil_wall = Int('franz_oil_wall')
solver.add(franz_oil_wall >= 1, franz_oil_wall <= 4)
# Franz's oil is either upper or lower on franz_oil_wall
solver.add(Or(
    And(student(upper[franz_oil_wall-1]) == Franz, type_(upper[franz_oil_wall-1]) == Oil),
    And(student(lower[franz_oil_wall-1]) == Franz, type_(lower[franz_oil_wall-1]) == Oil)
))
# Greene's watercolor is in the upper position of franz_oil_wall
solver.add(type_(upper[franz_oil_wall-1]) == Watercolor)
solver.add(student(upper[franz_oil_wall-1]) == Greene)

# Constraint 5: Isaacs's oil is in the lower position of wall 4
solver.add(student(lower[3]) == Isaacs)
solver.add(type_(lower[3]) == Oil)

# Now, evaluate each option for the lower positions on walls 1-4
# Each option is a list of 4 paintings (student, type) for lower positions on walls 1-4

# Helper to create a painting tuple
make_painting = Function('make_painting', Student, PaintingType, TupleSort(Student, PaintingType))

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