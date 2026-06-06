from z3 import *

# Define variables
Iw, Iv = Ints('Iw Iv')  # Image website, voicemail
Sw, Sv = Ints('Sw Sv')  # Solide website, voicemail
Tw, Tv = Ints('Tw Tv')  # Truvest website, voicemail

solver = Solver()
# Domain constraints: each target is 1,2,3
vars = [Iw, Iv, Sw, Sv, Tw, Tv]
for v in vars:
    solver.add(And(v >= 1, v <= 3))

# Base constraints
# website <= voicemail for each client
solver.add(Iw <= Iv)
solver.add(Sw <= Sv)
solver.add(Tw <= Tv)
# Image voicemail shorter than others' voicemail
solver.add(Iv < Sv)
solver.add(Iv < Tv)
# Solide website shorter than Truvest website
solver.add(Sw < Tw)
# Additional condition: none of the voicemail targets is 3
solver.add(Iv != 3)
solver.add(Sv != 3)
solver.add(Tv != 3)

# Define option constraints (negations of the statements)
opt_a_constr = Iw != 1
opt_b_constr = Sw != 2
opt_c_constr = Sv != 2
opt_d_constr = Tw != 2
opt_e_constr = Tv != 2

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