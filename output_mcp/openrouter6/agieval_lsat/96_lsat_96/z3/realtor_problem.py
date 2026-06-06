from z3 import *

solver = Solver()

# Declare variables for positions of houses
J, K, L, M, N, O, P = Ints('J K L M N O P')

# All positions are between 1 and 7 inclusive
solver.add(J >= 1, J <= 7)
solver.add(K >= 1, K <= 7)
solver.add(L >= 1, L <= 7)
solver.add(M >= 1, M <= 7)
solver.add(N >= 1, N <= 7)
solver.add(O >= 1, O <= 7)
solver.add(P >= 1, P <= 7)

# All positions are distinct
solver.add(Distinct(J, K, L, M, N, O, P))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(J == 6, J == 7))

# Rule 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(Not(Or(K == 1, K == 2)))

# Rule 3: L must be shown after K and before M
solver.add(L > K)
solver.add(L < M)

# Define option constraints
opt_a_constr = (K > J)          # K after J
opt_b_constr = (L > J)          # L after J
opt_c_constr = (P > J)          # P after J
opt_d_constr = And(N > M, O > M)  # Both N and O after M
opt_e_constr = And(N > K, P > K)  # Both N and P after K

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