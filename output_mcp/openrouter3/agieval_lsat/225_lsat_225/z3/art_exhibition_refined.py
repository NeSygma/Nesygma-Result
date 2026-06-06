from z3 import *

solver = Solver()

# Define students and painting types
students = ["F", "G", "H", "I"]  # Franz, Greene, Hidalgo, Isaacs
types = ["O", "W"]  # Oil, Watercolor

# Walls and positions
walls = [1, 2, 3, 4]
positions = ["U", "L"]  # Upper, Lower

# Create variables: wall and position for each painting
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
for w in walls:
    oils_on_wall = [If(wall[(s, "O")] == w, 1, 0) for s in students]
    solver.add(Sum(oils_on_wall) >= 1)

# Constraint 2: No wall has work of only one student
for w in walls:
    students_on_wall = []
    for s in students:
        has_painting = Or(wall[(s, "O")] == w, wall[(s, "W")] == w)
        students_on_wall.append(If(has_painting, 1, 0))
    solver.add(Sum(students_on_wall) >= 2)

# Constraint 3: No wall has both Franz and Isaacs paintings
for w in walls:
    franz_on_w = Or(wall[("F", "O")] == w, wall[("F", "W")] == w)
    isaacs_on_w = Or(wall[("I", "O")] == w, wall[("I", "W")] == w)
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 4: Greene's watercolor is in upper position of the wall where Franz's oil is displayed
franz_oil_wall = wall[("F", "O")]
solver.add(wall[("G", "W")] == franz_oil_wall)
solver.add(pos[("G", "W")] == 0)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(wall[("I", "O")] == 4)
solver.add(pos[("I", "O")] == 1)

# Additional constraint: Each wall has exactly 2 paintings (one upper, one lower)
for w in walls:
    paintings_on_wall = []
    for s in students:
        for t in types:
            paintings_on_wall.append(If(wall[(s, t)] == w, 1, 0))
    solver.add(Sum(paintings_on_wall) == 2)
    
    upper_on_wall = []
    lower_on_wall = []
    for s in students:
        for t in types:
            upper_on_wall.append(If(And(wall[(s, t)] == w, pos[(s, t)] == 0), 1, 0))
            lower_on_wall.append(If(And(wall[(s, t)] == w, pos[(s, t)] == 1), 1, 0))
    solver.add(Sum(upper_on_wall) == 1)
    solver.add(Sum(lower_on_wall) == 1)

# Define the options as constraints
opt_a = wall[("F", "W")] == wall[("G", "O")]  # Franz's watercolor on same wall as Greene's oil
opt_b = wall[("F", "W")] == wall[("H", "O")]  # Franz's watercolor on same wall as Hidalgo's oil
opt_c = pos[("G", "O")] == 0  # Greene's oil in upper position
opt_d = pos[("H", "W")] == 1  # Hidalgo's watercolor in lower position
opt_e = wall[("I", "W")] == wall[("H", "O")]  # Isaacs's watercolor on same wall as Hidalgo's oil

# Test which option CANNOT be true (i.e., makes the problem unsatisfiable)
# We need to find which option leads to UNSAT when added to base constraints
found_unsat_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        found_unsat_options.append(letter)
    solver.pop()

# According to the problem, exactly one option CANNOT be true
if len(found_unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat_options[0]}")
elif len(found_unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {found_unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that cannot be true")