from z3 import *

solver = Solver()

# Paintings (0-7)
# 0: FO (Franz Oil)     - student 0 (Franz), type 0 (Oil)
# 1: FW (Franz Watercolor) - student 0, type 1
# 2: GO (Greene Oil)      - student 1, type 0
# 3: GW (Greene Watercolor) - student 1, type 1
# 4: HO (Hidalgo Oil)     - student 2, type 0
# 5: HW (Hidalgo Watercolor) - student 2, type 1
# 6: IO (Isaacs Oil)      - student 3, type 0
# 7: IW (Isaacs Watercolor) - student 3, type 1

student_of = [0, 0, 1, 1, 2, 2, 3, 3]  # F=0, G=1, H=2, I=3
type_of = [0, 1, 0, 1, 0, 1, 0, 1]    # O=0, W=1

# For each painting p, which wall (1-4) it's on, and which position (1=upper, 0=lower)
painting_wall = [Int(f'pw_{p}') for p in range(8)]
painting_pos = [Int(f'pp_{p}') for p in range(8)]

for p in range(8):
    solver.add(painting_wall[p] >= 1, painting_wall[p] <= 4)
    solver.add(painting_pos[p] >= 0, painting_pos[p] <= 1)

# Each (wall, position) slot has exactly one painting
for w in range(1, 5):
    for pos in range(2):
        solver.add(Sum([If(And(painting_wall[p] == w, painting_pos[p] == pos), 1, 0) for p in range(8)]) == 1)

# ========== CONSTRAINTS ==========

# Constraint 1: No wall has only watercolors -> each wall has at least one oil
for w in range(1, 5):
    solver.add(Or([And(painting_wall[p] == w, type_of[p] == 0) for p in range(8)]))

# Constraint 2: No wall has the work of only one student -> each wall has at least 2 different students
for w in range(1, 5):
    # Find at least two paintings on wall w with different students
    solver.add(Or([
        And(painting_wall[p1] == w, painting_wall[p2] == w, student_of[p1] != student_of[p2])
        for p1 in range(8) for p2 in range(p1+1, 8)
    ]))

# Constraint 3: No wall has both Franz (student 0) and Isaacs (student 3)
for w in range(1, 5):
    solver.add(Not(And(
        Or([And(painting_wall[p] == w, student_of[p] == 0) for p in range(8)]),
        Or([And(painting_wall[p] == w, student_of[p] == 3) for p in range(8)])
    )))

# Constraint 4: Greene's watercolor (p=3, GW) is in upper position of the wall on which Franz's oil (p=0, FO) is displayed
solver.add(painting_pos[3] == 1)  # upper position
solver.add(painting_wall[3] == painting_wall[0])  # same wall as FO

# Constraint 5: Isaacs's oil (p=6, IO) is in lower position of wall 4
solver.add(painting_wall[6] == 4)
solver.add(painting_pos[6] == 0)  # lower

# ========== GIVEN CONDITIONS ==========
# Isaacs's watercolor (p=7, IW) is displayed on wall 2
solver.add(painting_wall[7] == 2)

# Franz's oil (p=0, FO) is displayed on wall 3
solver.add(painting_wall[0] == 3)

# From constraint 4: GW (p=3) is on same wall as FO, so wall 3, upper position
# Already covered by painting_wall[3] == painting_wall[0] and painting_pos[3] == 1

# ========== EVALUATE OPTIONS ==========
# We need to find which painting MUST be on wall 1
# Option A: Franz's watercolor (p=1, FW) on wall 1
# Option B: Greene's oil (p=2, GO) on wall 1
# Option C: Greene's watercolor (p=3, GW) on wall 1
# Option D: Hidalgo's oil (p=4, HO) on wall 1
# Option E: Hidalgo's watercolor (p=5, HW) on wall 1

# For "must be" questions: check if NOT being on wall 1 is impossible (unsat)
option_names = ["A", "B", "C", "D", "E"]
option_paintings = [1, 2, 3, 4, 5]  # FW, GO, GW, HO, HW

found_must = []
for letter, p in zip(option_names, option_paintings):
    solver.push()
    # Try to find a model where this painting is NOT on wall 1
    solver.add(painting_wall[p] != 1)
    result = solver.check()
    if result == unsat:
        found_must.append(letter)
    solver.pop()

if len(found_must) == 1:
    print("STATUS: sat")
    print(f"answer:{found_must[0]}")
elif len(found_must) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_must}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")