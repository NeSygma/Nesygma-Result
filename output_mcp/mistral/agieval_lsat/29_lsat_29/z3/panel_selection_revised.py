from z3 import *

# Declare Boolean variables for each scientist
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# Base constraints for the panel selection
solver = Solver()

# 1. Panel size: exactly 5 scientists
panel = [F, G, H, K, L, M, P, Q, R]
solver.add(Sum(panel) == 5)

# 2. At least one scientist of each type
# Botanist: F, G, H
# Chemist: K, L, M
# Zoologist: P, Q, R
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# 3. If more than one botanist is selected, then at most one zoologist is selected
# Botanists selected count
botanists_selected = Sum([F, G, H])
zoologists_selected = Sum([P, Q, R])
solver.add(Implies(botanists_selected > 1, zoologists_selected <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 5. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional constraint: Both G and H are selected
solver.add(And(G, H))

# Now evaluate the multiple-choice options for necessity
# Each option is necessary if its negation leads to unsat
necessary_options = []

# Option A: F or else K
# Negation: Not F and Not K
solver.push()
solver.add(Not(Or(F, K)))
if solver.check() == unsat:
    necessary_options.append("A")
solver.pop()

# Option B: F or else M
# Negation: Not F and Not M
solver.push()
solver.add(Not(Or(F, M)))
if solver.check() == unsat:
    necessary_options.append("B")
solver.pop()

# Option C: K or else M
# Negation: Not K and Not M
solver.push()
solver.add(Not(Or(K, M)))
if solver.check() == unsat:
    necessary_options.append("C")
solver.pop()

# Option D: M or else Q
# Negation: Not M and Not Q
solver.push()
solver.add(Not(Or(M, Q)))
if solver.check() == unsat:
    necessary_options.append("D")
solver.pop()

# Option E: P or else Q
# Negation: Not P and Not Q
solver.push()
solver.add(Not(Or(P, Q)))
if solver.check() == unsat:
    necessary_options.append("E")
solver.pop()

# Output the result
if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")