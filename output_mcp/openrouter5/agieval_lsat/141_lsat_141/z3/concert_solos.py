from z3 import *

# Six members: guitarist, keyboard player, percussionist, saxophonist, trumpeter, violinist
# Each performs exactly one solo (positions 1 through 6)
# We'll use Int variables for each member's solo position (1-indexed)

g, k, p, s, t, v = Ints('g k p s t v')
members = [g, k, p, s, t, v]
names = ['guitarist', 'keyboard', 'percussionist', 'saxophonist', 'trumpeter', 'violinist']

solver = Solver()

# Domain: each position is between 1 and 6
for m in members:
    solver.add(m >= 1, m <= 6)

# All distinct (each member performs exactly one solo)
solver.add(Distinct(members))

# 1. The guitarist does not perform the fourth solo.
solver.add(g != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(p < k)

# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(v < k)
solver.add(k < g)

# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# "after either the percussionist does or the trumpeter does, but not both"
# Means: (s > p) XOR (s > t)
# XOR: (s > p) != (s > t)
solver.add(If(s > p, True, False) != If(s > t, True, False))

# Now evaluate each option
# Option A: The keyboard player performs the first solo.
opt_a = (k == 1)

# Option B: The guitarist performs the second solo.
opt_b = (g == 2)

# Option C: The guitarist performs a solo at some time before the saxophonist does.
opt_c = (g < s)

# Option D: The guitarist performs a solo at some time before the percussionist does.
opt_d = (g < p)

# Option E: The keyboard player performs a solo at some time before the saxophonist does.
opt_e = (k < s)

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