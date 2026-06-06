from z3 import *

solver = Solver()

# Declare variables
g = Int('g')
k = Int('k')
p = Int('p')
sax = Int('sax')
t = Int('t')
v = Int('v')

# Base constraints
solver.add(g >= 1, g <= 6)
solver.add(k >= 1, k <= 6)
solver.add(p >= 1, p <= 6)
solver.add(sax >= 1, sax <= 6)
solver.add(t >= 1, t <= 6)
solver.add(v >= 1, v <= 6)
solver.add(Distinct([g, k, p, sax, t, v]))

# Additional constraints
solver.add(g != 4)
solver.add(p < k)
solver.add(v < k)
solver.add(k < g)
solver.add(Xor(sax > p, sax > t))

# Option constraints
opt_a_constr = (k == 1)
opt_b_constr = (g == 2)
opt_c_constr = (g < sax)
opt_d_constr = (g < p)
opt_e_constr = (k < sax)

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