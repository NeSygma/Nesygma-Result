from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Students
Franz = 0
Greene = 1
Hidalgo = 2
Isaacs = 3

# Painting types
OIL = 0
WATERCOLOR = 1

# Total paintings: 8 (4 students * 2 types)
num_paintings = 8

# Decision variables for paintings (using Z3 arrays for symbolic indexing)
painting_student = Array('painting_student', IntSort(), IntSort())
painting_type = Array('painting_type', IntSort(), IntSort())

# Wall assignments: 4 walls, each with upper (0) and lower (1) positions
wall_assignment = [[Int(f'wall_{w}_pos_{p}') for p in range(2)] for w in range(4)]

# Solver
solver = Solver()

# Each painting ID is from 0 to 7
for i in range(num_paintings):
    solver.add(And(
        painting_student[i] >= 0, painting_student[i] <= 3,
        painting_type[i] >= 0, painting_type[i] <= 1
    ))

# Each student has exactly one oil and one watercolor
for s in range(4):
    oils = Sum([If(And(painting_student[i] == s, painting_type[i] == OIL), 1, 0) for i in range(num_paintings)])
    watercolors = Sum([If(And(painting_student[i] == s, painting_type[i] == WATERCOLOR), 1, 0) for i in range(num_paintings)])
    solver.add(oils == 1)
    solver.add(watercolors == 1)

# Each painting ID is used exactly once across all wall positions
all_assignments = [wall_assignment[w][p] for w in range(4) for p in range(2)]
solver.add(Distinct(all_assignments))
for a in all_assignments:
    solver.add(a >= 0, a < num_paintings)

# Constraint 1: No wall has only watercolors (each wall has at least one oil)
for w in range(4):
    p1, p2 = wall_assignment[w][0], wall_assignment[w][1]
    solver.add(Or(
        painting_type[p1] == OIL,
        painting_type[p2] == OIL
    ))

# Constraint 2: No wall has only one student's work (paintings on a wall are from different students)
for w in range(4):
    p1, p2 = wall_assignment[w][0], wall_assignment[w][1]
    solver.add(painting_student[p1] != painting_student[p2])

# Constraint 3: No wall has both Franz and Isaacs
for w in range(4):
    p1, p2 = wall_assignment[w][0], wall_assignment[w][1]
    solver.add(Not(And(
        Or(painting_student[p1] == Franz, painting_student[p2] == Franz),
        Or(painting_student[p1] == Isaacs, painting_student[p2] == Isaacs)
    )))

# Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is displayed
for w in range(4):
    p1, p2 = wall_assignment[w][0], wall_assignment[w][1]
    is_franz_oil = Or(
        And(painting_student[p1] == Franz, painting_type[p1] == OIL),
        And(painting_student[p2] == Franz, painting_type[p2] == OIL)
    )
    greene_watercolor_upper = And(
        painting_student[p1] == Greene,
        painting_type[p1] == WATERCOLOR
    )
    solver.add(Implies(is_franz_oil, greene_watercolor_upper))

# Constraint 5: Isaacs's oil is in the lower position of wall 4
wall4_lower = wall_assignment[3][1]
solver.add(And(
    painting_student[wall4_lower] == Isaacs,
    painting_type[wall4_lower] == OIL
))

# Identify paintings by student for option constraints
# We need to find the painting IDs for each student's oil and watercolor
franz_oil = Int('franz_oil')
franz_watercolor = Int('franz_watercolor')
greene_oil = Int('greene_oil')
greene_watercolor = Int('greene_watercolor')
hidalgo_oil = Int('hidalgo_oil')
hidalgo_watercolor = Int('hidalgo_watercolor')
isaacs_oil = Int('isaacs_oil')
isaacs_watercolor = Int('isaacs_watercolor')

solver.add(
    painting_student[franz_oil] == Franz, painting_type[franz_oil] == OIL,
    painting_student[franz_watercolor] == Franz, painting_type[franz_watercolor] == WATERCOLOR,
    painting_student[greene_oil] == Greene, painting_type[greene_oil] == OIL,
    painting_student[greene_watercolor] == Greene, painting_type[greene_watercolor] == WATERCOLOR,
    painting_student[hidalgo_oil] == Hidalgo, painting_type[hidalgo_oil] == OIL,
    painting_student[hidalgo_watercolor] == Hidalgo, painting_type[hidalgo_watercolor] == WATERCOLOR,
    painting_student[isaacs_oil] == Isaacs, painting_type[isaacs_oil] == OIL,
    painting_student[isaacs_watercolor] == Isaacs, painting_type[isaacs_watercolor] == WATERCOLOR
)

# Option constraints
# Option A: Both of Franz's paintings and both of Greene's paintings are in lower positions
option_a_constr = And(
    Or([wall_assignment[w][1] == franz_oil for w in range(4)]),
    Or([wall_assignment[w][1] == franz_watercolor for w in range(4)]),
    Or([wall_assignment[w][1] == greene_oil for w in range(4)]),
    Or([wall_assignment[w][1] == greene_watercolor for w in range(4)])
)

# Option B: Both of Franz's paintings and both of Greene's paintings are in upper positions
option_b_constr = And(
    Or([wall_assignment[w][0] == franz_oil for w in range(4)]),
    Or([wall_assignment[w][0] == franz_watercolor for w in range(4)]),
    Or([wall_assignment[w][0] == greene_oil for w in range(4)]),
    Or([wall_assignment[w][0] == greene_watercolor for w in range(4)])
)

# Option C: Both of Franz's paintings and both of Hidalgo's paintings are in upper positions
option_c_constr = And(
    Or([wall_assignment[w][0] == franz_oil for w in range(4)]),
    Or([wall_assignment[w][0] == franz_watercolor for w in range(4)]),
    Or([wall_assignment[w][0] == hidalgo_oil for w in range(4)]),
    Or([wall_assignment[w][0] == hidalgo_watercolor for w in range(4)])
)

# Option D: Both of Greene's paintings and both of Hidalgo's paintings are in lower positions
option_d_constr = And(
    Or([wall_assignment[w][1] == greene_oil for w in range(4)]),
    Or([wall_assignment[w][1] == greene_watercolor for w in range(4)]),
    Or([wall_assignment[w][1] == hidalgo_oil for w in range(4)]),
    Or([wall_assignment[w][1] == hidalgo_watercolor for w in range(4)])
)

# Option E: Both of Greene's paintings and both of Hidalgo's paintings are in upper positions
option_e_constr = And(
    Or([wall_assignment[w][0] == greene_oil for w in range(4)]),
    Or([wall_assignment[w][0] == greene_watercolor for w in range(4)]),
    Or([wall_assignment[w][0] == hidalgo_oil for w in range(4)]),
    Or([wall_assignment[w][0] == hidalgo_watercolor for w in range(4)])
)

# Evaluate multiple-choice options
found_options = []
for letter, constr in [("A", option_a_constr), ("B", option_b_constr), ("C", option_c_constr), ("D", option_d_constr), ("E", option_e_constr)]:
    solver.push()
    solver.add(constr)
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