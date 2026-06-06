from z3 import *

solver = Solver()
# Variables for positions
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
vars = [F, H, L, O, P, R, S, T]
for v in vars:
    solver.add(v >= 1, v <= 8)
solver.add(Distinct(vars))

# Base constraints
solver.add(Or(T + 1 == F, T == R + 1))  # T before F or after R
solver.add(Or(F - R >= 3, R - F >= 3))   # at least two between F and R
solver.add(Or(O == 1, O == 5))          # O first or fifth
solver.add(Or(L == 8, H == 8))          # eighth is L or H
solver.add(P < S)                       # P before S
solver.add(Or(S - O >= 2, O - S >= 2))  # at least one between O and S
# Conditional premise: O immediately after T
solver.add(O == T + 1)

found_options = []
options = [
    ("A", Or(F == 1, F == 2)),
    ("B", Or(F == 2, F == 3)),
    ("C", Or(F == 4, F == 6)),
    ("D", Or(F == 4, F == 7)),
    ("E", Or(F == 6, F == 7))
]
for letter, opt_constr in options:
    solver.push()
    # To test if F must be in these positions, assert that it is NOT in them and see if unsat
    solver.add(Not(opt_constr))
    res = solver.check()
    if res == unsat:
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