from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
# Positions: Upper (U), Lower (L)
# Each student has exactly two paintings: an oil and a watercolor.
# We need to assign each painting to a wall and position.

# Let's model each painting as a variable:
# For each student s and type t (0=oil, 1=watercolor), we have:
#   wall[s][t] = wall number (1-4)
#   pos[s][t] = position (0=upper, 1=lower)

wall = {s: [Int(f'wall_{s}_oil'), Int(f'wall_{s}_water')] for s in students}
pos = {s: [Int(f'pos_{s}_oil'), Int(f'pos_{s}_water')] for s in students}

# Domain constraints
for s in students:
    for i in range(2):
        solver.add(wall[s][i] >= 1, wall[s][i] <= 4)
        solver.add(pos[s][i] >= 0, pos[s][i] <= 1)  # 0=upper, 1=lower

# Exactly two paintings on each wall (one upper, one lower)
# So each wall has exactly 2 paintings total.
# Count paintings per wall
for w in range(1, 5):
    count_wall = Sum([If(wall[s][i] == w, 1, 0) for s in students for i in range(2)])
    solver.add(count_wall == 2)

# Each wall has exactly one upper and one lower position
for w in range(1, 5):
    count_upper = Sum([If(And(wall[s][i] == w, pos[s][i] == 0), 1, 0) for s in students for i in range(2)])
    count_lower = Sum([If(And(wall[s][i] == w, pos[s][i] == 1), 1, 0) for s in students for i in range(2)])
    solver.add(count_upper == 1)
    solver.add(count_lower == 1)

# Condition 1: No wall has only watercolors displayed on it.
# i.e., on each wall, at least one painting is an oil.
for w in range(1, 5):
    has_oil = Or([And(wall[s][0] == w) for s in students])
    solver.add(has_oil)

# Condition 2: No wall has the work of only one student displayed on it.
# i.e., on each wall, at least two different students have paintings.
for w in range(1, 5):
    # At least two distinct students on wall w
    student_pairs = []
    for s1 in students:
        for s2 in students:
            if s1 < s2:
                # Both s1 and s2 have at least one painting on wall w
                s1_on_w = Or([wall[s1][i] == w for i in range(2)])
                s2_on_w = Or([wall[s2][i] == w for i in range(2)])
                student_pairs.append(And(s1_on_w, s2_on_w))
    solver.add(Or(student_pairs))

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in range(1, 5):
    franz_on_w = Or([wall['F'][i] == w for i in range(2)])
    isaacs_on_w = Or([wall['I'][i] == w for i in range(2)])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# So: wall_G_water == wall_F_oil, and pos_G_water == 0 (upper)
solver.add(wall['G'][1] == wall['F'][0])
solver.add(pos['G'][1] == 0)

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall['I'][0] == 4)
solver.add(pos['I'][0] == 1)

# Now evaluate each option

# Option A: Both of Franz's paintings and both of Greene's paintings are displayed in lower positions.
opt_a_constr = And(
    pos['F'][0] == 1, pos['F'][1] == 1,  # Franz's oil and watercolor both lower
    pos['G'][0] == 1, pos['G'][1] == 1   # Greene's oil and watercolor both lower
)

# Option B: Both of Franz's paintings and both of Greene's paintings are displayed in upper positions.
opt_b_constr = And(
    pos['F'][0] == 0, pos['F'][1] == 0,  # Franz's oil and watercolor both upper
    pos['G'][0] == 0, pos['G'][1] == 0   # Greene's oil and watercolor both upper
)

# Option C: Both of Franz's paintings and both of Hidalgo's paintings are displayed in upper positions.
opt_c_constr = And(
    pos['F'][0] == 0, pos['F'][1] == 0,  # Franz's oil and watercolor both upper
    pos['H'][0] == 0, pos['H'][1] == 0   # Hidalgo's oil and watercolor both upper
)

# Option D: Both of Greene's paintings and both of Hidalgo's paintings are displayed in lower positions.
opt_d_constr = And(
    pos['G'][0] == 1, pos['G'][1] == 1,  # Greene's oil and watercolor both lower
    pos['H'][0] == 1, pos['H'][1] == 1   # Hidalgo's oil and watercolor both lower
)

# Option E: Both of Greene's paintings and both of Hidalgo's paintings are displayed in upper positions.
opt_e_constr = And(
    pos['G'][0] == 0, pos['G'][1] == 0,  # Greene's oil and watercolor both upper
    pos['H'][0] == 0, pos['H'][1] == 0   # Hidalgo's oil and watercolor both upper
)

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