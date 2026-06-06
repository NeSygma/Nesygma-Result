from z3 import *

# BENCHMARK_MODE is ON for this problem
BENCHMARK_MODE = True

# Declare symbolic variables for each scientist
# Botanists: F, G, H
F, G, H = Bools('F G H')
# Chemists: K, L, M
K, L, M = Bools('K L M')
# Zoologists: P, Q, R
P, Q, R = Bools('P Q R')

# Base constraints from the problem statement
solver = Solver()

# At least one scientist of each type
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# If more than one botanist is selected, then at most one zoologist is selected
# We will enforce this later when we know the number of botanists and zoologists

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Given: Four of the scientists selected are F, L, Q, and R
# So we know F, L, Q, R are selected
solver.add(F)
solver.add(L)
solver.add(Q)
solver.add(R)

# Now, we need to find the fifth scientist from the options: G, H, K, M, P
# We will test each option to see which one must be selected

found_options = []

# Option A: G
solver.push()
solver.add(G)
result_A = solver.check()
solver.pop()

# Option B: H
solver.push()
solver.add(H)
result_B = solver.check()
solver.pop()

# Option C: K
solver.push()
solver.add(K)
result_C = solver.check()
solver.pop()

# Option D: M
solver.push()
solver.add(M)
result_D = solver.check()
solver.pop()

# Option E: P
solver.push()
solver.add(P)
result_E = solver.check()
solver.pop()

# Collect the options that are valid
if result_A == sat:
    found_options.append("A")
if result_B == sat:
    found_options.append("B")
if result_C == sat:
    found_options.append("C")
if result_D == sat:
    found_options.append("D")
if result_E == sat:
    found_options.append("E")

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")