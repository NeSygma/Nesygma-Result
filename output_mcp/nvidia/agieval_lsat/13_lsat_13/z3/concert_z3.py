from z3 import *

solver = Solver()

# Declare position variables
F_pos = Int('F_pos')
H_pos = Int('H_pos')
L_pos = Int('L_pos')
O_pos = Int('O_pos')
P_pos = Int('P_pos')
R_pos = Int('R_pos')
S_pos = Int('S_pos')
T_pos = Int('T_pos')

# Domain constraints
for var in [F_pos, H_pos, L_pos, O_pos, P_pos, R_pos, S_pos, T_pos]:
    solver.add(var >= 1, var <= 8)

# All-different
solver.add(Distinct([F_pos, H_pos, L_pos, O_pos, P_pos, R_pos, S_pos, T_pos]))

# Base constraints
# T is immediately before F or immediately after R
solver.add(Or(T_pos == F_pos - 1, T_pos == R_pos + 1))

# At least two compositions between F and R
solver.add(Or(F_pos >= R_pos + 3, R_pos >= F_pos + 3))

# O is first or fifth
solver.add(Or(O_pos == 1, O_pos == 5))

# Eighth composition is L or H
solver.add(Or(L_pos == 8, H_pos == 8))

# P before S
solver.add(P_pos < S_pos)

# At least one composition between O and S
solver.add(Or(O_pos + 1 < S_pos, S_pos + 1 < O_pos))

# Define option constraints
opt_a_constr = P_pos == 2
opt_b_constr = P_pos == 3
opt_c_constr = P_pos == 4
opt_d_constr = P_pos == 6
opt_e_constr = P_pos == 7

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