from z3 import *

# Declare Boolean variables for each scientist
F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

# Base constraints
solver = Solver()

# 1. Panel must include at least one scientist of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# 2. If more than one botanist is selected, then at most one zoologist is selected
# More than one botanist: at least two of F,G,H are True
# At most one zoologist: at most one of P,Q,R is True
# We can encode: (count_botanists > 1) → (count_zoologists ≤ 1)
# Use If for counting
botanist_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zoologist_count = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# 3. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 4. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 5. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: Both G and H are selected
solver.add(G)
solver.add(H)

# Panel size: exactly 5 scientists selected
total_count = Sum([If(F,1,0), If(G,1,0), If(H,1,0),
                   If(K,1,0), If(L,1,0), If(M,1,0),
                   If(P,1,0), If(Q,1,0), If(R,1,0)])
solver.add(total_count == 5)

# Now test each option as a necessary condition
# For each option, check if premises + G + H + ¬option is UNSAT
# If UNSAT, then option is necessary

options = [
    ("A", Or(F, K)),          # F or else K
    ("B", Or(F, M)),          # F or else M
    ("C", Or(K, M)),          # K or else M
    ("D", Or(M, Q)),          # M or else Q
    ("E", Or(P, Q))           # P or else Q
]

necessary_options = []
for letter, option_expr in options:
    # Create a new solver for this check
    s_check = Solver()
    # Add all base constraints (including G and H)
    s_check.add(Or(F, G, H))
    s_check.add(Or(K, L, M))
    s_check.add(Or(P, Q, R))
    s_check.add(Implies(botanist_count > 1, zoologist_count <= 1))
    s_check.add(Not(And(F, K)))
    s_check.add(Not(And(K, M)))
    s_check.add(Implies(M, And(P, R)))
    s_check.add(G)
    s_check.add(H)
    s_check.add(total_count == 5)
    # Add negation of the option
    s_check.add(Not(option_expr))
    # Check
    if s_check.check() == unsat:
        necessary_options.append(letter)

# According to the problem, exactly one option should be necessary
if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")