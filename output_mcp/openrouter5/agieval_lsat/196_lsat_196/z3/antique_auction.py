from z3 import *

# Days: June 1st = 0, June 2nd = 1, ..., June 6th = 5
# Antiques: harmonica (H), lamp (L), mirror (M), sundial (S), table (T), vase (V)
# We'll assign each antique a day number (0-5), all distinct.

H, L, M, S, T, V = Ints('H L M S T V')
antiques = [H, L, M, S, T, V]
names = ['H', 'L', 'M', 'S', 'T', 'V']

solver = Solver()

# Domain: each antique gets a day from 0 to 5
for a in antiques:
    solver.add(a >= 0, a <= 5)

# All different days
solver.add(Distinct(antiques))

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(S != 0)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(H < L, M < L))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(S < M)
solver.add(S < V)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(Or(T < H, T < V))
solver.add(Not(And(T < H, T < V)))

# Now define each option as a specific ordering (list of antiques in order from day 0 to day 5)
# Option A: harmonica, table, sundial, lamp, vase, mirror
# Day 0: H, Day 1: T, Day 2: S, Day 3: L, Day 4: V, Day 5: M
opt_a = And(H == 0, T == 1, S == 2, L == 3, V == 4, M == 5)

# Option B: lamp, harmonica, sundial, mirror, vase, table
opt_b = And(L == 0, H == 1, S == 2, M == 3, V == 4, T == 5)

# Option C: harmonica, sundial, table, mirror, lamp, vase
opt_c = And(H == 0, S == 1, T == 2, M == 3, L == 4, V == 5)

# Option D: sundial, mirror, harmonica, table, vase, lamp
opt_d = And(S == 0, M == 1, H == 2, T == 3, V == 4, L == 5)

# Option E: vase, sundial, lamp, harmonica, table, mirror
opt_e = And(V == 0, S == 1, L == 2, H == 3, T == 4, M == 5)

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