from z3 import *

solver = Solver()
# Variables: Image website (Iw), Image voicemail (Iv), Solide website (Sw), Solide voicemail (Sv), Truvest website (Tw), Truvest voicemail (Tv)
Iw, Iv, Sw, Sv, Tw, Tv = Ints('Iw Iv Sw Sv Tw Tv')
vars = [Iw, Iv, Sw, Sv, Tw, Tv]
# Domain constraints: each target is 1,2, or 3 days
for v in vars:
    solver.add(And(v >= 1, v <= 3))
# Base constraints
# 1. website <= voicemail for each client
solver.add(Iw <= Iv)
solver.add(Sw <= Sv)
solver.add(Tw <= Tv)
# 2. Image's voicemail shorter than other clients' voicemail targets
solver.add(Iv < Sv)
solver.add(Iv < Tv)
# 3. Solide's website shorter than Truvest's website
solver.add(Sw < Tw)
# Additional condition from the question premise
solver.add(Sv < Tw)

# Define option constraints
opt_a = Iw == 2
opt_b = Iv == 2
opt_c = Sw == 2
opt_d = Tv == 2
opt_e = Tw == 2

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