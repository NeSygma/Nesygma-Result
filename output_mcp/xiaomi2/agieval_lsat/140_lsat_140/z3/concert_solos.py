from z3 import *

solver = Solver()

# Each member has a solo position 1-6, all distinct
G = Int('G')  # Guitarist
K = Int('K')  # Keyboard player
P = Int('P')  # Percussionist
S = Int('S')  # Saxophonist
T = Int('T')  # Trumpeter
V = Int('V')  # Violinist

members = [G, K, P, S, T, V]

# All positions 1-6, all distinct
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: Guitarist does not perform the fourth solo
solver.add(G != 4)

# Constraint 2: Percussionist before keyboard player
solver.add(P < K)

# Constraint 3: Keyboard player after violinist and before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist after exactly one of {P, T} (XOR)
# (P < S) XOR (T < S)
solver.add(Xor(P < S, T < S))

# Hypothesis: Percussionist before saxophonist
solver.add(P < S)

# From constraint 4 XOR + hypothesis (P < S):
# So NOT (T < S), meaning S < T
# Let's verify this is implied, but also keep original constraints

# Now test each answer choice
# (A) P == 1
# (B) P == 2
# (C) V < S
# (D) P < T
# (E) S < K

# For "must be true", we check if the negation is UNSAT
# i.e., if adding the negation makes the problem unsatisfiable

options = {
    "A": P == 1,
    "B": P == 2,
    "C": V < S,
    "D": P < T,
    "E": S < K,
}

must_be_true = []

for letter, claim in options.items():
    solver.push()
    solver.add(Not(claim))
    result = solver.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is unsat)")
    else:
        m = solver.model()
        print(f"Option {letter}: NOT necessarily true (counterexample: G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]})")
    solver.pop()

print()
print(f"Options that must be true: {must_be_true}")

# Now use the required skeleton for multiple choice
found_options = []
for letter, claim in options.items():
    solver.push()
    solver.add(claim)
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