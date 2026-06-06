from z3 import *

# Declare symbolic variables for each client's website and voicemail targets
# Image
Image_W = Int('Image_W')
Image_V = Int('Image_V')

# Solide
Solide_W = Int('Solide_W')
Solide_V = Int('Solide_V')

# Truvest
Truvest_W = Int('Truvest_W')
Truvest_V = Int('Truvest_V')

# Base constraints
solver = Solver()

# 1. None of the clients can have a website target that is longer than its voicemail target
solver.add(Image_W <= Image_V)
solver.add(Solide_W <= Solide_V)
solver.add(Truvest_W <= Truvest_V)

# 2. Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(Image_V < Solide_V)
solver.add(Image_V < Truvest_V)

# 3. Solide's website target must be shorter than Truvest's website target
solver.add(Solide_W < Truvest_W)

# 4. None of the clients has a website target of 2 days
solver.add(Image_W != 2)
solver.add(Solide_W != 2)
solver.add(Truvest_W != 2)

# Domain constraints: targets are 1, 2, or 3 days
solver.add(Image_W >= 1, Image_W <= 3)
solver.add(Image_V >= 1, Image_V <= 3)
solver.add(Solide_W >= 1, Solide_W <= 3)
solver.add(Solide_V >= 1, Solide_V <= 3)
solver.add(Truvest_W >= 1, Truvest_W <= 3)
solver.add(Truvest_V >= 1, Truvest_V <= 3)

# Evaluate each option
found_options = []

# Option A: Image's website target is shorter than Solide's
solver.push()
solver.add(Image_W < Solide_W)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Solide's website target is shorter than Image's
solver.push()
solver.add(Solide_W < Image_W)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Solide's voicemail target is shorter than Truvest's
solver.push()
solver.add(Solide_V < Truvest_V)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's website target is shorter than Image's
solver.push()
solver.add(Truvest_W < Image_W)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's voicemail target is shorter than Solide's
solver.push()
solver.add(Truvest_V < Solide_V)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")