from z3 import *

solver = Solver()

# Variables: 1, 2, or 3 days
image_w = Int('image_w')
image_v = Int('image_v')
solide_w = Int('solide_w')
solide_v = Int('solide_v')
truvest_w = Int('truvest_w')
truvest_v = Int('truvest_v')

# Domains
for var in [image_w, image_v, solide_w, solide_v, truvest_w, truvest_v]:
    solver.add(1 <= var, var <= 3)

# Constraint 1: website target <= voicemail target for each client
solver.add(image_w <= image_v)
solver.add(solide_w <= solide_v)
solver.add(truvest_w <= truvest_v)

# Constraint 2: Image's voicemail target < other clients' voicemail targets
solver.add(image_v < solide_v)
solver.add(image_v < truvest_v)

# Constraint 3: Solide's website target < Truvest's website target
solver.add(solide_w < truvest_w)

# Given: Image's website target is 2 days
solver.add(image_w == 2)

# Now evaluate each option: which variable MUST be 2?
# We test: add variable != 2, see if unsat (meaning it must be 2).

options = [
    ("A", image_v, "Image's voicemail target"),
    ("B", solide_w, "Solide's website target"),
    ("C", solide_v, "Solide's voicemail target"),
    ("D", truvest_w, "Truvest's website target"),
    ("E", truvest_v, "Truvest's voicemail target")
]

found_options = []
for letter, var, desc in options:
    solver.push()
    solver.add(var != 2)
    result = solver.check()
    if result == unsat:
        # It's impossible for var to not be 2, so var must be 2
        found_options.append(letter)
    solver.pop()

print("found_options:", found_options)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")