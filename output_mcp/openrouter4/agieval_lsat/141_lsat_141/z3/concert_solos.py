from z3 import *

solver = Solver()

# Variables: positions 1-6 for each musician
g, k, p, s, t, v = Ints('g k p s t v')

# Domain: positions 1 to 6
members = [g, k, p, s, t, v]
for m in members:
    solver.add(m >= 1, m <= 6)

# All distinct positions
solver.add(Distinct(members))

# Constraint 1: guitarist not fourth
solver.add(g != 4)

# Constraint 2: percussionist before keyboard
solver.add(p < k)

# Constraint 3: violinist before keyboard before guitarist
solver.add(v < k)
solver.add(k < g)

# Constraint 4: saxophonist after exactly one of {percussionist, trumpeter}
# i.e., (s > p) XOR (s > t)
solver.add(Xor(s > p, s > t))

# Now evaluate each option
options = [
    ("A", k == 1),
    ("B", g == 2),
    ("C", g < s),
    ("D", g < p),
    ("E", k < s)
]

found_options = []
for letter, constr in options:
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