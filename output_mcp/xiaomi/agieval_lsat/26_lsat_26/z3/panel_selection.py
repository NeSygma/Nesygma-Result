from z3 import *

solver = Solver()

# Define Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

botanists = [F, G, H]
chemists = [K, L, M]
zoologists = [P, Q, R]
all_scientists = botanists + chemists + zoologists

# Panel must have exactly 5 members
solver.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)

# At least one of each type
solver.add(Or(botanists))
solver.add(Or(chemists))
solver.add(Or(zoologists))

# If more than one botanist selected, at most one zoologist selected
# More than one botanist: Sum(botanists) >= 2
# At most one zoologist: Sum(zoologists) <= 1
solver.add(Implies(Sum([If(s, 1, 0) for s in botanists]) >= 2, Sum([If(s, 1, 0) for s in zoologists]) <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: M is the only chemist selected
solver.add(M == True)
solver.add(K == False)
solver.add(L == False)

# Now check each answer choice
found_options = []

# (A) F and G are both selected
opt_a = And(F, G)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) G and H are both selected
opt_b = And(G, H)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) H and P are both selected
opt_c = And(H, P)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) F, G, and H are all selected
opt_d = And(F, G, H)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) P, Q, and R are all selected
opt_e = And(P, Q, R)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Now check which MUST be true (i.e., is entailed by the constraints)
# An option must be true if its negation is unsatisfiable
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")