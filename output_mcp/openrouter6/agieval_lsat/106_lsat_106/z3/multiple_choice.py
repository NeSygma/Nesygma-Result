from z3 import *

solver = Solver()

# Declare variables
Image_W, Image_V = Ints('Image_W Image_V')
Solide_W, Solide_V = Ints('Solide_W Solide_V')
Truvest_W, Truvest_V = Ints('Truvest_W Truvest_V')

# Domain constraints: each target is 1, 2, or 3 days
solver.add(Image_W >= 1, Image_W <= 3)
solver.add(Image_V >= 1, Image_V <= 3)
solver.add(Solide_W >= 1, Solide_W <= 3)
solver.add(Solide_V >= 1, Solide_V <= 3)
solver.add(Truvest_W >= 1, Truvest_W <= 3)
solver.add(Truvest_V >= 1, Truvest_V <= 3)

# Condition 1: website target <= voicemail target for each client
solver.add(Image_W <= Image_V)
solver.add(Solide_W <= Solide_V)
solver.add(Truvest_W <= Truvest_V)

# Condition 2: Image's voicemail target is shorter than the other clients' voicemail targets
solver.add(Image_V < Solide_V)
solver.add(Image_V < Truvest_V)

# Condition 3: Solide's website target is shorter than Truvest's website target
solver.add(Solide_W < Truvest_W)

# Additional condition: Solide's voicemail target is shorter than Truvest's website target
solver.add(Solide_V < Truvest_W)

# Define options
opt_a_constr = (Image_W == 2)
opt_b_constr = (Image_V == 2)
opt_c_constr = (Solide_W == 2)
opt_d_constr = (Truvest_V == 2)
opt_e_constr = (Truvest_W == 2)

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