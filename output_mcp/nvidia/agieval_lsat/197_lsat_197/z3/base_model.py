from z3 import *

solver = Solver()

# Variables
H, L, M, S, T, V = Ints('H L M S T V')

# Base constraints
solver.add(Distinct([H, L, M, S, T, V]))
solver.add(H >= 0, H <= 5)
solver.add(L >= 0, L <= 5)
solver.add(M >= 0, M <= 5)
solver.add(S >= 0, S <= 5)
solver.add(T >= 0, T <= 5)
solver.add(V >= 0, V <= 5)

solver.add(S != 0)
solver.add(Implies(H < L, M < L))
solver.add(S < M)
solver.add(S < V)
solver.add(Xor(T < H, T < V))

result = solver.check()
print("Base result:", result)
if result == sat:
    m = solver.model()
    print("Model:")
    print("H =", m[H])
    print("L =", m[L])
    print("M =", m[M])
    print("S =", m[S])
    print("T =", m[T])
    print("V =", m[V])