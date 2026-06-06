from z3 import *

# Create solver
solver = Solver()

# Define paintings: 0-7 as before
paintings = list(range(8))

# For each painting, we need wall (1-4) and position (U/L)
wall = [Int(f"wall_{p}") for p in paintings]
pos = [Int(f"pos_{p}") for p in paintings]  # 0=upper, 1=lower

# Base constraints: walls 1-4, positions 0-1
for p in paintings:
    solver.add(wall[p] >= 1)
    solver.add(wall[p] <= 4)
    solver.add(pos[p] >= 0)
    solver.add(pos[p] <= 1)

# Each wall has exactly 2 paintings (one upper, one lower)
# For each wall w and position p, exactly one painting
for w in range(1, 5):
    for p in range(2):
        # Count paintings on wall w at position p
        count = Sum([If(And(wall[i] == w, pos[i] == p), 1, 0) for i in paintings])
        solver.add(count == 1)

# Precomputed data
students = [0, 0, 1, 1, 2, 2, 3, 3]  # Franz=0, Greene=1, Hidalgo=2, Isaacs=3
is_wc = [False, True, False, True, False, True, False, True]  # watercolor flags

# Constraint 1: No wall has only watercolors
# For each wall, at least one oil painting
for w in range(1, 5):
    has_oil = Or([And(wall[i] == w, Not(is_wc[i])) for i in paintings])
    solver.add(has_oil)

# Constraint 2: No wall has work of only one student
# For each wall, at least two different students
for w in range(1, 5):
    # Get students on this wall
    students_on_wall = [students[i] for i in paintings if i in paintings]  # all students
    # Actually, we need to ensure at least two different students
    # We'll use a different approach: for each pair of paintings on same wall, they must be different students
    pass  # We'll handle this in the pairwise constraints below

# Constraint 3: No wall has both Franz and Isaacs
# Constraint 4: Greene's watercolor is upper on wall where Franz's oil is displayed
# Constraint 5: Isaacs's oil is lower on wall 4

# Let's add pairwise constraints
for p1 in paintings:
    for p2 in paintings:
        if p1 >= p2:
            continue
        same_wall = (wall[p1] == wall[p2])
        
        # Constraint 2: different students on same wall
        if students[p1] == students[p2]:
            solver.add(Not(same_wall))
        
        # Constraint 3: no Franz + Isaacs on same wall
        if (students[p1] == 0 and students[p2] == 3) or (students[p1] == 3 and students[p2] == 0):
            solver.add(Not(same_wall))

# Constraint 4: Greene's watercolor (3) is upper on wall where Franz's oil (0) is displayed
solver.add(wall[0] == wall[3])  # same wall
solver.add(pos[3] == 0)  # Greene's watercolor is upper

# Constraint 5: Isaacs's oil (6) is lower on wall 4
solver.add(wall[6] == 4)
solver.add(pos[6] == 1)

# Now evaluate answer choices
options = []

# Option A: Both Franz's and both Greene's in lower positions
opt_a = And(
    pos[0] == 1,  # Franz oil lower
    pos[1] == 1,  # Franz watercolor lower
    pos[2] == 1,  # Greene oil lower
    pos[3] == 1   # Greene watercolor lower
)
options.append(("A", opt_a))

# Option B: Both Franz's and both Greene's in upper positions
opt_b = And(
    pos[0] == 0,
    pos[1] == 0,
    pos[2] == 0,
    pos[3] == 0
)
options.append(("B", opt_b))

# Option C: Both Franz's and both Hidalgo's in upper positions
opt_c = And(
    pos[0] == 0,
    pos[1] == 0,
    pos[4] == 0,
    pos[5] == 0
)
options.append(("C", opt_c))

# Option D: Both Greene's and both Hidalgo's in lower positions
opt_d = And(
    pos[2] == 1,
    pos[3] == 1,
    pos[4] == 1,
    pos[5] == 1
)
options.append(("D", opt_d))

# Option E: Both Greene's and both Hidalgo's in upper positions
opt_e = And(
    pos[2] == 0,
    pos[3] == 0,
    pos[4] == 0,
    pos[5] == 0
)
options.append(("E", opt_e))

# Test each option using the required skeleton
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")