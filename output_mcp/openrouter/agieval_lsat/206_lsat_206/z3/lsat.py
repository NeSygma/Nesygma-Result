from z3 import *

solver = Solver()
# variables
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_W = Int('pos_W')
pos_T = Int('pos_T')
pos_Z = Int('pos_Z')
pos_Y = Int('pos_Y')
positions = [pos_K, pos_L, pos_W, pos_T, pos_Z, pos_Y]
# domain 1..6
for p in positions:
    solver.add(p >= 1, p <= 6)
# all distinct
solver.add(Distinct(positions))
# fourth not recorded
solver.add(pos_K != 4, pos_L != 4)
# fifth recorded
solver.add(Or(pos_K == 5, pos_L == 5))
# Waite earlier than both recorded
solver.add(pos_W < pos_K)
solver.add(pos_W < pos_L)
# Kammer earlier than Trillo
solver.add(pos_K < pos_T)
# Zinn earlier than Yoshida
solver.add(pos_Z < pos_Y)

# define option constraints for each answer
options = []
# A: Yoshida fifth
options.append(("A", pos_Y == 5))
# B: fourth
options.append(("B", pos_Y == 4))
# C: third
options.append(("C", pos_Y == 3))
# D: second
options.append(("D", pos_Y == 2))
# E: first
options.append(("E", pos_Y == 1))

found_options = []
for letter, constr in options:
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