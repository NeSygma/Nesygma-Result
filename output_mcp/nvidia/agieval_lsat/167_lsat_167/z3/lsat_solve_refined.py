from z3 import *
solver = Solver()
# Declare position variables
p_P = Int('p_P')
p_Q = Int('p_Q')
p_R = Int('p_R')
p_S = Int('p_S')
p_T = Int('p_T')
p_V = Int('p_V')
p_W = Int('p_W')
# Domain constraints (1..7)
for var in [p_P, p_Q, p_R, p_S, p_T, p_V, p_W]:
    solver.add(var >= 1, var <= 7)
# Base constraints
solver.add(Distinct([p_P, p_Q, p_R, p_S, p_T, p_V, p_W]))
solver.add(p_P == 4)
solver.add(p_V + 1 == p_W)  # Villas immediately before White
solver.add(p_Q < p_R)      # Quinn earlier than Rovero
solver.add(p_W + 1 == p_Q) # White immediately before Quinn (given condition)
solver.add(p_S != p_T + 1)
solver.add(p_S != p_T - 1)
# Options constraints: test each option being at position 6
found_options = []
for letter, constr in [("A", p_Q == 6), ("B", p_R == 6), ("C", p_S == 6), ("D", p_V == 6), ("E", p_W == 6)]:
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