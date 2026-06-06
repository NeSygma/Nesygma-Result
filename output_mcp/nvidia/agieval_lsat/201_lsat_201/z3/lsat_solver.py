from z3 import *

solver = Solver()

# Declare variables
h = Int('h')  # harmonica day
l = Int('l')  # lamp day
m = Int('m')  # mirror day
s = Int('s')  # sundial day
t = Int('t')  # table day
v = Int('v')  # vase day

# Domain constraints
for var in (h, l, m, s, t, v):
    solver.add(var >= 1, var <= 6)

# All different
solver.add(Distinct([h, l, m, s, t, v]))

# Base constraints
solver.add(s != 1)          # sundial not on June 1
solver.add(s < m)           # sundial earlier than mirror
solver.add(s < v)           # sundial earlier than vase
solver.add(Implies(h < l, m < l))  # conditional
solver.add(Xor(t < h, t < v))      # table earlier than exactly one of harmonica or vase

# Option constraints
opt_a = (s == 5)
opt_b = (s == 4)
opt_c = And(l == 5, m == 6)
opt_d = And(t == 3, l == 4)
opt_e = And(h == 2, v == 3)

options = {
    "A": opt_a,
    "B": opt_b,
    "C": opt_c,
    "D": opt_d,
    "E": opt_e
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
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