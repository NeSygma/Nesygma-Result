from z3 import *

solver = Solver()

# Declare variables
pos_F_o = Int('pos_F_o')
pos_F_w = Int('pos_F_w')
pos_G_o = Int('pos_G_o')
pos_G_w = Int('pos_G_w')
pos_H_o = Int('pos_H_o')
pos_H_w = Int('pos_H_w')
pos_I_o = Int('pos_I_o')
pos_I_w = Int('pos_I_w')

# Base constraints
# 1. Positions between 0 and 7
solver.add(And(pos_F_o >= 0, pos_F_o <= 7))
solver.add(And(pos_F_w >= 0, pos_F_w <= 7))
solver.add(And(pos_G_o >= 0, pos_G_o <= 7))
solver.add(And(pos_G_w >= 0, pos_G_w <= 7))
solver.add(And(pos_H_o >= 0, pos_H_o <= 7))
solver.add(And(pos_H_w >= 0, pos_H_w <= 7))
solver.add(And(pos_I_o >= 0, pos_I_o <= 7))
solver.add(And(pos_I_w >= 0, pos_I_w <= 7))

# 2. All distinct
solver.add(Distinct([pos_F_o, pos_F_w, pos_G_o, pos_G_w, pos_H_o, pos_H_w, pos_I_o, pos_I_w]))

# 3. Each wall has exactly one oil and one watercolor
# Define walls: for w in 1..4, positions are 2*(w-1) and 2*(w-1)+1
for w in range(1,5):
    # Oils
    solver.add(Sum([If(Or(pos_F_o == 2*(w-1), pos_F_o == 2*(w-1)+1), 1, 0),
                    If(Or(pos_G_o == 2*(w-1), pos_G_o == 2*(w-1)+1), 1, 0),
                    If(Or(pos_H_o == 2*(w-1), pos_H_o == 2*(w-1)+1), 1, 0),
                    If(Or(pos_I_o == 2*(w-1), pos_I_o == 2*(w-1)+1), 1, 0)]) == 1)
    # Watercolors
    solver.add(Sum([If(Or(pos_F_w == 2*(w-1), pos_F_w == 2*(w-1)+1), 1, 0),
                    If(Or(pos_G_w == 2*(w-1), pos_G_w == 2*(w-1)+1), 1, 0),
                    If(Or(pos_H_w == 2*(w-1), pos_H_w == 2*(w-1)+1), 1, 0),
                    If(Or(pos_I_w == 2*(w-1), pos_I_w == 2*(w-1)+1), 1, 0)]) == 1)

# 4. Each student's oil and watercolor on different walls
# Compute wall for each painting using ToInt(pos/2)+1
def wall(pos):
    return ToInt(pos / 2) + 1

solver.add(wall(pos_F_o) != wall(pos_F_w))
solver.add(wall(pos_G_o) != wall(pos_G_w))
solver.add(wall(pos_H_o) != wall(pos_H_w))
solver.add(wall(pos_I_o) != wall(pos_I_w))

# 5. No wall has both Franz and Isaacs
for w in range(1,5):
    # Count paintings by Franz or Isaacs on wall w
    count = 0
    # Franz's oil
    count += If(Or(pos_F_o == 2*(w-1), pos_F_o == 2*(w-1)+1), 1, 0)
    # Franz's watercolor
    count += If(Or(pos_F_w == 2*(w-1), pos_F_w == 2*(w-1)+1), 1, 0)
    # Isaacs's oil
    count += If(Or(pos_I_o == 2*(w-1), pos_I_o == 2*(w-1)+1), 1, 0)
    # Isaacs's watercolor
    count += If(Or(pos_I_w == 2*(w-1), pos_I_w == 2*(w-1)+1), 1, 0)
    solver.add(count <= 1)

# 6. Greene's watercolor is in upper position of the wall where Franz's oil is displayed
w_f = wall(pos_F_o)
solver.add(wall(pos_G_w) == w_f)
solver.add(pos_G_w % 2 == 0)

# 7. Isaacs's oil is in lower position of wall 4
solver.add(wall(pos_I_o) == 4)
solver.add(pos_I_o % 2 == 1)

# Define answer choices as constraints
opt_a = (wall(pos_F_w) == wall(pos_G_o))
opt_b = (wall(pos_F_w) == wall(pos_H_o))
opt_c = (pos_G_o % 2 == 0)
opt_d = (pos_H_w % 2 == 1)
opt_e = (wall(pos_I_w) == wall(pos_H_o))

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

BENCHMARK_MODE = True
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")