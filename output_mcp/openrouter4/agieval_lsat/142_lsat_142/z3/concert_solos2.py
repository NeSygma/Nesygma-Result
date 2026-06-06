from z3 import *

solver = Solver()

# Declare 6 members with position variables (1 to 6)
G, K, P, S, T, V = Ints('G K P S T V')
members = [G, K, P, S, T, V]

# Each position is between 1 and 6
for m in members:
    solver.add(m >= 1, m <= 6)

# All positions distinct
solver.add(Distinct(members))

# Constraint 1: Guitarist does not perform the fourth solo
solver.add(G != 4)

# Constraint 2: Percussionist before keyboard player
solver.add(P < K)

# Constraint 3: Keyboard player after violinist and before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist after either percussionist or trumpeter, but not both.
solver.add(If(P < S, 1, 0) + If(T < S, 1, 0) == 1)

# Test each option for being UNSAT (CANNOT be third)
# We'll find which members CAN be in position 3
pos3_options = []

for letter, name, constr in [("A", "guitarist", G == 3), ("B", "keyboard", K == 3), 
                              ("C", "saxophonist", S == 3), ("D", "trumpeter", T == 3), 
                              ("E", "violinist", V == 3)]:
    s = Solver()
    # Re-add all constraints
    for m in members:
        s.add(m >= 1, m <= 6)
    s.add(Distinct(members))
    s.add(G != 4)
    s.add(P < K)
    s.add(V < K)
    s.add(K < G)
    s.add(If(P < S, 1, 0) + If(T < S, 1, 0) == 1)
    # Add this option
    s.add(constr)
    res = s.check()
    print(f"Option {letter} ({name} at pos 3): {res}")
    if res == sat:
        pos3_options.append(letter)
        m = s.model()
        print(f"  Model: G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]}")

# The one that CANNOT be third is the one not in pos3_options
cannot_options = [l for l in ["A","B","C","D","E"] if l not in pos3_options]
print(f"\nOptions that CAN be third: {pos3_options}")
print(f"Options that CANNOT be third: {cannot_options}")

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) == 0:
    print("STATUS: unsat")
    print("Refine: All options can be third")
else:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be third: {cannot_options}")