from z3 import *

solver = Solver()

# Declare variables for positions
p = Int('Peters')
q = Int('Quinn')
r = Int('Rovero')
s = Int('Stanton')
t = Int('Tao')
v = Int('Villas')
w = Int('White')

# Base constraints
solver.add(p == 4)                     # Peters was recruited fourth
solver.add(v + 1 == w)                 # Villas immediately before White
solver.add(w + 1 == q)                 # White immediately before Quinn (extra condition)
solver.add(q < r)                      # Quinn earlier than Rovero
solver.add(Not(Or(s == t + 1, t == s + 1)))  # Stanton not adjacent to Tao
solver.add(Distinct([p, q, r, s, t, v, w]))  # All positions distinct
solver.add(And([x >= 1 for x in [p, q, r, s, t, v, w]]))  # positions >= 1
solver.add(And([x <= 7 for x in [p, q, r, s, t, v, w]]))  # positions <= 7

# Evaluate each option: which one must be sixth?
# We test if adding the constraint that the option's position is 6 is satisfiable.
found_options = []
for letter, constr in [
    ("A", q == 6),   # Quinn
    ("B", r == 6),   # Rovero
    ("C", s == 6),   # Stanton
    ("D", v == 6),   # Villas
    ("E", w == 6)    # White
]:
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