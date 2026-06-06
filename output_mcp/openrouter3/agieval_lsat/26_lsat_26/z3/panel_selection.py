from z3 import *

# Create solver
solver = Solver()

# Define scientists as Boolean variables (True = selected)
botanists = [Bool('F'), Bool('G'), Bool('H')]
chemists = [Bool('K'), Bool('L'), Bool('M')]
zoologists = [Bool('P'), Bool('Q'), Bool('R')]

# Unpack for easier reference
F, G, H = botanists
K, L, M = chemists
P, Q, R = zoologists

# Base constraints

# 1. Panel must include at least one scientist of each type
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# 2. Panel size is exactly 5
solver.add(Sum([If(b, 1, 0) for b in botanists] + 
               [If(c, 1, 0) for c in chemists] + 
               [If(z, 1, 0) for z in zoologists]) == 5)

# 3. If more than one botanist is selected, then at most one zoologist is selected
# More than one botanist: (F+G+H) >= 2
# At most one zoologist: (P+Q+R) <= 1
botanist_count = Sum([If(b, 1, 0) for b in botanists])
zoologist_count = Sum([If(z, 1, 0) for z in zoologists])
solver.add(Implies(botanist_count >= 2, zoologist_count <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 5. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: M is the only chemist selected
# This means M is selected, and K and L are not selected
solver.add(M)
solver.add(Not(K))
solver.add(Not(L))

# Now evaluate each answer choice
# We need to check which one MUST be true (i.e., is true in ALL valid models)

# First, let's find all valid models to see what must be true
# But for efficiency, we'll check each option by seeing if it's implied by the constraints

# For each option, we check if the option is true in all models
# We do this by checking if the negation of the option leads to unsat

# Option A: F and G are both selected
opt_a = And(F, G)
# Check if NOT(opt_a) is compatible with constraints
solver.push()
solver.add(Not(opt_a))
result_a = solver.check()
solver.pop()

# Option B: G and H are both selected
opt_b = And(G, H)
solver.push()
solver.add(Not(opt_b))
result_b = solver.check()
solver.pop()

# Option C: H and P are both selected
opt_c = And(H, P)
solver.push()
solver.add(Not(opt_c))
result_c = solver.check()
solver.pop()

# Option D: F, G, and H are all selected
opt_d = And(F, G, H)
solver.push()
solver.add(Not(opt_d))
result_d = solver.check()
solver.pop()

# Option E: P, Q, and R are all selected
opt_e = And(P, Q, R)
solver.push()
solver.add(Not(opt_e))
result_e = solver.check()
solver.pop()

# Now determine which options MUST be true
# An option MUST be true if its negation leads to unsat
found_options = []
if result_a == unsat:
    found_options.append("A")
if result_b == unsat:
    found_options.append("B")
if result_c == unsat:
    found_options.append("C")
if result_d == unsat:
    found_options.append("D")
if result_e == unsat:
    found_options.append("E")

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")