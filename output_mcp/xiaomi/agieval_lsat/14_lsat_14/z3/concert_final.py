from z3 import *

solver = Solver()

F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
positions = [F, H, L, O, P, R, S, T]

for p in positions:
    solver.add(p >= 1, p <= 8)
solver.add(Distinct(positions))

# Given: T is performed fifth and F is performed sixth
solver.add(T == 5)
solver.add(F == 6)

# Condition 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions between F and R
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed before S
solver.add(P < S)

# Condition 6: At least one composition between O and S
solver.add(Or(O - S >= 2, S - O >= 2))

# Define answer options
opt_a_constr = Or(S == 4, S == 7)
opt_b_constr = Or(S == 3, S == 6)
opt_c_constr = Or(S == 3, S == 4)
opt_d_constr = Or(S == 2, S == 7)
opt_e_constr = Or(S == 1, S == 4)

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