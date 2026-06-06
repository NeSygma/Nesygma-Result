from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the order of auditions as a list of 6 integers
# 0: Kammer (K), 1: Lugo (L), 2: Trillo (T), 3: Waite (W), 4: Yoshida (Y), 5: Zinn (Z)
order = [Int(f'order_{i}') for i in range(6)]

# Declare variables for the position of each singer
pos_K = Int('pos_K')  # Kammer
pos_L = Int('pos_L')  # Lugo
pos_T = Int('pos_T')  # Trillo
pos_W = Int('pos_W')  # Waite
pos_Y = Int('pos_Y')  # Yoshida
pos_Z = Int('pos_Z')  # Zinn

solver = Solver()

# 1. All singers are distinct and each position is assigned to exactly one singer
solver.add(Distinct(order))

# 2. Each singer's position is unique and within 0..5
solver.add(pos_K >= 0, pos_K < 6)
solver.add(pos_L >= 0, pos_L < 6)
solver.add(pos_T >= 0, pos_T < 6)
solver.add(pos_W >= 0, pos_W < 6)
solver.add(pos_Y >= 0, pos_Y < 6)
solver.add(pos_Z >= 0, pos_Z < 6)

# 3. The fourth audition (index 3) cannot be recorded
# Recorded singers are K (0) and L (1)
solver.add(Not(Or([order[3] == 0, order[3] == 1])))

# 4. The fifth audition (index 4) must be recorded
solver.add(Or([order[4] == 0, order[4] == 1]))

# 5. Waite's audition (3) must take place earlier than the two recorded auditions (0 and 1)
solver.add(pos_W < pos_K)
solver.add(pos_W < pos_L)

# 6. Kammer's audition (0) must take place earlier than Trillo's audition (2)
solver.add(pos_K < pos_T)

# 7. Zinn's audition (5) must take place earlier than Yoshida's audition (4)
solver.add(pos_Z < pos_Y)

# 8. Each position is assigned to exactly one singer
solver.add(Distinct([pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]))

# Link the order list to the positions
for i in range(6):
    solver.add(Or([
        And(order[i] == 0, pos_K == i),
        And(order[i] == 1, pos_L == i),
        And(order[i] == 2, pos_T == i),
        And(order[i] == 3, pos_W == i),
        And(order[i] == 4, pos_Y == i),
        And(order[i] == 5, pos_Z == i)
    ]))

# 9. Kammer's audition is immediately before Yoshida's audition
# This means there exists an i such that pos_K = i and pos_Y = i+1
solver.add(Or([And(pos_K == i, pos_Y == i+1) for i in range(5)]))

# Now, evaluate each multiple-choice option
found_options = []

# Option A: Kammer's audition is second (pos_K == 1)
opt_a_constr = (pos_K == 1)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Trillo's audition is fourth (pos_T == 3)
opt_b_constr = (pos_T == 3)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Waite's audition is third (pos_W == 2)
opt_c_constr = (pos_W == 2)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yoshida's audition is sixth (pos_Y == 5)
opt_d_constr = (pos_Y == 5)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zinn's audition is second (pos_Z == 1)
opt_e_constr = (pos_Z == 1)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")