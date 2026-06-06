from z3 import *

solver = Solver()

# Variables
wi = Int('wi')
vi = Int('vi')
ws = Int('ws')
vs = Int('vs')
wt = Int('wt')
vt = Int('vt')

# Domain: 1 to 3
for var in [wi, vi, ws, vs, wt, vt]:
    solver.add(var >= 1, var <= 3)

# Website <= voicemail for each client
solver.add(wi <= vi)
solver.add(ws <= vs)
solver.add(wt <= vt)

# Image's voicemail < others
solver.add(vi < vs)
solver.add(vi < vt)

# Solide's website < Truvest's website
solver.add(ws < wt)

# No website target is 2 days
solver.add(wi != 2)
solver.add(ws != 2)
solver.add(wt != 2)

# Test each option
found_options = []
# Option A: WI < WS
opt_a_constr = wi < ws
# Option B: WS < WI
opt_b_constr = ws < wi
# Option C: VS < VT
opt_c_constr = vs < vt
# Option D: WT < WI
opt_d_constr = wt < wi
# Option E: VT < VS
opt_e_constr = vt < vs

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