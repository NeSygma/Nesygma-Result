from z3 import *

# Six members: guitarist, keyboard player, percussionist, saxophonist, trumpeter, violinist
# Each performs exactly one solo (positions 1-6, first to last)
# We'll use Int variables for each member's solo position (1-indexed)

g, k, p, s, t, v = Ints('g k p s t v')
members = [g, k, p, s, t, v]
names = ['guitarist', 'keyboard', 'percussionist', 'saxophonist', 'trumpeter', 'violinist']

solver = Solver()

# Domain: each position is 1 through 6
for m in members:
    solver.add(m >= 1, m <= 6)

# All distinct positions
solver.add(Distinct(members))

# Constraints:
# 1. The guitarist does not perform the fourth solo.
solver.add(g != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(p < k)

# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(v < k)
solver.add(k < g)

# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# "after either ... or ... but not both" means:
# (s > p) XOR (s > t)
# XOR: (s > p) != (s > t)
solver.add(If(s > p, True, False) != If(s > t, True, False))

# Now evaluate each option
# Each option is a specific ordering from first (position 1) to last (position 6)
# We'll encode each option as constraints on the positions

# Option A: violinist, percussionist, saxophonist, guitarist, trumpeter, keyboard player
# Position 1: violinist, Position 2: percussionist, Position 3: saxophonist, Position 4: guitarist, Position 5: trumpeter, Position 6: keyboard player
opt_a_constr = And(v == 1, p == 2, s == 3, g == 4, t == 5, k == 6)

# Option B: percussionist, violinist, keyboard player, trumpeter, saxophonist, guitarist
opt_b_constr = And(p == 1, v == 2, k == 3, t == 4, s == 5, g == 6)

# Option C: violinist, trumpeter, saxophonist, percussionist, keyboard player, guitarist
opt_c_constr = And(v == 1, t == 2, s == 3, p == 4, k == 5, g == 6)

# Option D: keyboard player, trumpeter, violinist, saxophonist, guitarist, percussionist
opt_d_constr = And(k == 1, t == 2, v == 3, s == 4, g == 5, p == 6)

# Option E: guitarist, violinist, keyboard player, percussionist, saxophonist, trumpeter
opt_e_constr = And(g == 1, v == 2, k == 3, p == 4, s == 5, t == 6)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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