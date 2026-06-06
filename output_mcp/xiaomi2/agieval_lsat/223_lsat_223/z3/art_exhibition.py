from z3 import *

solver = Solver()

# Paintings indexed: F_O=0, F_W=1, G_O=2, G_W=3, H_O=4, H_W=5, I_O=6, I_W=7
# wall[i] ∈ {1,2,3,4}, pos[i] ∈ {0=upper, 1=lower}
wall = [Int(f'wall_{i}') for i in range(8)]
pos = [Int(f'pos_{i}') for i in range(8)]

# Types and students per painting index
painting_type = [0, 1, 0, 1, 0, 1, 0, 1]   # 0=oil, 1=watercolor
painting_student = [0, 0, 1, 1, 2, 2, 3, 3] # F=0, G=1, H=2, I=3

# Domain constraints
for i in range(8):
    solver.add(wall[i] >= 1, wall[i] <= 4)
    solver.add(pos[i] >= 0, pos[i] <= 1)

# Each wall has exactly 2 paintings: one upper, one lower
for w in range(1, 5):
    solver.add(Sum([If(wall[i] == w, 1, 0) for i in range(8)]) == 2)
    solver.add(Sum([If(And(wall[i] == w, pos[i] == 0), 1, 0) for i in range(8)]) == 1)
    solver.add(Sum([If(And(wall[i] == w, pos[i] == 1), 1, 0) for i in range(8)]) == 1)

# No wall has only watercolors: each wall has at least one oil
for w in range(1, 5):
    solver.add(Or([And(wall[i] == w, painting_type[i] == 0) for i in range(8)]))

# No wall has work of only one student: each student at most 1 painting per wall
for w in range(1, 5):
    for s in range(4):
        solver.add(Sum([If(And(wall[i] == w, painting_student[i] == s), 1, 0) for i in range(8)]) <= 1)

# No wall has both Franz and Isaacs
for w in range(1, 5):
    franz_on_w = Or([And(wall[i] == w, painting_student[i] == 0) for i in range(8)])
    isaacs_on_w = Or([And(wall[i] == w, painting_student[i] == 3) for i in range(8)])
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Greene's watercolor (idx 3) is upper on same wall as Franz's oil (idx 0)
solver.add(wall[3] == wall[0])
solver.add(pos[3] == 0)

# Isaacs's oil (idx 6) is lower on wall 4
solver.add(wall[6] == 4)
solver.add(pos[6] == 1)

# GIVEN: Franz's oil is on wall 1
solver.add(wall[0] == 1)
# Since G_W is upper on wall 1, F_O must be lower on wall 1
solver.add(pos[0] == 1)

# Define answer options
opt_a = (wall[1] == 4)  # Franz's watercolor on wall 4
opt_b = (wall[2] == 2)  # Greene's oil on wall 2
opt_c = (wall[3] == 2)  # Greene's watercolor on wall 2
opt_d = (wall[5] == 3)  # Hidalgo's watercolor on wall 3
opt_e = (wall[6] == 1)  # Isaacs's oil on wall 1

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT - wall assignments:")
        names = ["F_O", "F_W", "G_O", "G_W", "H_O", "H_W", "I_O", "I_W"]
        for i in range(8):
            print(f"  {names[i]}: wall={m[wall[i]]}, pos={'upper' if m[pos[i]]==0 else 'lower'}")
    else:
        print(f"Option {letter}: {result}")
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