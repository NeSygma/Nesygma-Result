from z3 import *

# Define variables for positions
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_T = Int('pos_T')
pos_W = Int('pos_W')
pos_Y = Int('pos_Y')
pos_Z = Int('pos_Z')
positions = [pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]
solver = Solver()
# Domain constraints
for p in positions:
    solver.add(p >= 1, p <= 6)
# All distinct
solver.add(Distinct(positions))
# Problem constraints
solver.add(pos_K < pos_T)          # Kammer before Trillo
solver.add(pos_Z < pos_Y)          # Zinn before Yoshida
solver.add(pos_W < pos_K)
solver.add(pos_W < pos_L)          # Waite before both recorded
solver.add(pos_K != 4, pos_L != 4) # fourth not recorded
solver.add(Or(pos_K == 5, pos_L == 5)) # fifth recorded

# Define each option's ordering constraints
options = []
# Helper to create constraints from ordering list
def ordering_constraints(order):
    # order is list of singer letters in positions 1..6
    mapping = {
        'K': pos_K,
        'L': pos_L,
        'T': pos_T,
        'W': pos_W,
        'Y': pos_Y,
        'Z': pos_Z,
    }
    cons = []
    for idx, singer in enumerate(order, start=1):
        cons.append(mapping[singer] == idx)
    return cons

options.append(("A", ordering_constraints(['K','T','Z','W','L','Y'])))
options.append(("B", ordering_constraints(['W','K','Y','Z','L','T'])))
options.append(("C", ordering_constraints(['W','L','K','T','Z','Y'])))
options.append(("D", ordering_constraints(['W','Z','K','T','L','Y'])))
options.append(("E", ordering_constraints(['Z','Y','W','L','K','T'])))

found_options = []
for letter, cons in options:
    solver.push()
    solver.add(cons)
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