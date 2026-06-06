from z3 import *

solver = Solver()

# Variables
K = [Int(f'K{i}') for i in range(7)]
P = [Int(f'P{i}') for i in range(7)]

# Domain constraints
for i in range(7):
    solver.add(K[i] >= 0, K[i] <= 2)
    solver.add(P[i] >= 0, P[i] <= 2)

# Base constraints
solver.add(P[0] == 0)  # day1 puppy is G
for i in range(6):
    solver.add(K[i] != K[i+1])
    solver.add(P[i] != P[i+1])
solver.add(K[0] != K[6])  # day1 kitten not on day7
solver.add(P[6] != 0)     # day7 puppy not G
solver.add(P[6] != 2)     # day7 puppy not R

# H appears exactly 3 times, not on day1
H_count = Sum([If(K[i] == 0, 1, 0) for i in range(7)])
solver.add(H_count == 3)
solver.add(K[0] != 0)

# R not on any day that features H
for i in range(7):
    solver.add(Or(K[i] != 0, P[i] != 2))

# Option A constraint: exactly four breeds each featured on three days
M_count = Sum([If(K[i] == 1, 1, 0) for i in range(7)])
S_count = Sum([If(K[i] == 2, 1, 0) for i in range(7)])
G_count = Sum([If(P[i] == 0, 1, 0) for i in range(7)])
N_count = Sum([If(P[i] == 1, 1, 0) for i in range(7)])
R_count = Sum([If(P[i] == 2, 1, 0) for i in range(7)])
cnt_3_sum = Sum([If(H_count == 3, 1, 0),
                 If(M_count == 3, 1, 0),
                 If(S_count == 3, 1, 0),
                 If(G_count == 3, 1, 0),
                 If(N_count == 3, 1, 0),
                 If(R_count == 3, 1, 0)])
opt_a_constr = (cnt_3_sum == 4)

# Option B constraint
opt_b_constr = And([Or(K[i] != 0, P[i] == 0) for i in range(7)])

# Option C constraint
opt_c_constr = And([Or(P[i] != 0, K[i] == 0) for i in range(7)])

# Option D constraint
opt_d_constr = And([Or(P[i] == 2, K[i] == 0) for i in range(7)])

# Option E constraint
opt_e_constr = And([Or(K[i] == 0, P[i] == 2) for i in range(7)])

# Test each option
found_options = []
options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]

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