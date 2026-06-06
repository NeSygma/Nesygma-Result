from z3 import *

# Create solver
solver = Solver()

# Define students and painting types
students = ["Franz", "Greene", "Hidalgo", "Isaacs"]
painting_types = ["oil", "watercolor"]

# Create variables: for each wall (1-4), position (upper/lower), we need to know which student and painting type
# We'll use arrays: wall_pos_student[wall][position] = student index
# wall_pos_type[wall][position] = painting type index (0=oil, 1=watercolor)

# For simplicity, let's create variables for each wall and position
# Wall 1: positions 0=upper, 1=lower
w1_u_student = Int('w1_u_student')  # 0=Franz, 1=Greene, 2=Hidalgo, 3=Isaacs
w1_l_student = Int('w1_l_student')
w1_u_type = Int('w1_u_type')  # 0=oil, 1=watercolor
w1_l_type = Int('w1_l_type')

w2_u_student = Int('w2_u_student')
w2_l_student = Int('w2_l_student')
w2_u_type = Int('w2_u_type')
w2_l_type = Int('w2_l_type')

w3_u_student = Int('w3_u_student')
w3_l_student = Int('w3_l_student')
w3_u_type = Int('w3_u_type')
w3_l_type = Int('w3_l_type')

w4_u_student = Int('w4_u_student')
w4_l_student = Int('w4_l_student')
w4_u_type = Int('w4_u_type')
w4_l_type = Int('w4_l_type')

# Domain constraints: student indices 0-3, type indices 0-1
for var in [w1_u_student, w1_l_student, w2_u_student, w2_l_student, 
            w3_u_student, w3_l_student, w4_u_student, w4_l_student]:
    solver.add(var >= 0, var <= 3)
for var in [w1_u_type, w1_l_type, w2_u_type, w2_l_type, 
            w3_u_type, w3_l_type, w4_u_type, w4_l_type]:
    solver.add(var >= 0, var <= 1)

# Constraint 5: Isaacs's oil is in lower position of wall 4
# Isaacs is student index 3, oil is type index 0
solver.add(w4_l_student == 3)
solver.add(w4_l_type == 0)

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is displayed
# Franz is student index 0, Greene is 1, watercolor is type index 1
# We need to find which wall has Franz's oil in some position, and Greene's watercolor in upper position of same wall
# Let's create a variable for the wall where Franz's oil is
franz_oil_wall = Int('franz_oil_wall')
solver.add(franz_oil_wall >= 1, franz_oil_wall <= 4)

# Franz's oil could be in upper or lower position of that wall
franz_oil_pos = Int('franz_oil_pos')  # 0=upper, 1=lower
solver.add(franz_oil_pos >= 0, franz_oil_pos <= 1)

# Greene's watercolor must be in upper position of the same wall
greene_watercolor_wall = Int('greene_watercolor_wall')
solver.add(greene_watercolor_wall >= 1, greene_watercolor_wall <= 4)

# Link them: same wall
solver.add(franz_oil_wall == greene_watercolor_wall)

# Now encode the actual positions
# For each wall, check if Franz's oil is there
solver.add(Or(
    And(franz_oil_wall == 1, franz_oil_pos == 0, w1_u_student == 0, w1_u_type == 0),
    And(franz_oil_wall == 1, franz_oil_pos == 1, w1_l_student == 0, w1_l_type == 0),
    And(franz_oil_wall == 2, franz_oil_pos == 0, w2_u_student == 0, w2_u_type == 0),
    And(franz_oil_wall == 2, franz_oil_pos == 1, w2_l_student == 0, w2_l_type == 0),
    And(franz_oil_wall == 3, franz_oil_pos == 0, w3_u_student == 0, w3_u_type == 0),
    And(franz_oil_wall == 3, franz_oil_pos == 1, w3_l_student == 0, w3_l_type == 0),
    And(franz_oil_wall == 4, franz_oil_pos == 0, w4_u_student == 0, w4_u_type == 0),
    And(franz_oil_wall == 4, franz_oil_pos == 1, w4_l_student == 0, w4_l_type == 0)
))

# Greene's watercolor in upper position of same wall
solver.add(Or(
    And(greene_watercolor_wall == 1, w1_u_student == 1, w1_u_type == 1),
    And(greene_watercolor_wall == 2, w2_u_student == 1, w2_u_type == 1),
    And(greene_watercolor_wall == 3, w3_u_student == 1, w3_u_type == 1),
    And(greene_watercolor_wall == 4, w4_u_student == 1, w4_u_type == 1)
))

# Constraint 1: No wall has only watercolors (each wall must have at least one oil)
# For each wall, at least one position has type 0 (oil)
solver.add(Or(w1_u_type == 0, w1_l_type == 0))
solver.add(Or(w2_u_type == 0, w2_l_type == 0))
solver.add(Or(w3_u_type == 0, w3_l_type == 0))
solver.add(Or(w4_u_type == 0, w4_l_type == 0))  # Already satisfied by constraint 5

# Constraint 2: No wall has work of only one student
# For each wall, the two students must be different
solver.add(w1_u_student != w1_l_student)
solver.add(w2_u_student != w2_l_student)
solver.add(w3_u_student != w3_l_student)
solver.add(w4_u_student != w4_l_student)

# Constraint 3: No wall has both Franz and Isaacs together
# For each wall, not (Franz in one position AND Isaacs in other position)
solver.add(Not(And(w1_u_student == 0, w1_l_student == 3)))
solver.add(Not(And(w1_u_student == 3, w1_l_student == 0)))
solver.add(Not(And(w2_u_student == 0, w2_l_student == 3)))
solver.add(Not(And(w2_u_student == 3, w2_l_student == 0)))
solver.add(Not(And(w3_u_student == 0, w3_l_student == 3)))
solver.add(Not(And(w3_u_student == 3, w3_l_student == 0)))
solver.add(Not(And(w4_u_student == 0, w4_l_student == 3)))
solver.add(Not(And(w4_u_student == 3, w4_l_student == 0)))

# Additional constraint: Each student has exactly 2 paintings (1 oil, 1 watercolor)
# We need to count how many times each student appears with each type
# For each student, count oil paintings and watercolor paintings
for s in range(4):
    oil_count = Sum([
        If(And(w1_u_student == s, w1_u_type == 0), 1, 0),
        If(And(w1_l_student == s, w1_l_type == 0), 1, 0),
        If(And(w2_u_student == s, w2_u_type == 0), 1, 0),
        If(And(w2_l_student == s, w2_l_type == 0), 1, 0),
        If(And(w3_u_student == s, w3_u_type == 0), 1, 0),
        If(And(w3_l_student == s, w3_l_type == 0), 1, 0),
        If(And(w4_u_student == s, w4_u_type == 0), 1, 0),
        If(And(w4_l_student == s, w4_l_type == 0), 1, 0)
    ])
    watercolor_count = Sum([
        If(And(w1_u_student == s, w1_u_type == 1), 1, 0),
        If(And(w1_l_student == s, w1_l_type == 1), 1, 0),
        If(And(w2_u_student == s, w2_u_type == 1), 1, 0),
        If(And(w2_l_student == s, w2_l_type == 1), 1, 0),
        If(And(w3_u_student == s, w3_u_type == 1), 1, 0),
        If(And(w3_l_student == s, w3_l_type == 1), 1, 0),
        If(And(w4_u_student == s, w4_u_type == 1), 1, 0),
        If(And(w4_l_student == s, w4_l_type == 1), 1, 0)
    ])
    solver.add(oil_count == 1)
    solver.add(watercolor_count == 1)

# Now evaluate each answer choice
# Answer choices give the lower position paintings for walls 1-4 in order
# Each choice specifies: student's painting type

# Map student names to indices: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Map painting types: oil=0, watercolor=1

# Define constraints for each option
opt_a_constr = And(
    w1_l_student == 0, w1_l_type == 0,  # Franz's oil
    w2_l_student == 0, w2_l_type == 1,  # Franz's watercolor
    w3_l_student == 1, w3_l_type == 0,  # Greene's oil
    w4_l_student == 3, w4_l_type == 0   # Isaacs's oil (already constrained)
)

opt_b_constr = And(
    w1_l_student == 0, w1_l_type == 0,  # Franz's oil
    w2_l_student == 2, w2_l_type == 1,  # Hidalgo's watercolor
    w3_l_student == 3, w3_l_type == 1,  # Isaacs's watercolor
    w4_l_student == 3, w4_l_type == 0   # Isaacs's oil
)

opt_c_constr = And(
    w1_l_student == 1, w1_l_type == 0,  # Greene's oil
    w2_l_student == 0, w2_l_type == 0,  # Franz's oil
    w3_l_student == 3, w3_l_type == 0,  # Isaacs's oil
    w4_l_student == 2, w4_l_type == 0   # Hidalgo's oil
)

opt_d_constr = And(
    w1_l_student == 2, w1_l_type == 0,  # Hidalgo's oil
    w2_l_student == 1, w2_l_type == 0,  # Greene's oil
    w3_l_student == 1, w3_l_type == 1,  # Greene's watercolor
    w4_l_student == 3, w4_l_type == 0   # Isaacs's oil
)

opt_e_constr = And(
    w1_l_student == 2, w1_l_type == 1,  # Hidalgo's watercolor
    w2_l_student == 0, w2_l_type == 0,  # Franz's oil
    w3_l_student == 1, w3_l_type == 0,  # Greene's oil
    w4_l_student == 3, w4_l_type == 0   # Isaacs's oil
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")