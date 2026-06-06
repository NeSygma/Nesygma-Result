from z3 import *

solver = Solver()

# Declare variables for positions (1..7)
p = Int('Peters')
q = Int('Quinn')
r = Int('Rovero')
s = Int('Stanton')
t = Int('Tao')
v = Int('Villas')
w = Int('White')

# Base constraints
solver.add(p == 4)          # Peters fourth
solver.add(t == 2)          # Tao second (given)
solver.add(q < r)           # Quinn earlier than Rovero
solver.add(v + 1 == w)      # Villas immediately before White
# Stanton not adjacent to Tao
solver.add(s != t - 1)
solver.add(s != t + 1)

# All positions distinct
solver.add(Distinct([p, q, r, s, t, v, w]))

# Domain bounds (1..7)
solver.add(And(p >= 1, p <= 7))
solver.add(And(q >= 1, q <= 7))
solver.add(And(r >= 1, r <= 7))
solver.add(And(s >= 1, s <= 7))
solver.add(And(t >= 1, t <= 7))
solver.add(And(v >= 1, v <= 7))
solver.add(And(w >= 1, w <= 7))

# Options
opt_a = (q == 3)
opt_b = (r == 5)
opt_c = (s == 6)
opt_d = (v == 6)
opt_e = (w == 3)

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