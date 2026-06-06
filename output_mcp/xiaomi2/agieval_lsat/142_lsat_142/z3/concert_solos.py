from z3 import *

solver = Solver()

# Each member's solo position (1-6, all distinct)
G = Int('G')  # Guitarist
K = Int('K')  # Keyboard
P = Int('P')  # Percussionist
S = Int('S')  # Saxophonist
T = Int('T')  # Trumpeter
V = Int('V')  # Violinist

members = [G, K, P, S, T, V]

# All positions are 1-6 and distinct
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: Guitarist does NOT perform the 4th solo
solver.add(G != 4)

# Constraint 2: Percussionist before keyboard player
solver.add(P < K)

# Constraint 3: Keyboard after violinist AND keyboard before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist after either percussionist or trumpeter, but not both
# (S > P) XOR (S > T)
solver.add(Xor(S > P, S > T))

# Now test each option: which CANNOT be in position 3?
# We check if each member CAN be in position 3.
# The one that CANNOT is the answer.

options = [
    ("A", G),  # guitarist
    ("B", K),  # keyboard player
    ("C", S),  # saxophonist
    ("D", T),  # trumpeter
    ("E", V),  # violinist
]

found_options = []
for letter, member in options:
    solver.push()
    solver.add(member == 3)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The question asks who CANNOT perform the 3rd solo.
# So the answer is the one NOT in found_options.
cannot_options = [letter for letter, _ in options if letter not in found_options]

print(f"CAN be 3rd: {found_options}")
print(f"CANNOT be 3rd: {cannot_options}")

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be 3rd {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be 3rd")