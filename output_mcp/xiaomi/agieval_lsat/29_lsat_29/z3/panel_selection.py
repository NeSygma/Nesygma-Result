from z3 import *

# Define Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

solver = Solver()

# Base constraints from problem statement
# 1. Panel of exactly 5 scientists
solver.add(Sum([If(s, 1, 0) for s in [F, G, H, K, L, M, P, Q, R]]) == 5)

# 2. At least one of each type
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# 3. If more than one botanist selected, then at most one zoologist selected
botanist_count = Sum([If(s, 1, 0) for s in [F, G, H]])
zoologist_count = Sum([If(s, 1, 0) for s in [P, Q, R]])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 5. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional constraint: G and H are both selected (given in question)
solver.add(G)
solver.add(H)

# Define answer choice constraints
# Each option says "the panel must include either X or else Y"
# We interpret this as: if G and H are selected, then (X OR Y) must be true
# We need to find which option is necessarily true given the constraints

# Option A: F or else K
opt_a = Or(F, K)
# Option B: F or else M
opt_b = Or(F, M)
# Option C: K or else M
opt_c = Or(K, M)
# Option D: M or else Q
opt_d = Or(M, Q)
# Option E: P or else Q
opt_e = Or(P, Q)

# We need to find which option is ALWAYS true when G and H are selected
# For each option, check if its negation is unsatisfiable with the base constraints
# If negation is unsat, then the option is necessarily true

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
necessary_options = []

for letter, opt in options:
    # Check if NOT(opt) is satisfiable with base constraints
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(opt))
    if s.check() == unsat:
        # If NOT(opt) is unsatisfiable, then opt is necessarily true
        necessary_options.append(letter)

if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessary options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No necessary options found")