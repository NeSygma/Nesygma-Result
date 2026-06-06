from z3 import *

solver = Solver()

# Declare symbolic variables for the order of houses (0 to 6)
# 0 = first, 1 = second, 2 = third, 3 = fourth, 4 = fifth, 5 = sixth, 6 = seventh
houses = [Int(f'house_{i}') for i in range(7)]

# Each house is one of J, K, L, M, N, O, P
# We'll use integer values to represent the houses for simplicity
# Let's assign: J=0, K=1, L=2, M=3, N=4, O=5, P=6
J, K, L, M, N, O, P = 0, 1, 2, 3, 4, 5, 6

# All houses must be distinct
solver.add(Distinct(houses))

# Assign the actual house values to the order variables
for i in range(7):
    solver.add(Or([houses[i] == h for h in [J, K, L, M, N, O, P]]))

# Morning: positions 0 and 1
# Afternoon: positions 2, 3, 4
# Evening: positions 5 and 6

# Rule 1: J must be shown in the evening (positions 5 or 6)
solver.add(Or(houses[5] == J, houses[6] == J))

# Rule 2: K cannot be shown in the morning (positions 0 or 1)
solver.add(And(houses[0] != K, houses[1] != K))

# Rule 3: L must be shown after K and before M
# Helper function to find the index of a house in the houses list
def get_pos(house):
    return [If(houses[i] == house, i, -1) for i in range(7)]

# Get positions for K, L, M, J, N, O, P
k_pos = Int('k_pos')
l_pos = Int('l_pos')
m_pos = Int('m_pos')
j_pos = Int('j_pos')
n_pos = Int('n_pos')
o_pos = Int('o_pos')
p_pos = Int('p_pos')

solver.add(k_pos == Sum([If(houses[i] == K, i, 0) for i in range(7)]))
solver.add(l_pos == Sum([If(houses[i] == L, i, 0) for i in range(7)]))
solver.add(m_pos == Sum([If(houses[i] == M, i, 0) for i in range(7)]))
solver.add(j_pos == Sum([If(houses[i] == J, i, 0) for i in range(7)]))
solver.add(n_pos == Sum([If(houses[i] == N, i, 0) for i in range(7)]))
solver.add(o_pos == Sum([If(houses[i] == O, i, 0) for i in range(7)]))
solver.add(p_pos == Sum([If(houses[i] == P, i, 0) for i in range(7)]))

# L must be after K and before M
solver.add(l_pos > k_pos)
solver.add(l_pos < m_pos)

# Base constraints for the multiple choice options
# Option A: K is shown at some time after J is shown
# This means the position of K is greater than the position of J
opt_a_constr = (k_pos > j_pos)

# Option B: L is shown at some time after J is shown
# This means the position of L is greater than the position of J
opt_b_constr = (l_pos > j_pos)

# Option C: P is shown at some time after J is shown
# This means the position of P is greater than the position of J
opt_c_constr = (p_pos > j_pos)

# Option D: Both N and O are shown at some time after M is shown
# This means the positions of N and O are greater than the position of M
opt_d_constr = And(
    n_pos > m_pos,
    o_pos > m_pos
)

# Option E: Both N and P are shown at some time after K is shown
# This means the positions of N and P are greater than the position of K
opt_e_constr = And(
    n_pos > k_pos,
    p_pos > k_pos
)

# Test each option
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