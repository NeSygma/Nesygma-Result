from z3 import *

solver = Solver()

# Declare variables: each painting has a position (0..7)
pos_F_o = Int('pos_F_o')
pos_F_w = Int('pos_F_w')
pos_G_o = Int('pos_G_o')
pos_G_w = Int('pos_G_w')
pos_H_o = Int('pos_H_o')
pos_H_w = Int('pos_H_w')
pos_I_o = Int('pos_I_o')
pos_I_w = Int('pos_I_w')

# Base constraints
# 1. Positions between 0 and 7
solver.add(And(pos_F_o >= 0, pos_F_o <= 7))
solver.add(And(pos_F_w >= 0, pos_F_w <= 7))
solver.add(And(pos_G_o >= 0, pos_G_o <= 7))
solver.add(And(pos_G_w >= 0, pos_G_w <= 7))
solver.add(And(pos_H_o >= 0, pos_H_o <= 7))
solver.add(And(pos_H_w >= 0, pos_H_w <= 7))
solver.add(And(pos_I_o >= 0, pos_I_o <= 7))
solver.add(And(pos_I_w >= 0, pos_I_w <= 7))

# 2. All distinct
solver.add(Distinct([pos_F_o, pos_F_w, pos_G_o, pos_G_w, pos_H_o, pos_H_w, pos_I_o, pos_I_w]))

# 3. Each wall has exactly one oil and one watercolor
# Define walls: for w in 1..4, positions are 2*(w-1) and 2*(w-1)+1
for w in range(1,5):
    # Oils
    solver.add(Sum([If(Or(pos_F_o == 2*(w-1), pos_F_o == 2*(w-1)+1), 1, 0),
                    If(Or(pos_G_o == 2*(w-1), pos_G_o == 2*(w-1)+1), 1, 0),
                    If(Or(pos_H_o == 2*(w-1), pos_H_o == 2*(w-1)+1), 1, 0),
                    If(Or(pos_I_o == 2*(w-1), pos_I_o == 2*(w-1)+1), 1, 0)]) == 1)
    # Watercolors
    solver.add(Sum([If(Or(pos_F_w == 2*(w-1), pos_F_w == 2*(w-1)+1), 1, 0),
                    If(Or(pos_G_w == 2*(w-1), pos_G_w == 2*(w-1)+1), 1, 0),
                    If(Or(pos_H_w == 2*(w-1), pos_H_w == 2*(w-1)+1), 1, 0),
                    If(Or(pos_I_w == 2*(w-1), pos_I_w == 2*(w-1)+1), 1, 0)]) == 1)

# 4. Each student's oil and watercolor on different walls
# Compute wall for each painting using integer division
def wall_expr(pos):
    # pos is an integer expression, return wall number (1..4)
    return pos / 2 + 1  # This is real division, but pos is integer, so pos/2 may be fractional.
    # Actually, we need integer division. Use Div.
    # return Div(pos, 2) + 1

# Let's use Div
def wall_expr(pos):
    return Div(pos, 2) + 1

solver.add(wall_expr(pos_F_o) != wall_expr(pos_F_w))
solver.add(wall_expr(pos_G_o) != wall_expr(pos_G_w))
solver.add(wall_expr(pos_H_o) != wall_expr(pos_H_w))
solver.add(wall_expr(pos_I_o) != wall_expr(pos_I_w))

# 5. No wall has both Franz and Isaacs
for w in range(1,5):
    # Count paintings by Franz or Isaacs on wall w
    count = 0
    # Franz's oil
    count += If(Or(pos_F_o == 2*(w-1), pos_F_o == 2*(w-1)+1), 1, 0)
    # Franz's watercolor
    count += If(Or(pos_F_w == 2*(w-1), pos_F_w == 2*(w-1)+1), 1, 0)
    # Isaacs's oil
    count += If(Or(pos_I_o == 2*(w-1), pos_I_o == 2*(w-1)+1), 1, 0)
    # Isaacs's watercolor
    count += If(Or(pos_I_w == 2*(w-1), pos_I_w == 2*(w-1)+1), 1, 0)
    solver.add(count <= 1)

# 6. Greene's watercolor is in upper position of the wall where Franz's oil is displayed
w_f = wall_expr(pos_F_o)
solver.add(wall_expr(pos_G_w) == w_f)
solver.add(pos_G_w % 2 == 0)

# 7. Isaacs's oil is in lower position of wall 4
solver.add(wall_expr(pos_I_o) == 4)
solver.add(pos_I_o % 2 == 1)

# 8. No wall has the work of only one student
# For each wall, the oil and watercolor must be by different students
for w in range(1,5):
    # Determine which student's oil is on wall w
    oil_student = None
    watercolor_student = None
    # We'll create a variable for each student's oil on wall w
    # Instead, we can use a big OR constraint: the oil student and watercolor student are different.
    # Let's define a function that returns the student for a given painting position.
    # Since we have separate variables, we can check which painting is on wall w.
    # For oil: check which of the four oils is on wall w.
    # For watercolor: check which of the four watercolors is on wall w.
    # Then assert that the oil student and watercolor student are different.
    # We can do this by enumerating all possibilities.
    # Let's create a list of oil positions and corresponding student names.
    oil_positions = [(pos_F_o, 'F'), (pos_G_o, 'G'), (pos_H_o, 'H'), (pos_I_o, 'I')]
    water_positions = [(pos_F_w, 'F'), (pos_G_w, 'G'), (pos_H_w, 'H'), (pos_I_w, 'I')]
    
    # For each oil student, if that oil is on wall w, then the watercolor student must be different.
    # We'll use a constraint that for each oil student, if that oil is on wall w, then the watercolor on wall w is not that student.
    for (oil_pos, oil_stud) in oil_positions:
        # Check if this oil is on wall w
        oil_on_w = Or(oil_pos == 2*(w-1), oil_pos == 2*(w-1)+1)
        # For each watercolor student, if that watercolor is on wall w, then oil student != watercolor student
        for (water_pos, water_stud) in water_positions:
            water_on_w = Or(water_pos == 2*(w-1), water_pos == 2*(w-1)+1)
            # If both are on wall w, then they must be different students
            solver.add(Implies(And(oil_on_w, water_on_w), oil_stud != water_stud))

# Now evaluate answer choices
# Define answer choices as constraints
opt_a = (wall_expr(pos_F_w) == wall_expr(pos_G_o))
opt_b = (wall_expr(pos_F_w) == wall_expr(pos_H_o))
opt_c = (pos_G_o % 2 == 0)
opt_d = (pos_H_w % 2 == 1)
opt_e = (wall_expr(pos_I_w) == wall_expr(pos_H_o))

# Evaluate each option: we want to find which CANNOT be true, i.e., which option leads to unsat when added to the base constraints.
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

BENCHMARK_MODE = True
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")