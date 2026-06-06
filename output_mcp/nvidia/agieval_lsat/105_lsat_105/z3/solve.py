from z3 import *

solver = Solver()

# Declare variables
iw = Int('iw')
iv = Int('iv')
sw = Int('sw')
sv = Int('sv')
tvw = Int('tvw')
tvv = Int('tvv')

# Domain constraints: 1 <= var <= 3
for var in [iw, iv, sw, sv, tvw, tvv]:
    solver.add(var >= 1, var <= 3)

# Website <= voicemail for each client
solver.add(iw <= iv)
solver.add(sw <= sv)
solver.add(tvw <= tvv)

# Image's voicemail < other clients' voicemail
solver.add(iv < sv)
solver.add(iv < tvv)

# Solide's website < Truvest's website
solver.add(sw < tvw)

# Given: Image's website target is 2 days
solver.add(iw == 2)

# Option constraints
opt_a = (iv == 2)
opt_b = (sw == 2)
opt_c = (sv == 2)
opt_d = (tvw == 2)
opt_e = (tvv == 2)

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