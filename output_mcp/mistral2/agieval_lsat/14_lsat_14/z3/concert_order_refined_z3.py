from z3 import *

# BENCHMARK_MODE: ON (as per instructions)
BENCHMARK_MODE = True

# Create a solver
solver = Solver()

# Define the compositions as integers for easier handling
# Let's map: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = [0, 1, 2, 3, 4, 5, 6, 7]

# Create a list of 8 integer variables representing the performance order
# positions 0 to 7 correspond to 1st to 8th performance
order = [Int(f'order_{i}') for i in range(8)]

# Each position must be assigned a unique composition
solver.add(Distinct(order))

# Constraint 1: T is performed either immediately before F or immediately after R
# T=7, F=0, R=5
# Case 1: T immediately before F -> order[i] = 7 and order[i+1] = 0
# Case 2: T immediately after R -> order[i] = 5 and order[i+1] = 7
solver.add(Or(
    Or([And(order[i] == 7, order[i+1] == 0) for i in range(7)]),
    Or([And(order[i] == 5, order[i+1] == 7) for i in range(7)])
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# We need to ensure that in the sequence, there are at least two compositions between F and R in either order.
f_pos = [order[i] == 0 for i in range(8)]
r_pos = [order[i] == 5 for i in range(8)]
f_index = Int('f_index')
r_index = Int('r_index')
solver.add(Or(
    And(
        f_index < r_index,
        r_index - f_index >= 3
    ),
    And(
        r_index < f_index,
        f_index - r_index >= 3
    )
))
# To find f_index and r_index, we can use:
solver.add(Or([And(f_pos[i], f_index == i) for i in range(8)]))
solver.add(Or([And(r_pos[i], r_index == i) for i in range(8)]))

# Constraint 3: O is performed either first or fifth
# O=3
solver.add(Or(order[0] == 3, order[4] == 3))

# Constraint 4: The eighth composition performed is either L or H
# L=2, H=1
solver.add(Or(order[7] == 2, order[7] == 1))

# Constraint 5: P is performed at some time before S
# P=4, S=6
p_before_s = [And(order[i] == 4, order[j] == 6, i < j) for i in range(8) for j in range(i+1, 8)]
solver.add(Or(p_before_s))

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# O=3, S=6
o_pos = [order[i] == 3 for i in range(8)]
s_pos = [order[i] == 6 for i in range(8)]
o_index = Int('o_index')
s_index = Int('s_index')
solver.add(Or(
    And(
        o_index < s_index,
        s_index - o_index >= 2
    ),
    And(
        s_index < o_index,
        o_index - s_index >= 2
    )
))
# To find o_index and s_index:
solver.add(Or([And(o_pos[i], o_index == i) for i in range(8)]))
solver.add(Or([And(s_pos[i], s_index == i) for i in range(8)]))

# Additional condition for the question:
# T is performed fifth and F is performed sixth
# T=7, F=0
# Fifth position is index 4, sixth is index 5
solver.add(order[4] == 7)  # T is fifth
solver.add(order[5] == 0)  # F is sixth

# Now, evaluate the answer choices for S (S=6)
# We need to check for each option if S is in the specified positions
# The question asks: "then S must be performed either ..."
# So we need to check which of the options are forced by the constraints.

# Define the options as constraints on S's position
# S=6
# Option A: S is fourth (index 3) or seventh (index 6)
opt_a_constr = And(Or(order[3] == 6, order[6] == 6), order[5] == 0, order[4] == 7)
# Option B: S is third (index 2) or sixth (index 5)
opt_b_constr = And(Or(order[2] == 6, order[5] == 6), order[5] == 0, order[4] == 7)
# Option C: S is third (index 2) or fourth (index 3)
opt_c_constr = And(Or(order[2] == 6, order[3] == 6), order[5] == 0, order[4] == 7)
# Option D: S is second (index 1) or seventh (index 6)
opt_d_constr = And(Or(order[1] == 6, order[6] == 6), order[5] == 0, order[4] == 7)
# Option E: S is first (index 0) or fourth (index 3)
opt_e_constr = And(Or(order[0] == 6, order[3] == 6), order[5] == 0, order[4] == 7)

# Now, test each option
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