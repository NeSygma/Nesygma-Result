from z3 import *

# Students: 0=Franz, 1=Greene, 2=Hidalgo, 3=Isaacs
# Mediums: 0=oil, 1=watercolor

wall = [[Int(f"wall_{s}_{m}") for m in range(2)] for s in range(4)]
pos = [[Int(f"pos_{s}_{m}") for m in range(2)] for s in range(4)]

solver = Solver()

# Domains
for s in range(4):
    for m in range(2):
        solver.add(wall[s][m] >= 1, wall[s][m] <= 4)
        solver.add(pos[s][m] >= 0, pos[s][m] <= 1)

# Each wall has exactly 2 paintings (one upper, one lower)
for w in range(1, 5):
    # Exactly 2 paintings on this wall
    solver.add(Sum([If(wall[s][m] == w, 1, 0) for s in range(4) for m in range(2)]) == 2)
    # Exactly 1 upper on this wall
    solver.add(Sum([If(And(wall[s][m] == w, pos[s][m] == 0), 1, 0) for s in range(4) for m in range(2)]) == 1)
    # Exactly 1 lower on this wall
    solver.add(Sum([If(And(wall[s][m] == w, pos[s][m] == 1), 1, 0) for s in range(4) for m in range(2)]) == 1)

# No wall has only watercolors -> each wall has at least one oil
for w in range(1, 5):
    solver.add(Sum([If(wall[s][0] == w, 1, 0) for s in range(4)]) >= 1)

# No wall has the work of only one student -> each wall has 2 different students
for w in range(1, 5):
    solver.add(Sum([If(Or(wall[s][0] == w, wall[s][1] == w), 1, 0) for s in range(4)]) >= 2)

# No wall has both Franz and Isaacs
for w in range(1, 5):
    solver.add(Not(And(Or(wall[0][0] == w, wall[0][1] == w), Or(wall[3][0] == w, wall[3][1] == w))))

# Greene's watercolor is in the upper position of the wall on which Franz's oil is displayed
solver.add(wall[1][1] == wall[0][0])  # same wall
solver.add(pos[1][1] == 0)  # upper position

# Isaacs's oil is displayed in the lower position of wall 4
solver.add(wall[3][0] == 4)
solver.add(pos[3][0] == 1)

# Define the options
# Option A: Both Franz's and both Greene's paintings in lower positions (pos=1)
opt_a = And(pos[0][0] == 1, pos[0][1] == 1, pos[1][0] == 1, pos[1][1] == 1)

# Option B: Both Franz's and both Greene's paintings in upper positions (pos=0)
opt_b = And(pos[0][0] == 0, pos[0][1] == 0, pos[1][0] == 0, pos[1][1] == 0)

# Option C: Both Franz's and both Hidalgo's paintings in upper positions
opt_c = And(pos[0][0] == 0, pos[0][1] == 0, pos[2][0] == 0, pos[2][1] == 0)

# Option D: Both Greene's and both Hidalgo's paintings in lower positions
opt_d = And(pos[1][0] == 1, pos[1][1] == 1, pos[2][0] == 1, pos[2][1] == 1)

# Option E: Both Greene's and both Hidalgo's paintings in upper positions
opt_e = And(pos[1][0] == 0, pos[1][1] == 0, pos[2][0] == 0, pos[2][1] == 0)

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