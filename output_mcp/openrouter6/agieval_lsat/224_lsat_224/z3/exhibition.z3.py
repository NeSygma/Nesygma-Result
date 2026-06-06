from z3 import *

# Create solver
solver = Solver()

# Define painting indices
# 0: Franz oil, 1: Franz watercolor
# 2: Greene oil, 3: Greene watercolor  
# 4: Hidalgo oil, 5: Hidalgo watercolor
# 6: Isaacs oil, 7: Isaacs watercolor
paintings = list(range(8))

# Slot variables: each painting assigned to a slot 0-7
# Slot mapping: 0:(1,U), 1:(1,L), 2:(2,U), 3:(2,L), 4:(3,U), 5:(3,L), 6:(4,U), 7:(4,L)
slot = [Int(f"slot_{p}") for p in paintings]

# Base constraints: each slot 0-7, all distinct
for p in paintings:
    solver.add(slot[p] >= 0)
    solver.add(slot[p] <= 7)
solver.add(Distinct(slot))

# Precomputed data for each painting
students = [0, 0, 1, 1, 2, 2, 3, 3]  # Franz=0, Greene=1, Hidalgo=2, Isaacs=3
is_wc = [False, True, False, True, False, True, False, True]  # watercolor flags

# Helper functions for Z3 expressions
def wall_index(p):
    return UDiv(slot[p], 2)  # integer division by 2

def position(p):
    return Mod(slot[p], 2)  # 0=upper, 1=lower

# Constraint 1: No wall has only watercolors
# Constraint 2: No wall has work of only one student
# Constraint 3: No wall has both Franz and Isaacs
for p1 in paintings:
    for p2 in paintings:
        if p1 >= p2:
            continue
        same_wall = (wall_index(p1) == wall_index(p2))
        
        # Constraint 1: not both watercolors on same wall
        if is_wc[p1] and is_wc[p2]:
            solver.add(Not(same_wall))
        
        # Constraint 2: different students on same wall
        if students[p1] == students[p2]:
            solver.add(Not(same_wall))
        
        # Constraint 3: no Franz + Isaacs on same wall
        if (students[p1] == 0 and students[p2] == 3) or (students[p1] == 3 and students[p2] == 0):
            solver.add(Not(same_wall))

# Constraint 4: Greene's watercolor (3) is upper on wall where Franz's oil (0) is displayed
solver.add(wall_index(0) == wall_index(3))  # same wall
solver.add(position(3) == 0)  # Greene's watercolor is upper

# Constraint 5: Isaacs's oil (6) is lower on wall 4
solver.add(slot[6] == 7)  # wall 4, lower position

# Now evaluate answer choices
options = []

# Option A: Both Franz's and both Greene's in lower positions
opt_a = And(
    position(0) == 1,  # Franz oil lower
    position(1) == 1,  # Franz watercolor lower
    position(2) == 1,  # Greene oil lower
    position(3) == 1   # Greene watercolor lower
)
options.append(("A", opt_a))

# Option B: Both Franz's and both Greene's in upper positions
opt_b = And(
    position(0) == 0,
    position(1) == 0,
    position(2) == 0,
    position(3) == 0
)
options.append(("B", opt_b))

# Option C: Both Franz's and both Hidalgo's in upper positions
opt_c = And(
    position(0) == 0,
    position(1) == 0,
    position(4) == 0,
    position(5) == 0
)
options.append(("C", opt_c))

# Option D: Both Greene's and both Hidalgo's in lower positions
opt_d = And(
    position(2) == 1,
    position(3) == 1,
    position(4) == 1,
    position(5) == 1
)
options.append(("D", opt_d))

# Option E: Both Greene's and both Hidalgo's in upper positions
opt_e = And(
    position(2) == 0,
    position(3) == 0,
    position(4) == 0,
    position(5) == 0
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