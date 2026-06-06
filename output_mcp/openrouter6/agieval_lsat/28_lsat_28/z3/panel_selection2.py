from z3 import *

# Define boolean variables for each scientist
F, G, H, K, L, M, P, Q, R = Bools('F G H K L M P Q R')

solver = Solver()

# Base constraints
# Exactly 5 scientists selected
solver.add(Sum([F, G, H, K, L, M, P, Q, R]) == 5)

# At least one of each type
solver.add(Or(F, G, H))  # botanists
solver.add(Or(K, L, M))  # chemists
solver.add(Or(P, Q, R))  # zoologists

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: P is the only zoologist selected
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Since R is false, M must be false (from condition 5), but we enforce it explicitly
solver.add(M == False)

# Condition about botanists and zoologists: if more than one botanist, at most one zoologist.
# Since zoologists are exactly one (P), this is automatically satisfied, but we encode for completeness.
botanists_count = Sum([F, G, H])
zoologists_count = Sum([P, Q, R])  # will be 1
solver.add(Implies(botanists_count >= 2, zoologists_count <= 1))

# Now evaluate each answer choice by checking the negation of the implication
found_options = []

# Option A: "If K is selected, G cannot be selected." => K => Not(G)
# Negation: K and G
solver.push()
solver.add(And(K, G))
if solver.check() == unsat:  # Changed from sat to unsat
    found_options.append("A")
solver.pop()

# Option B: "If L is selected, F cannot be selected." => L => Not(F)
# Negation: L and F
solver.push()
solver.add(And(L, F))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: "If exactly one chemist is selected, it must be K." => (chemists_count == 1) => K
# Negation: chemists_count == 1 and Not(K)
# Chemists are K, L, M; M is false, so chemists_count == 1 means (K + L) == 1
solver.push()
solver.add(Sum([K, L]) == 1)
solver.add(Not(K))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: "If exactly two chemists are selected, F cannot be selected." => (chemists_count == 2) => Not(F)
# Negation: chemists_count == 2 and F
# Exactly two chemists means K and L both true (since M is false)
solver.push()
solver.add(And(K, L))
solver.add(F)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: "If exactly two chemists are selected, G cannot be selected." => (chemists_count == 2) => Not(G)
# Negation: chemists_count == 2 and G
solver.push()
solver.add(And(K, L))
solver.add(G)
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")