from z3 import *

# Scientists: botanists F, G, H; chemists K, L, M; zoologists P, Q, R
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# If more than one botanist, then at most one zoologist
count_botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
count_zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(count_botanists >= 2, count_zoologists <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Question condition: P is the only zoologist selected
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Let's first check what models exist under these constraints
print("Checking base constraints with P only zoologist...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("SAT - example model:")
    for var in [F, G, H, K, L, M, P, Q, R]:
        print(f"  {var} = {m[var]}")
    print(f"  count_botanists = {m.eval(count_botanists)}")
    print(f"  count_chemists = {m.eval(Sum([If(K,1,0), If(L,1,0), If(M,1,0)]))}")
else:
    print("UNSAT - no model exists with P as only zoologist")
    # Let's check if the constraints are contradictory
    # Maybe M cannot be selected because M requires P and R, but R is False
    # So M must be False
    print("Checking: M must be False because M => P and R, but R=False")