from z3 import *

solver = Solver()

# Positions: 0=first, 1=second, 2=third, 3=fourth
# Historians
pos_F, pos_G, pos_H, pos_J = Ints('pos_F pos_G pos_H pos_J')
# Topics
pos_L, pos_O, pos_S, pos_W = Ints('pos_L pos_O pos_S pos_W')

# All positions are 0-3
solver.add(And(0 <= pos_F, pos_F <= 3))
solver.add(And(0 <= pos_G, pos_G <= 3))
solver.add(And(0 <= pos_H, pos_H <= 3))
solver.add(And(0 <= pos_J, pos_J <= 3))
solver.add(And(0 <= pos_L, pos_L <= 3))
solver.add(And(0 <= pos_O, pos_O <= 3))
solver.add(And(0 <= pos_S, pos_S <= 3))
solver.add(And(0 <= pos_W, pos_W <= 3))

# All historians distinct positions, all topics distinct positions
solver.add(Distinct(pos_F, pos_G, pos_H, pos_J))
solver.add(Distinct(pos_L, pos_O, pos_S, pos_W))

# Each historian is assigned to exactly one topic (positions align)
# Actually, the mapping between historian and topic at the same position
# We need to enforce that historian and topic at position i are linked.
# But with the options, we just test each option's specific assignment.

# Constraint 1: Oil paintings and watercolors both earlier than lithographs
solver.add(pos_O < pos_L)
solver.add(pos_W < pos_L)

# Constraint 2: Farley's lecture earlier than oil paintings
solver.add(pos_F < pos_O)

# Constraint 3: Holden's lecture earlier than both Garcia's and Jiang's
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Now test each option
options = []

# Option A: 1st:Farley(sculptures), 2nd:Holden(lithographs), 3rd:Garcia(oil paintings), 4th:Jiang(watercolors)
opt_a = [
    pos_F == 0, pos_S == 0,
    pos_H == 1, pos_L == 1,
    pos_G == 2, pos_O == 2,
    pos_J == 3, pos_W == 3
]

# Option B: 1st:Farley(watercolors), 2nd:Jiang(oil paintings), 3rd:Holden(sculptures), 4th:Garcia(lithographs)
opt_b = [
    pos_F == 0, pos_W == 0,
    pos_J == 1, pos_O == 1,
    pos_H == 2, pos_S == 2,
    pos_G == 3, pos_L == 3
]

# Option C: 1st:Garcia(sculptures), 2nd:Farley(watercolors), 3rd:Holden(oil paintings), 4th:Jiang(lithographs)
opt_c = [
    pos_G == 0, pos_S == 0,
    pos_F == 1, pos_W == 1,
    pos_H == 2, pos_O == 2,
    pos_J == 3, pos_L == 3
]

# Option D: 1st:Holden(oil paintings), 2nd:Jiang(watercolors), 3rd:Farley(lithographs), 4th:Garcia(sculptures)
opt_d = [
    pos_H == 0, pos_O == 0,
    pos_J == 1, pos_W == 1,
    pos_F == 2, pos_L == 2,
    pos_G == 3, pos_S == 3
]

# Option E: 1st:Holden(sculptures), 2nd:Farley(watercolors), 3rd:Jiang(oil paintings), 4th:Garcia(lithographs)
opt_e = [
    pos_H == 0, pos_S == 0,
    pos_F == 1, pos_W == 1,
    pos_J == 2, pos_O == 2,
    pos_G == 3, pos_L == 3
]

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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