from z3 import *

# Declare variables for positions (1..8) of each composition
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')
vars = [F,H,L,O,P,R,S,T]

solver = Solver()
# Domain constraints
for v in vars:
    solver.add(v >= 1, v <= 8)
# All distinct
solver.add(Distinct(vars))

# Base constraints
# 1. T is immediately before F or immediately after R
solver.add(Or(T == F - 1, T == R + 1))
# 2. At least two compositions between F and R => distance >=3
solver.add(Abs(F - R) >= 3)
# 3. O is first or fifth
solver.add(Or(O == 1, O == 5))
# 4. Eighth composition is L or H
solver.add(Or(L == 8, H == 8))
# 5. P before S
solver.add(P < S)
# 6. At least one composition between O and S
solver.add(Abs(O - S) >= 2)

# Helper to build constraints for a given ordering list
def ordering_constraints(order_list):
    # order_list is list of composition symbols in positions 1..8
    mapping = {
        'F': F, 'H': H, 'L': L, 'O': O, 'P': P, 'R': R, 'S': S, 'T': T
    }
    cons = []
    for idx, comp in enumerate(order_list, start=1):
        cons.append(mapping[comp] == idx)
    return And(cons)

# Define each option's ordering
opt_a = ordering_constraints(['L','P','S','R','O','T','F','H'])
opt_b = ordering_constraints(['O','T','P','F','S','H','R','L'])
opt_c = ordering_constraints(['P','T','F','S','L','R','O','H'])
opt_d = ordering_constraints(['P','T','F','S','O','R','L','H'])
opt_e = ordering_constraints(['T','F','P','R','O','L','S','H'])

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