from z3 import *

solver = Solver()

# Variables
G = Int('G')
K = Int('K')
P = Int('P')
S = Int('S')
T = Int('T')
V = Int('V')

# Distinct and domain
solver.add(Distinct([G, K, P, S, T, V]))
solver.add(G >= 1, G <= 6)
solver.add(K >= 1, K <= 6)
solver.add(P >= 1, P <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)

# Constraints
solver.add(G != 4)
solver.add(P < K)
solver.add(V < K)
solver.add(K < G)
solver.add(Xor(S > P, S > T))

# Check
result = solver.check()
print("Result:", result)
if result == sat:
    m = solver.model()
    print("Model:")
    print("G =", m[G])
    print("K =", m[K])
    print("P =", m[P])
    print("S =", m[S])
    print("T =", m[T])
    print("V =", m[V])