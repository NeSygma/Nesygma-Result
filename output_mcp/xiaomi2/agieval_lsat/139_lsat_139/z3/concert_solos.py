from z3 import *

solver = Solver()

# Members: G=guitarist, K=keyboard, P=percussionist, S=saxophonist, T=trumpeter, V=violinist
# Each performs in a unique position 1-6
G, K, P, S, T, V = Ints('G K P S T V')
members = [G, K, P, S, T, V]

# All positions 1-6, all distinct
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: Guitarist does not perform the fourth solo
solver.add(G != 4)

# Constraint 2: Percussionist before keyboard player
solver.add(P < K)

# Constraint 3: Violinist before keyboard player before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist after exactly one of percussionist or trumpeter (XOR)
# (S > P AND NOT (S > T)) OR (NOT (S > P) AND S > T)
solver.add(Or(
    And(S > P, Not(S > T)),
    And(Not(S > P), S > T)
))

# Define each option as a complete ordering (position 1 through 6)
# Option A: violinist, percussionist, saxophonist, guitarist, trumpeter, keyboard
opt_a = And(V == 1, P == 2, S == 3, G == 4, T == 5, K == 6)
# Option B: percussionist, violinist, keyboard, trumpeter, saxophonist, guitarist
opt_b = And(P == 1, V == 2, K == 3, T == 4, S == 5, G == 6)
# Option C: violinist, trumpeter, saxophonist, percussionist, keyboard, guitarist
opt_c = And(V == 1, T == 2, S == 3, P == 4, K == 5, G == 6)
# Option D: keyboard, trumpeter, violinist, saxophonist, guitarist, percussionist
opt_d = And(K == 1, T == 2, V == 3, S == 4, G == 5, P == 6)
# Option E: guitarist, violinist, keyboard, percussionist, saxophonist, trumpeter
opt_e = And(G == 1, V == 2, K == 3, P == 4, S == 5, T == 6)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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