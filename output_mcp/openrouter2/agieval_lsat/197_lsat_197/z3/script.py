from z3 import *
solver = Solver()

# Variables
h = Int('h')
l = Int('l')
m = Int('m')
s = Int('s')
t = Int('t')
v = Int('v')

# Domain constraints: days 1-6
for var in [h,l,m,s,t,v]:
    solver.add(var >= 1, var <= 6)

# Distinct
solver.add(Distinct([h,l,m,s,t,v]))

# sundial not on June 1
solver.add(s != 1)

# If harmonica before lamp then mirror before lamp
solver.add(Implies(h < l, m < l))

# sundial before mirror and vase
solver.add(s < m)
solver.add(s < v)

# table before harmonica or before vase, but not both
solver.add(Xor(t < h, t < v))

# Option constraints
opt_a_constr = And(t == 2, l == 3)
opt_b_constr = And(s == 2, v == 3)
opt_c_constr = And(m == 3, s == 4)
opt_d_constr = And(v == 4, s == 5)
opt_e_constr = And(s == 4, t == 5)

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