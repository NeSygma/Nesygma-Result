from z3 import *

solver = Solver()

# Students: 0=Franz, 1=Greene, 2=Hidalgo, 3=Isaacs
# Media: 0=oil, 1=watercolor
# Walls: 1,2,3,4
# Positions: 0=lower, 1=upper

# Declare wall and position for each student's oil and watercolor
wall = [[Int(f"wall_{s}_{m}") for m in range(2)] for s in range(4)]
pos = [[Int(f"pos_{s}_{m}") for m in range(2)] for s in range(4)]

# Domain constraints: walls 1-4, positions 0-1
for s in range(4):
    for m in range(2):
        solver.add(wall[s][m] >= 1, wall[s][m] <= 4)
        solver.add(pos[s][m] >= 0, pos[s][m] <= 1)

# Constraint 2: No wall has only watercolors displayed on it.
# Each wall must have at least one oil painting.
for w in range(1, 5):
    # Count oils on wall w
    oils_on_wall = Sum([If(wall[s][0] == w, 1, 0) for s in range(4)])
    solver.add(oils_on_wall >= 1)

# Constraint 3: No wall has the work of only one student displayed on it.
# Since each wall has exactly 2 paintings (one upper, one lower),
# they must be by two different students.
# Equivalent: a student's two paintings cannot be on the same wall.
for s in range(4):
    solver.add(wall[s][0] != wall[s][1])

# Constraint 4: No wall has both a painting by Franz and a painting by Isaacs.
for w in range(1, 5):
    franz_on_w = Or([wall[0][m] == w for m in range(2)])
    isaacs_on_w = Or([wall[3][m] == w for m in range(2)])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 5: Greene's watercolor is displayed in the upper position
# of the wall on which Franz's oil is displayed.
solver.add(pos[1][1] == 1)  # Greene's watercolor is upper
solver.add(wall[1][1] == wall[0][0])  # same wall as Franz's oil

# Constraint 6: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[3][0] == 4)
solver.add(pos[3][0] == 0)  # lower position

# Additional condition (Q): Greene's oil is displayed on the same wall as Franz's watercolor.
solver.add(wall[1][0] == wall[0][1])

# Also need: each wall has exactly one upper and one lower position.
# We have 4 walls, each with 2 paintings (upper and lower).
# So exactly 2 paintings per wall, one upper one lower.
# Let's enforce: For each wall w, exactly one painting in upper position and exactly one in lower position.
for w in range(1, 5):
    # Count upper positions on wall w
    upper_on_wall = Sum([If(And(wall[s][m] == w, pos[s][m] == 1), 1, 0) for s in range(4) for m in range(2)])
    solver.add(upper_on_wall == 1)
    lower_on_wall = Sum([If(And(wall[s][m] == w, pos[s][m] == 0), 1, 0) for s in range(4) for m in range(2)])
    solver.add(lower_on_wall == 1)

# Now evaluate each option for "must be true" by checking if its negation is inconsistent.

# Option A: Greene's oil is displayed in an upper position.
opt_a = (pos[1][0] == 1)

# Option B: Hidalgo's watercolor is displayed on the same wall as Isaacs's watercolor.
opt_b = (wall[2][1] == wall[3][1])

# Option C: Hidalgo's oil is displayed in an upper position.
opt_c = (pos[2][0] == 1)

# Option D: Hidalgo's oil is displayed on the same wall as Isaacs's watercolor.
opt_d = (wall[2][0] == wall[3][1])

# Option E: Isaacs's watercolor is displayed in a lower position.
opt_e = (pos[3][1] == 0)

found_options = []
for letter, neg_constr in [("A", Not(opt_a)), ("B", Not(opt_b)), ("C", Not(opt_c)), ("D", Not(opt_d)), ("E", Not(opt_e))]:
    solver.push()
    solver.add(neg_constr)
    if solver.check() == unsat:
        # The negation is inconsistent, so the option must be true
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