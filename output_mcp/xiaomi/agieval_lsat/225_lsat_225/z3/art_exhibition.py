from z3 import *

solver = Solver()

# Students: Franz=0, Greene=1, Hidalgo=2, Isaacs=3
# Types: Oil=0, Watercolor=1
# Walls: 1,2,3,4
# Positions: Upper=0, Lower=1

# For each painting, we assign a wall and a position
# paintings[student][type] = wall (1-4)
# positions[student][type] = 0 (upper) or 1 (lower)

paintings = [[Int(f"paint_{s}_{t}") for t in range(2)] for s in range(4)]
positions = [[Int(f"pos_{s}_{t}") for t in range(2)] for s in range(4)]

# Domain constraints
for s in range(4):
    for t in range(2):
        solver.add(paintings[s][t] >= 1, paintings[s][t] <= 4)
        solver.add(Or(positions[s][t] == 0, positions[s][t] == 1))

# Each wall has exactly 2 paintings (one upper, one lower)
# Count paintings per wall
for w in range(1, 5):
    # Exactly 2 paintings on wall w
    solver.add(Sum([If(paintings[s][t] == w, 1, 0) for s in range(4) for t in range(2)]) == 2)
    # Exactly 1 upper and 1 lower on wall w
    solver.add(Sum([If(And(paintings[s][t] == w, positions[s][t] == 0), 1, 0) for s in range(4) for t in range(2)]) == 1)
    solver.add(Sum([If(And(paintings[s][t] == w, positions[s][t] == 1), 1, 0) for s in range(4) for t in range(2)]) == 1)

# All paintings on different wall-position combinations
all_assignments = []
for s in range(4):
    for t in range(2):
        all_assignments.append((paintings[s][t], positions[s][t]))
for i in range(len(all_assignments)):
    for j in range(i+1, len(all_assignments)):
        solver.add(Or(all_assignments[i][0] != all_assignments[j][0],
                      all_assignments[i][1] != all_assignments[j][1]))

# Constraint 1: No wall has only watercolors
# Each wall must have at least one oil painting
for w in range(1, 5):
    solver.add(Or([And(paintings[s][0] == w) for s in range(4)]))

# Constraint 2: No wall has work of only one student
# Each wall must have paintings from 2 different students
for w in range(1, 5):
    # For each wall, the two paintings must be from different students
    # The two paintings on wall w are from students s1 and s2 where s1 != s2
    # We need: for any pair of paintings on the same wall, they must be from different students
    for s in range(4):
        # Student s can have at most 1 painting on wall w
        solver.add(Sum([If(paintings[s][t] == w, 1, 0) for t in range(2)]) <= 1)

# Constraint 3: No wall has both Franz (0) and Isaacs (3)
for w in range(1, 5):
    solver.add(Not(And(
        Or(paintings[0][0] == w, paintings[0][1] == w),
        Or(paintings[3][0] == w, paintings[3][1] == w)
    )))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is
# Franz's oil is paintings[0][0], Greene's watercolor is paintings[1][1]
solver.add(paintings[1][1] == paintings[0][0])
solver.add(positions[1][1] == 0)  # upper

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(paintings[3][0] == 4)
solver.add(positions[3][0] == 1)  # lower

# Now test each option
# (A) Franz's watercolor on same wall as Greene's oil
opt_a = (paintings[0][1] == paintings[1][0])

# (B) Franz's watercolor on same wall as Hidalgo's oil
opt_b = (paintings[0][1] == paintings[2][0])

# (C) Greene's oil is displayed in an upper position
opt_c = (positions[1][0] == 0)

# (D) Hidalgo's watercolor is displayed in a lower position
opt_d = (positions[2][1] == 1)

# (E) Isaacs's watercolor on same wall as Hidalgo's oil
opt_e = (paintings[3][1] == paintings[2][0])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for s in range(4):
            for t in range(2):
                stype = "Oil" if t == 0 else "Watercolor"
                sname = ["Franz", "Greene", "Hidalgo", "Isaacs"][s]
                w = m[paintings[s][t]].as_long()
                p = "Upper" if m[positions[s][t]].as_long() == 0 else "Lower"
                print(f"  {sname}'s {stype}: Wall {w}, {p}")
    else:
        print(f"Option {letter} is UNSAT (CANNOT be true)")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")