from z3 import *

solver = Solver()

# Define Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

# Base constraints from the problem
# 1. Panel must include at least one scientist of each type
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# 2. If more than one botanist is selected, then at most one zoologist is selected
# More than one botanist: at least two of F, G, H are True
botanist_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zoologist_count = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# 3. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 4. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 5. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional constraints: exactly 5 scientists selected
total_selected = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0),
                      If(K, 1, 0), If(L, 1, 0), If(M, 1, 0),
                      If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(total_selected == 5)

# Given: four of the scientists selected are F, L, Q, and R
solver.add(F == True)
solver.add(L == True)
solver.add(Q == True)
solver.add(R == True)

# Now test each option for the fifth scientist
found_options = []

# Option A: G is the fifth scientist
solver.push()
solver.add(G == True)
# Since we already have F, L, Q, R selected, adding G means we have 5 scientists
# We need to ensure no other scientist is selected (except possibly the fifth)
# But we must check consistency with all constraints
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is the fifth scientist
solver.push()
solver.add(H == True)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: K is the fifth scientist
solver.push()
solver.add(K == True)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: M is the fifth scientist
solver.push()
solver.add(M == True)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P is the fifth scientist
solver.push()
solver.add(P == True)
if solver.check() == sat:
    found_options.append("E")
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