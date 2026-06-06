from z3 import *

# Students: F=0, G=1, H=2, I=3
# Types: O=0, W=1
# Paintings: 
# 0: (F, O), 1: (F, W), 2: (G, O), 3: (G, W), 4: (H, O), 5: (H, W), 6: (I, O), 7: (I, W)
# Positions: (wall, pos) where wall in 0..3, pos in 0..1 (0=U, 1=L)

solver = Solver()

# Variables: wall[p] in 0..3, pos[p] in 0..1
wall = [Int(f'wall_{p}') for p in range(8)]
pos = [Int(f'pos_{p}') for p in range(8)]

# Domain constraints
for p in range(8):
    solver.add(wall[p] >= 0, wall[p] <= 3)
    solver.add(pos[p] >= 0, pos[p] <= 1)

# Each painting is at a unique (wall, pos)
for p1 in range(8):
    for p2 in range(p1 + 1, 8):
        solver.add(Not(And(wall[p1] == wall[p2], pos[p1] == pos[p2])))

# Helper to get painting at (w, p)
def get_painting_at(w, p):
    # Returns the index of the painting at wall w, pos p
    # Since we don't know which painting is where, we use an Or-loop
    # Actually, we can just use the fact that each (w, p) is occupied by exactly one painting
    # Let's define a function that returns the student and type at (w, p)
    pass

# Let's define student_at(w, p) and type_at(w, p)
# student_at[w][p] = student index
# type_at[w][p] = type index
# This is easier with a 4x2 array
student_at = [[Int(f's_{w}_{p}') for p in range(2)] for w in range(4)]
type_at = [[Int(f't_{w}_{p}') for p in range(2)] for w in range(4)]

# Link paintings to the grid
for w in range(4):
    for p in range(2):
        # The painting at (w, p) must be one of the 8
        # This is equivalent to saying: for each (w, p), there exists a unique painting p_idx
        # such that wall[p_idx] == w and pos[p_idx] == p
        # And the student/type of that painting matches student_at/type_at
        
        # Painting definitions:
        # 0: (F, O), 1: (F, W), 2: (G, O), 3: (G, W), 4: (H, O), 5: (H, W), 6: (I, O), 7: (I, W)
        s_vals = [0, 0, 1, 1, 2, 2, 3, 3]
        t_vals = [0, 1, 0, 1, 0, 1, 0, 1]
        
        solver.add(Or([And(wall[p_idx] == w, pos[p_idx] == p, 
                           student_at[w][p] == s_vals[p_idx], 
                           type_at[w][p] == t_vals[p_idx]) for p_idx in range(8)]))

# C1: No wall has only watercolors
for w in range(4):
    solver.add(Or(type_at[w][0] == 0, type_at[w][1] == 0))

# C2: No wall has the work of only one student
for w in range(4):
    solver.add(student_at[w][0] != student_at[w][1])

# C3: No wall has both a painting by Franz (0) and a painting by Isaacs (3)
for w in range(4):
    solver.add(Not(And(student_at[w][0] == 0, student_at[w][1] == 3)))
    solver.add(Not(And(student_at[w][0] == 3, student_at[w][1] == 0)))

# C4: Greene's watercolor (G, W) is displayed in the upper position of the wall on which Franz's oil (F, O) is displayed.
# (G, W) is painting 3, (F, O) is painting 0
# Greene's watercolor (3) is at (w, 0)
# Franz's oil (0) is at (w, 1)
w_gw = Int('w_gw')
solver.add(wall[3] == w_gw, pos[3] == 0)
solver.add(wall[0] == w_gw, pos[0] == 1)

# C5: Isaacs's oil (I, O) is displayed in the lower position of wall 4 (index 3)
# (I, O) is painting 6
solver.add(wall[6] == 3, pos[6] == 1)

# Define options
# (A) Both of Franz's paintings (0, 1) and both of Greene's paintings (2, 3) are displayed in lower positions (pos=1).
opt_a_constr = And(pos[0] == 1, pos[1] == 1, pos[2] == 1, pos[3] == 1)
# (B) Both of Franz's paintings (0, 1) and both of Greene's paintings (2, 3) are displayed in upper positions (pos=0).
opt_b_constr = And(pos[0] == 0, pos[1] == 0, pos[2] == 0, pos[3] == 0)
# (C) Both of Franz's paintings (0, 1) and both of Hidalgo's paintings (4, 5) are displayed in upper positions (pos=0).
opt_c_constr = And(pos[0] == 0, pos[1] == 0, pos[4] == 0, pos[5] == 0)
# (D) Both of Greene's paintings (2, 3) and both of Hidalgo's paintings (4, 5) are displayed in lower positions (pos=1).
opt_d_constr = And(pos[2] == 1, pos[3] == 1, pos[4] == 1, pos[5] == 1)
# (E) Both of Greene's paintings (2, 3) and both of Hidalgo's paintings (4, 5) are displayed in upper positions (pos=0).
opt_e_constr = And(pos[2] == 0, pos[3] == 0, pos[4] == 0, pos[5] == 0)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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