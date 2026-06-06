from z3 import *

# BENCHMARK_MODE is ON for this problem
BENCHMARK_MODE = True

# Declare students and painting types
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
painting_types = ["oil", "watercolor"]
walls = [1, 2, 3, 4]
positions = ["upper", "lower"]

# Create symbolic variables for each painting assignment
# Each painting is uniquely identified by (student, painting_type)
# We will represent assignments as a dictionary of dictionaries:
# assignment[wall][position] = (student, painting_type)
assignment = {w: {p: (String(f"assignment_{w}_{p}_student"), String(f"assignment_{w}_{p}_type")) for p in positions} for w in walls}

# Helper function to extract student and painting type from a tuple
student_of = lambda t: t[0]
painting_type_of = lambda t: t[1]

solver = Solver()

# Constraint 1: No wall has only watercolors displayed on it
for w in walls:
    upper = assignment[w]["upper"]
    lower = assignment[w]["lower"]
    solver.add(Or(
        painting_type_of(lower) == "oil",
        painting_type_of(upper) == "oil"
    ))

# Constraint 2: No wall has the work of only one student displayed on it
for w in walls:
    upper = assignment[w]["upper"]
    lower = assignment[w]["lower"]
    solver.add(Or(
        student_of(upper) != student_of(lower),
        And(
            student_of(upper) == student_of(lower),
            painting_type_of(upper) != painting_type_of(lower)
        )
    ))

# Constraint 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it
for w in walls:
    upper = assignment[w]["upper"]
    lower = assignment[w]["lower"]
    solver.add(Not(And(
        Or(student_of(upper) == "Franz", student_of(lower) == "Franz"),
        Or(student_of(upper) == "Isaacs", student_of(lower) == "Isaacs")
    )))

# Constraint 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed
for w in walls:
    upper = assignment[w]["upper"]
    lower = assignment[w]["lower"]
    franz_oil_on_wall = Or(
        And(student_of(upper) == "Franz", painting_type_of(upper) == "oil"),
        And(student_of(lower) == "Franz", painting_type_of(lower) == "oil")
    )
    greene_watercolor_upper = And(
        student_of(upper) == "Greene",
        painting_type_of(upper) == "watercolor"
    )
    solver.add(Implies(franz_oil_on_wall, greene_watercolor_upper))

# Constraint 5: Isaacs's oil is displayed in the lower position of wall 4
solver.add(And(
    student_of(assignment[4]["lower"]) == "Isaacs",
    painting_type_of(assignment[4]["lower"]) == "oil"
))

# Additional constraint: Hidalgo's oil is displayed on wall 2 (upper position)
solver.add(And(
    student_of(assignment[2]["upper"]) == "Hidalgo",
    painting_type_of(assignment[2]["upper"]) == "oil"
))

# Now, we need to check which of the options could also be displayed on wall 2
# We will test each option by adding it as a constraint and checking satisfiability

# Extract the current assignment for wall 2
wall2_upper_student, wall2_upper_type = assignment[2]["upper"]
wall2_lower_student, wall2_lower_type = assignment[2]["lower"]

# Define the options as constraints
# Option A: Franz's oil on wall 2 (upper)
opt_a_constr = And(
    wall2_upper_student == "Franz",
    wall2_upper_type == "oil"
)

# Option B: Greene's watercolor on wall 2 (upper)
opt_b_constr = And(
    wall2_upper_student == "Greene",
    wall2_upper_type == "watercolor"
)

# Option C: Greene's oil on wall 2 (upper)
opt_c_constr = And(
    wall2_upper_student == "Greene",
    wall2_upper_type == "oil"
)

# Option D: Hidalgo's watercolor on wall 2 (lower)
opt_d_constr = And(
    wall2_lower_student == "Hidalgo",
    wall2_lower_type == "watercolor"
)

# Option E: Isaacs's watercolor on wall 2 (upper)
opt_e_constr = And(
    wall2_upper_student == "Isaacs",
    wall2_upper_type == "watercolor"
)

# Test each option
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