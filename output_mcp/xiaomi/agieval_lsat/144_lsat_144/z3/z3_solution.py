from z3 import *

solver = Solver()

# Four historians: Farley, Garcia, Holden, Jiang
# Four topics: lithographs, oil paintings, sculptures, watercolors
# Each historian gives exactly one lecture on a different topic
# Positions are 1 (first) through 4 (fourth)

# Position of each historian
Farley = Int('Farley')
Garcia = Int('Garcia')
Holden = Int('Holden')
Jiang = Int('Jiang')

# Position of each topic
lithographs = Int('lithographs')
oil_paintings = Int('oil_paintings')
sculptures = Int('sculptures')
watercolors = Int('watercolors')

# All positions are between 1 and 4
for v in [Farley, Garcia, Holden, Jiang, lithographs, oil_paintings, sculptures, watercolors]:
    solver.add(v >= 1, v <= 4)

# All historians have distinct positions
solver.add(Distinct(Farley, Garcia, Holden, Jiang))

# All topics have distinct positions
solver.add(Distinct(lithographs, oil_paintings, sculptures, watercolors))

# Each historian's position equals the position of their topic
# (This is implicit - each historian gives exactly one topic, so the historian's position IS the topic's position)

# Constraint 1: oil paintings and watercolors must both be earlier than lithographs
solver.add(oil_paintings < lithographs)
solver.add(watercolors < lithographs)

# Constraint 2: Farley's lecture must be earlier than oil paintings lecture
solver.add(Farley < oil_paintings)

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(Holden < Garcia)
solver.add(Holden < Jiang)

# Now define each option as constraints
# Option A: Farley: sculptures; Holden: lithographs; Garcia: oil paintings; Jiang: watercolors
opt_a = And(
    Farley == sculptures,
    Holden == lithographs,
    Garcia == oil_paintings,
    Jiang == watercolors
)

# Option B: Farley: watercolors; Jiang: oil paintings; Holden: sculptures; Garcia: lithographs
opt_b = And(
    Farley == watercolors,
    Jiang == oil_paintings,
    Holden == sculptures,
    Garcia == lithographs
)

# Option C: Garcia: sculptures; Farley: watercolors; Holden: oil paintings; Jiang: lithographs
opt_c = And(
    Garcia == sculptures,
    Farley == watercolors,
    Holden == oil_paintings,
    Jiang == lithographs
)

# Option D: Holden: oil paintings; Jiang: watercolors; Farley: lithographs; Garcia: sculptures
opt_d = And(
    Holden == oil_paintings,
    Jiang == watercolors,
    Farley == lithographs,
    Garcia == sculptures
)

# Option E: Holden: sculptures; Farley: watercolors; Jiang: oil paintings; Garcia: lithographs
opt_e = And(
    Holden == sculptures,
    Farley == watercolors,
    Jiang == oil_paintings,
    Garcia == lithographs
)

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