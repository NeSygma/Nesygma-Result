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
solver.add(Xor(P < S, T < S))

# Hypothesis: Percussionist before saxophonist
solver.add(P < S)

# For "must be true" questions: check if negation is UNSAT
# An option "must be true" iff its negation is unsatisfiable
options = {
    "A": P == 1,
    "B": P == 2,
    "C": V < S,
    "D": P < T,
    "E": S < K,
}

found_options = []
for letter, claim in options.items():
    solver.push()
    solver.add(Not(claim))
    if solver.check() == unsat:
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