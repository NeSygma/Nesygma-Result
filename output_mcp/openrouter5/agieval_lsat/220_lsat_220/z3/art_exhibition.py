from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# Positions: Upper (U), Lower (L)
positions = ['U', 'L']

# Each student has exactly two paintings: an oil and a watercolor.
# We'll model each painting as a pair (wall, position).
# For each student s and medium m (oil or watercolor), we have variables:
# wall_s_m = which wall (1-4)
# pos_s_m = which position (0 for upper, 1 for lower)

# Let's use integer variables for walls (1-4) and positions (0=upper, 1=lower)

# For each student and medium, wall and position
wall = {}
pos = {}
for s in students:
    for m in ['oil', 'water']:
        wall[(s, m)] = Int(f'wall_{s}_{m}')
        pos[(s, m)] = Int(f'pos_{s}_{m}')
        solver.add(wall[(s, m)] >= 1, wall[(s, m)] <= 4)
        solver.add(pos[(s, m)] >= 0, pos[(s, m)] <= 1)

# Exactly two paintings on each wall, one upper (0) and one lower (1)
# For each wall w, exactly one painting (student+medium) has pos=0 and exactly one has pos=1
for w in walls:
    # Count paintings on wall w with upper position
    upper_count = Sum([If(And(wall[(s, m)] == w, pos[(s, m)] == 0), 1, 0) for s in students for m in ['oil', 'water']])
    lower_count = Sum([If(And(wall[(s, m)] == w, pos[(s, m)] == 1), 1, 0) for s in students for m in ['oil', 'water']])
    solver.add(upper_count == 1)
    solver.add(lower_count == 1)

# Each student displays exactly one oil and one watercolor (already have one each)
# No wall has only watercolors displayed on it.
# i.e., on each wall, at least one painting is an oil
for w in walls:
    oil_on_wall = Sum([If(And(wall[(s, 'oil')] == w), 1, 0) for s in students])
    solver.add(oil_on_wall >= 1)

# No wall has the work of only one student displayed on it.
# i.e., on each wall, the two paintings are by different students
for w in walls:
    # For each pair of distinct students, they can't both be on wall w... 
    # Actually: the two paintings on wall w must be by two different students.
    # So for each wall, count distinct students. At least 2.
    # We can encode: for each wall, there exist at least two different students with paintings there.
    # Simpler: For each wall, not (all paintings on that wall are by the same student)
    for s in students:
        # It's not the case that student s has both paintings on wall w
        # Actually "only one student" means both paintings are by the same student.
        # So for each wall w and each student s, we cannot have both of s's paintings on w.
        solver.add(Not(And(wall[(s, 'oil')] == w, wall[(s, 'water')] == w)))

# No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in walls:
    franz_on_w = Or([And(wall[('F', m)] == w) for m in ['oil', 'water']])
    isaacs_on_w = Or([And(wall[('I', m)] == w) for m in ['oil', 'water']])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# So: wall(G, water) = wall(F, oil) AND pos(G, water) = 0 (upper)
solver.add(wall[('G', 'water')] == wall[('F', 'oil')])
solver.add(pos[('G', 'water')] == 0)

# Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[('I', 'oil')] == 4)
solver.add(pos[('I', 'oil')] == 1)

# Additional given conditions:
# Isaacs's watercolor is displayed on wall 2
solver.add(wall[('I', 'water')] == 2)

# Franz's oil is displayed on wall 3
solver.add(wall[('F', 'oil')] == 3)

# Now evaluate each option for what must be displayed on wall 1.
# Each option says a specific painting is on wall 1.
# We need to find which one MUST be true (i.e., is entailed by the constraints).
# So we check: if we add the negation of the option, is it unsatisfiable?
# If so, the option must be true.

# Option A: Franz's watercolor on wall 1
opt_a = And(wall[('F', 'water')] == 1)

# Option B: Greene's oil on wall 1
opt_b = And(wall[('G', 'oil')] == 1)

# Option C: Greene's watercolor on wall 1
opt_c = And(wall[('G', 'water')] == 1)

# Option D: Hidalgo's oil on wall 1
opt_d = And(wall[('H', 'oil')] == 1)

# Option E: Hidalgo's watercolor on wall 1
opt_e = And(wall[('H', 'water')] == 1)

# For "must be true", we check if the negation is unsatisfiable.
# If negating the option leads to unsat, then the option must hold.
# Let's check each option by testing if it's forced.

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # To test if constr MUST be true, we check if the system without constr can still be sat
    # Actually, we need to check if constr is entailed.
    # We add NOT(constr) and see if unsat. If unsat, then constr must be true.
    solver.add(Not(constr))
    if solver.check() == unsat:
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