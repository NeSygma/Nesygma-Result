from z3 import *

# Students: F=0, G=1, H=2, I=3
# Types: O=0, W=1
# Walls: 0, 1, 2, 3 (representing 1, 2, 3, 4)
# Positions: 0 (Upper), 1 (Lower)

solver = Solver()

# Variables
student = [[Int(f's_{w}_{p}') for p in range(2)] for w in range(4)]
ptype = [[Int(f't_{w}_{p}') for p in range(2)] for w in range(4)]

for w in range(4):
    for p in range(2):
        solver.add(student[w][p] >= 0, student[w][p] <= 3)
        solver.add(ptype[w][p] >= 0, ptype[w][p] <= 1)

# Each student has exactly one O and one W
for s in range(4):
    solver.add(Sum([If(student[w][p] == s, If(ptype[w][p] == 0, 1, 0), 0) for w in range(4) for p in range(2)]) == 1)
    solver.add(Sum([If(student[w][p] == s, If(ptype[w][p] == 1, 1, 0), 0) for w in range(4) for p in range(2)]) == 1)

# C1: No wall has only watercolors
for w in range(4):
    solver.add(Sum([If(ptype[w][p] == 0, 1, 0) for p in range(2)]) >= 1)

# C2: No wall has only one student
for w in range(4):
    solver.add(student[w][0] != student[w][1])

# C3: No wall has both F and I
for w in range(4):
    solver.add(Not(And(Or(student[w][0] == 0, student[w][1] == 0), Or(student[w][0] == 3, student[w][1] == 3))))

# C4: G's watercolor (GW) is in the upper position of the wall where F's oil (FO) is in the lower position.
solver.add(Or([And(student[w][0] == 1, ptype[w][0] == 1, student[w][1] == 0, ptype[w][1] == 0) for w in range(4)]))

# C5: Isaacs's oil (IO) is in the lower position of wall 4 (index 3).
solver.add(student[3][1] == 3, ptype[3][1] == 0)

# Q: If Hidalgo's oil (HO) is displayed on wall 2 (index 1), which one of the following could also be displayed on wall 2?
# HO is on wall 2: (student[1][0] == 2 and ptype[1][0] == 0) or (student[1][1] == 2 and ptype[1][1] == 0)
solver.add(Or(And(student[1][0] == 2, ptype[1][0] == 0), And(student[1][1] == 2, ptype[1][1] == 0)))

# Options:
# (A) FO: student[1][other_pos] == 0 and ptype[1][other_pos] == 0
# (B) GW: student[1][other_pos] == 1 and ptype[1][other_pos] == 1
# (C) GO: student[1][other_pos] == 1 and ptype[1][other_pos] == 0
# (D) HW: student[1][other_pos] == 2 and ptype[1][other_pos] == 1
# (E) IW: student[1][other_pos] == 3 and ptype[1][other_pos] == 1

found_options = []
for letter, s_val, t_val in [("A", 0, 0), ("B", 1, 1), ("C", 1, 0), ("D", 2, 1), ("E", 3, 1)]:
    solver.push()
    # The other painting on wall 2 is (s_val, t_val)
    # This means:
    # (HO is at pos 0 AND (s_val, t_val) is at pos 1) OR (HO is at pos 1 AND (s_val, t_val) is at pos 0)
    solver.add(Or(
        And(student[1][0] == 2, ptype[1][0] == 0, student[1][1] == s_val, ptype[1][1] == t_val),
        And(student[1][1] == 2, ptype[1][1] == 0, student[1][0] == s_val, ptype[1][0] == t_val)
    ))
    
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