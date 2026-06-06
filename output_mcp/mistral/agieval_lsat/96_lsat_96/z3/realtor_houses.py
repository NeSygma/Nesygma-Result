from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the houses as symbolic integers representing their positions in the sequence
# We have 7 houses: J, K, L, M, N, O, P
# We'll represent the order as a list of 7 integers, where each integer is a house identifier
# Let's map houses to integers for clarity:
# J=0, K=1, L=2, M=3, N=4, O=5, P=6

# Decision variables: order[i] is the house shown at position i (0 to 6)
order = [Int(f"order_{i}") for i in range(7)]

# Helper: All houses are distinct
solver = Solver()
solver.add(Distinct(order))

# Helper: Map house names to their integer IDs
house_to_id = {
    "J": 0,
    "K": 1,
    "L": 2,
    "M": 3,
    "N": 4,
    "O": 5,
    "P": 6
}

# Rule 1: J must be shown in the evening (positions 5 or 6)
solver.add(Or(order[5] == house_to_id["J"], order[6] == house_to_id["J"]))

# Rule 2: K cannot be shown in the morning (positions 0 or 1)
solver.add(Not(Or(order[0] == house_to_id["K"], order[1] == house_to_id["K"])))

# Rule 3: L must be shown after K and before M
# We need to find the positions of K, L, M in the order
# We'll define pos_K, pos_L, pos_M as the positions of K, L, M respectively
pos_K = Int("pos_K")
pos_L = Int("pos_L")
pos_M = Int("pos_M")
pos_J = Int("pos_J")
pos_P = Int("pos_P")
pos_N = Int("pos_N")
pos_O = Int("pos_O")

# Constraints to link the positions to the order using Or-loop pattern
# pos_K is the position of K
solver.add(Or([And(pos_K == i, order[i] == house_to_id["K"]) for i in range(7)]))
# pos_L is the position of L
solver.add(Or([And(pos_L == i, order[i] == house_to_id["L"]) for i in range(7)]))
# pos_M is the position of M
solver.add(Or([And(pos_M == i, order[i] == house_to_id["M"]) for i in range(7)]))
# pos_J is the position of J
solver.add(Or([And(pos_J == i, order[i] == house_to_id["J"]) for i in range(7)]))
# pos_P is the position of P
solver.add(Or([And(pos_P == i, order[i] == house_to_id["P"]) for i in range(7)]))
# pos_N is the position of N
solver.add(Or([And(pos_N == i, order[i] == house_to_id["N"]) for i in range(7)]))
# pos_O is the position of O
solver.add(Or([And(pos_O == i, order[i] == house_to_id["O"]) for i in range(7)]))

# L must be after K
solver.add(pos_K < pos_L)
# L must be before M
solver.add(pos_L < pos_M)

# Now, we have encoded the base constraints.
# Next, we evaluate the multiple-choice options.

# Option A: K is shown at some time after J is shown
opt_A_constr = (pos_K > pos_J)

# Option B: L is shown at some time after J is shown
opt_B_constr = (pos_L > pos_J)

# Option C: P is shown at some time after J is shown
opt_C_constr = (pos_P > pos_J)

# Option D: Both N and O are shown at some time after M is shown
opt_D_constr = And(pos_N > pos_M, pos_O > pos_M)

# Option E: Both N and P are shown at some time after K is shown
opt_E_constr = And(pos_N > pos_K, pos_P > pos_K)

# Now, evaluate each option
found_options = []
for letter, constr in [("A", opt_A_constr), ("B", opt_B_constr), ("C", opt_C_constr), ("D", opt_D_constr), ("E", opt_E_constr)]:
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