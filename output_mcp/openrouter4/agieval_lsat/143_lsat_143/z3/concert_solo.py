from z3 import *

solver = Solver()

# Variables: positions 1-6 for each musician
G, K, P, S, T, V = Ints('G K P S T V')

# Domain constraints: each position is 1-6
solver.add(And(1 <= G, G <= 6))
solver.add(And(1 <= K, K <= 6))
solver.add(And(1 <= P, P <= 6))
solver.add(And(1 <= S, S <= 6))
solver.add(And(1 <= T, T <= 6))
solver.add(And(1 <= V, V <= 6))

# All positions distinct
solver.add(Distinct(G, K, P, S, T, V))

# Constraint 1: Guitarist is not 4th
solver.add(G != 4)

# Constraint 2: Percussionist before keyboard player
solver.add(P < K)

# Constraint 3: Violinist before keyboard player, keyboard player before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist after exactly one of {percussionist, trumpeter}
# (S > P) XOR (S > T)
solver.add(If(S > P, 1, 0) + If(S > T, 1, 0) == 1)

# Additional condition: Violinist is 4th
solver.add(V == 4)

# Let's first check if the base constraints + V=4 are satisfiable
result = solver.check()
print(f"Base constraints + V=4: {result}")
if result == sat:
    m = solver.model()
    print(f"G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]}")

# Now evaluate each option
# Option A: P < V (P < 4)
# Option B: T < V (T < 4)
# Option C: T < G
# Option D: S < V (S < 4)
# Option E: T < S

# For each option, check if Not(option) is satisfiable with V=4
# If Not(option) is SAT, then option is NOT forced to be true (it could be false)

options = {
    "A": P < V,
    "B": T < V,
    "C": T < G,
    "D": S < V,
    "E": T < S
}

for letter, constr in options.items():
    test_solver = Solver()
    # Add all base constraints
    test_solver.add(And(1 <= G, G <= 6, 1 <= K, K <= 6, 1 <= P, P <= 6, 1 <= S, S <= 6, 1 <= T, T <= 6, 1 <= V, V <= 6))
    test_solver.add(Distinct(G, K, P, S, T, V))
    test_solver.add(G != 4)
    test_solver.add(P < K)
    test_solver.add(V < K)
    test_solver.add(K < G)
    test_solver.add(If(S > P, 1, 0) + If(S > T, 1, 0) == 1)
    test_solver.add(V == 4)
    # Add the negation of the option
    test_solver.add(Not(constr))
    
    res = test_solver.check()
    if res == sat:
        print(f"Option {letter}: Not({letter}) is SAT — option {letter} is NOT forced (could be false)")
        m = test_solver.model()
        print(f"  G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter}: Not({letter}) is UNSAT — option {letter} IS forced (must be true)")