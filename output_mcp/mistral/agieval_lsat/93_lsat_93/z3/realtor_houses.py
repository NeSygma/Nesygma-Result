from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Helper function to find the index of a value in a list
def Index(lst, val):
    return Sum([If(lst[i] == val, 1, 0) * i for i in range(7)])

# Base constraints solver
solver = Solver()

# Houses: J, K, L, M, N, O, P
# Represented as indices: J=0, K=1, L=2, M=3, N=4, O=5, P=6
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
order = [Int(f'pos_{i}') for i in range(7)]

# All houses must be distinct and in the range [0, 6]
solver.add(Distinct(order))
for i in range(7):
    solver.add(order[i] >= 0, order[i] <= 6)

# Constraint 1: J (index 0) must be in evening (positions 5 or 6)
solver.add(Or(order[5] == 0, order[6] == 0))

# Constraint 2: K (index 1) cannot be in morning (positions 0 or 1)
solver.add(Not(Or(order[0] == 1, order[1] == 1)))

# Constraint 3: L (index 2) must be shown after K (index 1) and before M (index 3)
k_pos = Index(order, 1)
l_pos = Index(order, 2)
m_pos = Index(order, 3)

# K must come before L
solver.add(k_pos < l_pos)
# L must come before M
solver.add(l_pos < m_pos)

# Now, evaluate each option
found_options = []

# Option A: K, O, L, M, N, J, P
# Indices: K=1, O=5, L=2, M=3, N=4, J=0, P=6
opt_a_constr = And(
    order[0] == 1,
    order[1] == 5,
    order[2] == 2,
    order[3] == 3,
    order[4] == 4,
    order[5] == 0,
    order[6] == 6
)

# Option B: N, L, P, K, M, O, J
# Indices: N=4, L=2, P=6, K=1, M=3, O=5, J=0
opt_b_constr = And(
    order[0] == 4,
    order[1] == 2,
    order[2] == 6,
    order[3] == 1,
    order[4] == 3,
    order[5] == 5,
    order[6] == 0
)

# Option C: O, P, K, L, N, M, J
# Indices: O=5, P=6, K=1, L=2, N=4, M=3, J=0
opt_c_constr = And(
    order[0] == 5,
    order[1] == 6,
    order[2] == 1,
    order[3] == 2,
    order[4] == 4,
    order[5] == 3,
    order[6] == 0
)

# Option D: O, P, M, N, K, L, J
# Indices: O=5, P=6, M=3, N=4, K=1, L=2, J=0
opt_d_constr = And(
    order[0] == 5,
    order[1] == 6,
    order[2] == 3,
    order[3] == 4,
    order[4] == 1,
    order[5] == 2,
    order[6] == 0
)

# Option E: P, O, K, J, L, N, M
# Indices: P=6, O=5, K=1, J=0, L=2, N=4, M=3
opt_e_constr = And(
    order[0] == 6,
    order[1] == 5,
    order[2] == 1,
    order[3] == 0,
    order[4] == 2,
    order[5] == 4,
    order[6] == 3
)

# Evaluate each option
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