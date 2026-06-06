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
# - upper[w]: student and type for painting in upper position on wall w
# - lower[w]: student and type for painting in lower position on wall w
# Represent as (student, type) pairs using two Int variables per painting
upper_student = [Int('upper_student_%d' % w) for w in range(4)]
upper_type = [Int('upper_type_%d' % w) for w in range(4)]
lower_student = [Int('lower_student_%d' % w) for w in range(4)]
lower_type = [Int('lower_type_%d' % w) for w in range(4)]

# Helper to map student constants to integers
student_to_int = {Franz: 0, Greene: 1, Hidalgo: 2, Isaacs: 3}
int_to_student = {0: Franz, 1: Greene, 2: Hidalgo, 3: Isaacs}

# Helper to map type constants to integers
type_to_int = {Oil: 0, Watercolor: 1}
int_to_type = {0: Oil, 1: Watercolor}

# Constraint 1: No wall has only watercolors
for w in range(4):
    solver.add(Or(
        upper_type[w] == type_to_int[Oil],
        lower_type[w] == type_to_int[Oil]
    ))

# Constraint 2: No wall has only one student's work (i.e., at least two different students per wall)
for w in range(4):
    solver.add(Or(
        upper_student[w] != lower_student[w]
    ))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(And(
        Or(upper_student[w] == student_to_int[Franz], lower_student[w] == student_to_int[Franz]),
        Or(upper_student[w] == student_to_int[Isaacs], lower_student[w] == student_to_int[Isaacs])
    )))

# Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
# Find the wall where Franz's oil is displayed (either upper or lower)
franz_oil_wall = Int('franz_oil_wall')
solver.add(franz_oil_wall >= 0, franz_oil_wall <= 3)
# Franz's oil is either upper or lower on franz_oil_wall
solver.add(Or(
    And(upper_student[franz_oil_wall] == student_to_int[Franz], upper_type[franz_oil_wall] == type_to_int[Oil]),
    And(lower_student[franz_oil_wall] == student_to_int[Franz], lower_type[franz_oil_wall] == type_to_int[Oil])
))
# Greene's watercolor is in the upper position of franz_oil_wall
solver.add(upper_student[franz_oil_wall] == student_to_int[Greene])
solver.add(upper_type[franz_oil_wall] == type_to_int[Watercolor])

# Constraint 5: Isaacs's oil is in the lower position of wall 4 (index 3)
solver.add(lower_student[3] == student_to_int[Isaacs])
solver.add(lower_type[3] == type_to_int[Oil])

# Define the options as constraints on the lower paintings
# Option A: Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil
opt_a_constr = And(
    lower_student[0] == student_to_int[Franz], lower_type[0] == type_to_int[Oil],
    lower_student[1] == student_to_int[Franz], lower_type[1] == type_to_int[Watercolor],
    lower_student[2] == student_to_int[Greene], lower_type[2] == type_to_int[Oil],
    lower_student[3] == student_to_int[Isaacs], lower_type[3] == type_to_int[Oil]
)

# Option B: Franz's oil, Hidalgo's watercolor, Isaacs's watercolor, Isaacs's oil
opt_b_constr = And(
    lower_student[0] == student_to_int[Franz], lower_type[0] == type_to_int[Oil],
    lower_student[1] == student_to_int[Hidalgo], lower_type[1] == type_to_int[Watercolor],
    lower_student[2] == student_to_int[Isaacs], lower_type[2] == type_to_int[Watercolor],
    lower_student[3] == student_to_int[Isaacs], lower_type[3] == type_to_int[Oil]
)

# Option C: Greene's oil, Franz's oil, Isaacs's oil, Hidalgo's oil
opt_c_constr = And(
    lower_student[0] == student_to_int[Greene], lower_type[0] == type_to_int[Oil],
    lower_student[1] == student_to_int[Franz], lower_type[1] == type_to_int[Oil],
    lower_student[2] == student_to_int[Isaacs], lower_type[2] == type_to_int[Oil],
    lower_student[3] == student_to_int[Hidalgo], lower_type[3] == type_to_int[Oil]
)

# Option D: Hidalgo's oil, Greene's oil, Greene's watercolor, Isaacs's oil
opt_d_constr = And(
    lower_student[0] == student_to_int[Hidalgo], lower_type[0] == type_to_int[Oil],
    lower_student[1] == student_to_int[Greene], lower_type[1] == type_to_int[Oil],
    lower_student[2] == student_to_int[Greene], lower_type[2] == type_to_int[Watercolor],
    lower_student[3] == student_to_int[Isaacs], lower_type[3] == type_to_int[Oil]
)

# Option E: Hidalgo's watercolor, Franz's oil, Greene's oil, Isaacs's oil
opt_e_constr = And(
    lower_student[0] == student_to_int[Hidalgo], lower_type[0] == type_to_int[Watercolor],
    lower_student[1] == student_student[1] == student_to_int[Franz], lower_type[1] == type_to_int[Oil],
    lower_student[2] == student_to_int[Greene], lower_type[2] == type_to_int[Oil],
    lower_student[3] == student_to_int[Isaacs], lower_type[3] == type_to_int[Oil]
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