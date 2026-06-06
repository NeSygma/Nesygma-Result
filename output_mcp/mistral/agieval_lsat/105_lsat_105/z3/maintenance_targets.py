from z3 import *

solver = Solver()

# Declare variables for each target
# Image
Image_W = Int('Image_W')
Image_V = Int('Image_V')

# Solide
Solide_W = Int('Solide_W')
Solide_V = Int('Solide_V')

# Truvest
Truvest_W = Int('Truvest_W')
Truvest_V = Int('Truvest_V')

# Domain constraints: each target is 1, 2, or 3
domain_constraints = [
    Or(Image_W == 1, Image_W == 2, Image_W == 3),
    Or(Image_V == 1, Image_V == 2, Image_V == 3),
    Or(Solide_W == 1, Solide_W == 2, Solide_W == 3),
    Or(Solide_V == 1, Solide_V == 2, Solide_V == 3),
    Or(Truvest_W == 1, Truvest_W == 2, Truvest_W == 3),
    Or(Truvest_V == 1, Truvest_V == 2, Truvest_V == 3),
]
solver.add(domain_constraints)

# Problem constraints
# 1. None of the clients can have a website target that is longer than its voicemail target
solver.add(Image_W <= Image_V)
solver.add(Solide_W <= Solide_V)
solver.add(Truvest_W <= Truvest_V)

# 2. Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(Image_V < Solide_V)
solver.add(Image_V < Truvest_V)

# 3. Solide's website target must be shorter than Truvest's website target
solver.add(Solide_W < Truvest_W)

# Given: Image's website target is 2 days
solver.add(Image_W == 2)

# Evaluate each option
found_options = []

# Option A: Image's voicemail target is 2 days
solver.push()
solver.add(Image_V == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Solide's website target is 2 days
solver.push()
solver.add(Solide_W == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Solide's voicemail target is 2 days
solver.push()
solver.add(Solide_V == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's website target is 2 days
solver.push()
solver.add(Truvest_W == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's voicemail target is 2 days
solver.push()
solver.add(Truvest_V == 2)
if solver.check() == sat:
    found_options.append("E")
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