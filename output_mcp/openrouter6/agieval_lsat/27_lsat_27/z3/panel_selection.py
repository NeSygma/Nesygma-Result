from z3 import *
solver = Solver()

# Declare variables
F = Bool('F')
G = Bool('G')
H = Bool('H')
K = Bool('K')
L = Bool('L')
M = Bool('M')
P = Bool('P')
Q = Bool('Q')
R = Bool('R')

# Base constraints
# Exactly 5 selected
solver.add(Sum([F, G, H, K, L, M, P, Q, R]) == 5)

# At least one of each type
solver.add(Or(F, G, H))  # botanist
solver.add(Or(K, L, M))  # chemist
solver.add(Or(P, Q, R))  # zoologist

# Condition 2: If more than one botanist, then at most one zoologist
botanist_count = Sum([F, G, H])
zoologist_count = Sum([P, Q, R])
solver.add(Implies(botanist_count >= 2, zoologist_count <= 1))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Fixed selections: F, L, Q, R are selected
solver.add(F == True)
solver.add(L == True)
solver.add(Q == True)
solver.add(R == True)

# Now evaluate each option
found_options = []
for letter, constr in [("A", G == True), ("B", H == True), ("C", K == True), ("D", M == True), ("E", P == True)]:
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