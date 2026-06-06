from z3 import *

solver = Solver()

# Students: Franz(0), Greene(1), Hidalgo(2), Isaacs(3)
# Types: Oil(0), Watercolor(1)
# Walls: 1,2,3,4
# Position: Upper(1), Lower(0)

# Paintings: (student, type)
# FO=(0,0), FW=(0,1), GO=(1,0), GW=(1,1), HO=(2,0), HW=(2,1), IO=(3,0), IW=(3,1)
paintings = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)]
names = {0: 'Franz', 1: 'Greene', 2: 'Hidalgo', 3: 'Isaacs'}
types = {0: 'Oil', 1: 'Watercolor'}

# wall[p] = which wall (1-4), pos[p] = upper(1) or lower(0)
wall = {p: Int(f'wall_{names[p[0]]}_{types[p[1]]}') for p in paintings}
position = {p: Int(f'pos_{names[p[0]]}_{types[p[1]]}') for p in paintings}

# Each painting on a wall 1-4
for p in paintings:
    solver.add(wall[p] >= 1, wall[p] <= 4)
    solver.add(Or(position[p] == 0, position[p] == 1))

# Each wall has exactly 2 paintings, one upper and one lower
for w in range(1, 5):
    # Exactly 2 paintings on wall w
    solver.add(Sum([If(wall[p] == w, 1, 0) for p in paintings]) == 2)
    # Exactly 1 upper on wall w
    solver.add(Sum([If(And(wall[p] == w, position[p] == 1), 1, 0) for p in paintings]) == 1)
    # Exactly 1 lower on wall w
    solver.add(Sum([If(And(wall[p] == w, position[p] == 0), 1, 0) for p in paintings]) == 1)

# Each painting on a unique position (all 8 positions filled by distinct paintings)
# Since 8 paintings and 8 positions, and each wall has exactly 2, this is automatic
# if we ensure no two paintings share the same (wall, position)
for i in range(len(paintings)):
    for j in range(i+1, len(paintings)):
        pi, pj = paintings[i], paintings[j]
        solver.add(Not(And(wall[pi] == wall[pj], position[pi] == position[pj])))

# Constraint 1: No wall has only watercolors (each wall has at least one oil)
for w in range(1, 5):
    solver.add(Or([And(wall[p] == w, p[1] == 0) for p in paintings]))

# Constraint 2: No wall has work of only one student (each wall has paintings from >= 2 students)
for w in range(1, 5):
    for s in range(4):
        # Not both paintings on wall w are by student s
        paintings_by_s = [p for p in paintings if p[0] == s]
        solver.add(Not(And(
            Sum([If(And(wall[p] == w, p[0] == s), 1, 0) for p in paintings]) == 2
        )))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    franz_on_w = Or([wall[p] == w for p in paintings if p[0] == 0])
    isaacs_on_w = Or([wall[p] == w for p in paintings if p[0] == 3])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 4: Greene's watercolor is upper on the same wall as Franz's oil
GW = (1, 1)
FO = (0, 0)
solver.add(wall[GW] == wall[FO])
solver.add(position[GW] == 1)
# FO must be lower since GW is upper on same wall
solver.add(position[FO] == 0)

# Constraint 5: Isaacs's oil is lower on wall 4
IO = (3, 0)
solver.add(wall[IO] == 4)
solver.add(position[IO] == 0)

# Now check each answer choice
# (A) Franz's watercolor on same wall as Greene's oil
FW = (0, 1)
GO = (1, 0)
opt_a = (wall[FW] == wall[GO])

# (B) Franz's watercolor on same wall as Hidalgo's oil
HO = (2, 0)
opt_b = (wall[FW] == wall[HO])

# (C) Greene's oil is in upper position
opt_c = (position[GO] == 1)

# (D) Hidalgo's watercolor is in lower position
HW = (2, 1)
opt_d = (position[HW] == 0)

# (E) Isaacs's watercolor on same wall as Hidalgo's oil
IW = (3, 1)
opt_e = (wall[IW] == wall[HO])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for p in paintings:
            pname = f"{names[p[0]]}_{types[p[1]]}"
            print(f"  {pname}: wall={m[wall[p]]}, pos={'upper' if m[position[p]] == 1 else 'lower'}")
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