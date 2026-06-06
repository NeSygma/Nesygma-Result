from z3 import *

solver = Solver()
# Variables for each target (days)
IW = Int('IW')   # Image website
IVo = Int('IVo') # Image voicemail
SW = Int('SW')   # Solide website
SVo = Int('SVo') # Solide voicemail
TW = Int('TW')   # Truvest website
TVo = Int('TVo') # Truvest voicemail

vars = [IW, IVo, SW, SVo, TW, TVo]
# Domain constraints: each target is 1,2,or3
for v in vars:
    solver.add(And(v >= 1, v <= 3))

# Base constraints
# website <= voicemail for each client
solver.add(IW <= IVo)
solver.add(SW <= SVo)
solver.add(TW <= TVo)
# Image voicemail shorter than other voicemails
solver.add(IVo < SVo)
solver.add(IVo < TVo)
# Solide website shorter than Truvest website
solver.add(SW < TW)
# Condition: Image website is 2 days
solver.add(IW == 2)

# Define option constraints (target == 2)
opt_a_constr = IVo == 2
opt_b_constr = SW == 2
opt_c_constr = SVo == 2
opt_d_constr = TW == 2
opt_e_constr = TVo == 2

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