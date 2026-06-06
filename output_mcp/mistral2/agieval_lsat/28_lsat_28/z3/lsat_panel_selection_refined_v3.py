from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare scientists as Boolean variables
# Botanists: F, G, H
F, G, H = Bools('F G H')
# Chemists: K, L, M
K, L, M = Bools('K L M')
# Zoologists: P, Q, R
P, Q, R = Bools('P Q R')

# Base constraints from the problem statement
solver = Solver()

# The panel must include at least one scientist of each of the three types
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional constraint: P is the only zoologist selected
solver.add(P)
# Q and R cannot be selected
solver.add(Not(Q))
solver.add(Not(R))

# The panel must have exactly 5 scientists
# Count the number of selected scientists
selected = [F, G, H, K, L, M, P, Q, R]
panel_size = Sum(selected)
solver.add(panel_size == 5)

# If more than one botanist is selected, then at most one zoologist is selected
# Since P is the only zoologist selected, this constraint is automatically satisfied
# So no additional constraint is needed here.

# Now, we need to check the multiple-choice options under the above constraints

# Option A: If K is selected, G cannot be selected
opt_a_constr = Implies(K, Not(G))

# Option B: If L is selected, F cannot be selected
opt_b_constr = Implies(L, Not(F))

# Option C: If exactly one chemist is selected, it must be K
# Define exactly one chemist
chemists = [K, L, M]
exactly_one_chemist = And(
    Sum(chemists) == 1,
    K
)
opt_c_constr = exactly_one_chemist

# Option D: If exactly two chemists are selected, F cannot be selected
# Define exactly two chemists
exactly_two_chemists = And(
    Sum(chemists) == 2,
    Not(F)
)
opt_d_constr = exactly_two_chemists

# Option E: If exactly two chemists are selected, G cannot be selected
# Define exactly two chemists
exactly_two_chemists_e = And(
    Sum(chemists) == 2,
    Not(G)
)
opt_e_constr = exactly_two_chemists_e

# Now, check each option
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