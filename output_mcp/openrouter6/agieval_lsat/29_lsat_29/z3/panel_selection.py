from z3 import *

# Define boolean variables for each scientist
F, G, H, K, L, M, P, Q, R = Bools('F G H K L M P Q R')

# Base constraints
solver = Solver()

# 1. At least one of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# 2. If more than one botanist, then at most one zoologist
# More than one botanist: at least two of F, G, H
botanist_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zoologist_count = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(botanist_count >= 2, zoologist_count <= 1))

# 3. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 4. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 5. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# 6. Panel size exactly 5
total = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0),
             If(K, 1, 0), If(L, 1, 0), If(M, 1, 0),
             If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(total == 5)

# Now, we need to check for each option whether it is forced given G and H are selected.
# We'll test each option by checking if the negation is unsatisfiable.
# The negation of the implication "if G and H selected then (X or Y)" is: G and H and not (X or Y).
# If that is unsat, then the implication is necessary.

# We'll use a single solver and push/pop for each option.
# But we need to add base constraints only once. We already added them.
# For each option, we push, add G and H, add not (X or Y), check for unsat.
# If unsat, then the option is necessary.

found_options = []

# Option A: F or K
solver.push()
solver.add(G, H)  # G and H are selected
solver.add(Not(Or(F, K)))  # neither F nor K is selected
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: F or M
solver.push()
solver.add(G, H)
solver.add(Not(Or(F, M)))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: K or M
solver.push()
solver.add(G, H)
solver.add(Not(Or(K, M)))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: M or Q
solver.push()
solver.add(G, H)
solver.add(Not(Or(M, Q)))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: P or Q
solver.push()
solver.add(G, H)
solver.add(Not(Or(P, Q)))
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

# Now, based on found_options, print the result.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")