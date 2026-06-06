from z3 import *

solver = Solver()

# Variables: position of each solo (1=first, 6=last)
g, k, p, s, t, v = Ints('g k p s t v')

# Domain: each position is between 1 and 6, all distinct
members = [g, k, p, s, t, v]
for member in members:
    solver.add(member >= 1, member <= 6)
solver.add(Distinct(members))

# Constraint 1: guitarist does not perform the fourth solo
solver.add(g != 4)

# Constraint 2: percussionist before keyboard player
solver.add(p < k)

# Constraint 3: keyboard player after violinist and before guitarist
solver.add(v < k)
solver.add(k < g)

# Constraint 4: saxophonist after either percussionist OR trumpeter, but NOT both
# Exactly one of {s > p, s > t} is true
solver.add(Or(
    And(s > p, Not(s > t)),
    And(Not(s > p), s > t)
))

# Now evaluate each option
# Each option gives a full ordering, so we assert the position of each member

# Option A: violinist(1), percussionist(2), saxophonist(3), guitarist(4), trumpeter(5), keyboard player(6)
opt_a_constr = And(v == 1, p == 2, s == 3, g == 4, t == 5, k == 6)

# Option B: percussionist(1), violinist(2), keyboard player(3), trumpeter(4), saxophonist(5), guitarist(6)
opt_b_constr = And(p == 1, v == 2, k == 3, t == 4, s == 5, g == 6)

# Option C: violinist(1), trumpeter(2), saxophonist(3), percussionist(4), keyboard player(5), guitarist(6)
opt_c_constr = And(v == 1, t == 2, s == 3, p == 4, k == 5, g == 6)

# Option D: keyboard player(1), trumpeter(2), violinist(3), saxophonist(4), guitarist(5), percussionist(6)
opt_d_constr = And(k == 1, t == 2, v == 3, s == 4, g == 5, p == 6)

# Option E: guitarist(1), violinist(2), keyboard player(3), percussionist(4), saxophonist(5), trumpeter(6)
opt_e_constr = And(g == 1, v == 2, k == 3, p == 4, s == 5, t == 6)

options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    # print(f"Option {letter}: {result}")
    if result == sat:
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