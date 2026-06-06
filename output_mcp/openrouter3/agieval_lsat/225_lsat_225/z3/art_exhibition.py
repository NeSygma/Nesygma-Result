from z3 import *

solver = Solver()

# Define students and painting types
students = ["F", "G", "H", "I"]  # Franz, Greene, Hidalgo, Isaacs
types = ["O", "W"]  # Oil, Watercolor

# Walls and positions
walls = [1, 2, 3, 4]
positions = ["U", "L"]  # Upper, Lower

# Create variables: wall and position for each painting
# We'll use dictionaries for easy access
wall = {}
pos = {}

for s in students:
    for t in types:
        wall[(s, t)] = Int(f"wall_{s}_{t}")
        pos[(s, t)] = Int(f"pos_{s}_{t}")
        
        # Domain constraints: wall between 1-4, position 0=U, 1=L
        solver.add(wall[(s, t)] >= 1, wall[(s, t)] <= 4)
        solver.add(pos[(s, t)] >= 0, pos[(s, t)] <= 1)

# Constraint 1: No wall has only watercolors
# For each wall, at least one oil painting must be present
for w in walls:
    # Count oils on wall w
    oils_on_wall = [If(wall[(s, "O")] == w, 1, 0) for s in students]
    solver.add(Sum(oils_on_wall) >= 1)

# Constraint 2: No wall has work of only one student
# For each wall, at least 2 different students must have paintings
for w in walls:
    # Count distinct students on wall w
    students_on_wall = []
    for s in students:
        # Student s has a painting on wall w if either oil or watercolor is on wall w
        has_painting = Or(wall[(s, "O")] == w, wall[(s, "W")] == w)
        students_on_wall.append(If(has_painting, 1, 0))
    solver.add(Sum(students_on_wall) >= 2)

# Constraint 3: No wall has both Franz and Isaacs paintings
for w in walls:
    # Franz has painting on wall w
    franz_on_w = Or(wall[("F", "O")] == w, wall[("F", "W")] == w)
    # Isaacs has painting on wall w
    isaacs_on_w = Or(wall[("I", "O")] == w, wall[("I", "W")] == w)
    # They cannot both be on the same wall
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 4: Greene's watercolor is in upper position of the wall where Franz's oil is displayed
# First, find the wall where Franz's oil is
franz_oil_wall = wall[("F", "O")]
# Greene's watercolor must be on that same wall
solver.add(wall[("G", "W")] == franz_oil_wall)
# And Greene's watercolor must be in upper position (position 0)
solver.add(pos[("G", "W")] == 0)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(wall[("I", "O")] == 4)
solver.add(pos[("I", "O")] == 1)  # Lower position is 1

# Additional constraint: Each painting must be on a unique wall-position combination
# Actually, the problem says "exactly two paintings will be displayed on each wall"
# So each wall has exactly 2 paintings (one upper, one lower)
# We need to ensure that for each wall, there are exactly 2 paintings (one in each position)
for w in walls:
    # Count paintings on wall w
    paintings_on_wall = []
    for s in students:
        for t in types:
            paintings_on_wall.append(If(wall[(s, t)] == w, 1, 0))
    solver.add(Sum(paintings_on_wall) == 2)
    
    # Also ensure one upper and one lower on each wall
    upper_on_wall = []
    lower_on_wall = []
    for s in students:
        for t in types:
            upper_on_wall.append(If(And(wall[(s, t)] == w, pos[(s, t)] == 0), 1, 0))
            lower_on_wall.append(If(And(wall[(s, t)] == w, pos[(s, t)] == 1), 1, 0))
    solver.add(Sum(upper_on_wall) == 1)
    solver.add(Sum(lower_on_wall) == 1)

# Now test each answer choice
# Answer choices are about what CANNOT be true
# So we need to test if each statement can be true (satisfiable)
# The one that CANNOT be true is the one that is unsatisfiable when added

# Define the options as constraints
opt_a = wall[("F", "W")] == wall[("G", "O")]  # Franz's watercolor on same wall as Greene's oil
opt_b = wall[("F", "W")] == wall[("H", "O")]  # Franz's watercolor on same wall as Hidalgo's oil
opt_c = pos[("G", "O")] == 0  # Greene's oil in upper position
opt_d = pos[("H", "W")] == 1  # Hidalgo's watercolor in lower position
opt_e = wall[("I", "W")] == wall[("H", "O")]  # Isaacs's watercolor on same wall as Hidalgo's oil

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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