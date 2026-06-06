from z3 import *

# Declare Bool variables for each scientist
F = Bool('F')
G = Bool('G')
H = Bool('H')
K = Bool('K')
L = Bool('L')
M = Bool('M')
P = Bool('P')
Q = Bool('Q')
R = Bool('R')

vars = [F,G,H,K,L,M,P,Q,R]

solver = Solver()

# Helper to count selected of a list
def count_selected(lst):
    return Sum([If(v, 1, 0) for v in lst])

# Base constraints
# Exactly 5 scientists selected
solver.add(count_selected(vars) == 5)
# At least one of each type
solver.add(count_selected([F,G,H]) >= 1)   # botanists
solver.add(count_selected([K,L,M]) >= 1)   # chemists
solver.add(count_selected([P,Q,R]) >= 1)   # zoologists
# If more than one botanist, then at most one zoologist
solver.add(Implies(count_selected([F,G,H]) > 1, count_selected([P,Q,R]) <= 1))
# F and K cannot both be selected
solver.add(Not(And(F, K)))
# K and M cannot both be selected
solver.add(Not(And(K, M)))
# If M selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Fixed four scientists: F, L, Q, R are selected
solver.add(F == True)
solver.add(L == True)
solver.add(Q == True)
solver.add(R == True)

# Define option constraints
options = []
# Option A: G
opt_a = And(G == True,
            H == False,
            K == False,
            M == False,
            P == False)
options.append(("A", opt_a))
# Option B: H
opt_b = And(H == True,
            G == False,
            K == False,
            M == False,
            P == False)
options.append(("B", opt_b))
# Option C: K
opt_c = And(K == True,
            G == False,
            H == False,
            M == False,
            P == False)
options.append(("C", opt_c))
# Option D: M
opt_d = And(M == True,
            G == False,
            H == False,
            K == False,
            P == False)
options.append(("D", opt_d))
# Option E: P
opt_e = And(P == True,
            G == False,
            H == False,
            K == False,
            M == False)
options.append(("E", opt_e))

found_options = []
for letter, constr in options:
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