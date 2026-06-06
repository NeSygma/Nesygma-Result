from z3 import *

# Declare variables for each client and channel
Image_web = Int('Image_web')
Image_voice = Int('Image_voice')
Solide_web = Int('Solide_web')
Solide_voice = Int('Solide_voice')
Truvest_web = Int('Truvest_web')
Truvest_voice = Int('Truvest_voice')

# Base constraints
solver = Solver()

# All targets are in {1, 2, 3}
solver.add(Image_web >= 1, Image_web <= 3)
solver.add(Image_voice >= 1, Image_voice <= 3)
solver.add(Solide_web >= 1, Solide_web <= 3)
solver.add(Solide_voice >= 1, Solide_voice <= 3)
solver.add(Truvest_web >= 1, Truvest_web <= 3)
solver.add(Truvest_voice >= 1, Truvest_voice <= 3)

# None of the clients can have a website target that is longer than its voicemail target
solver.add(Image_web <= Image_voice)
solver.add(Solide_web <= Solide_voice)
solver.add(Truvest_web <= Truvest_voice)

# Image's voicemail target must be shorter than the other clients' voicemail targets
solver.add(Image_voice < Solide_voice)
solver.add(Image_voice < Truvest_voice)

# Solide's website target must be shorter than Truvest's website target
solver.add(Solide_web < Truvest_web)

# None of the clients has a voicemail target of 3 days
solver.add(Image_voice != 3)
solver.add(Solide_voice != 3)
solver.add(Truvest_voice != 3)

# Check each option
found_options = []

# Option A: Image's website target is 1 day
solver.push()
solver.add(Image_web == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Solide's website target is 2 days
solver.push()
solver.add(Solide_web == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Solide's voicemail target is 2 days
solver.push()
solver.add(Solide_voice == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Truvest's website target is 2 days
solver.push()
solver.add(Truvest_web == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Truvest's voicemail target is 2 days
solver.push()
solver.add(Truvest_voice == 2)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")