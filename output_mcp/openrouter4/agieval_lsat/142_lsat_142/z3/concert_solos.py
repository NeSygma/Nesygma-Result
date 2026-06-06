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
# (P < S) XOR (T < S) means exactly one of P < S, T < S is true
solver.add(If(P < S, 1, 0) + If(T < S, 1, 0) == 1)

# Now test each option for being the third solo (position = 3)
found_options = []

for letter, constr in [("A", G == 3), ("B", K == 3), ("C", S == 3), ("D", T == 3), ("E", V == 3)]:
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