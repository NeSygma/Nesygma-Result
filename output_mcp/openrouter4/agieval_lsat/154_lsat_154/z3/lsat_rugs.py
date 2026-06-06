from z3 import *

solver = Solver()

# Colors to rug assignments: 0,1,2 for rugs, 3 for unused
f, o, p, t, w, y = Ints('f o p t w y')
colors = [f, o, p, t, w, y]
color_names = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']

# Domain constraints
for c in colors:
    solver.add(And(c >= 0, c <= 3))

# Exactly 5 colors are used
solver.add(Sum([If(c != 3, 1, 0) for c in colors]) == 5)

# Olive rule: If olive used, peach is in same rug
solver.add(Implies(o != 3, And(o == p, p != 3)))

# Forest and turquoise not together
solver.add(Implies(And(f != 3, t != 3), f != t))

# Peach and turquoise not together
solver.add(Implies(And(p != 3, t != 3), p != t))

# Peach and yellow not together
solver.add(Implies(And(p != 3, y != 3), p != y))

# White rule: if white used, its rug has exactly 3 colors (white + 2 others)
for rug in range(3):
    solver.add(Implies(w == rug, 
        Sum([If(c == rug, 1, 0) for c in colors]) == 3))

# Solid yellow: yellow is used and its rug has exactly 1 color
solver.add(y != 3)
solver.add(Sum([If(c == y, 1, 0) for c in colors]) == 1)

# Count of colors in each rug
count_in_rug = [Sum([If(c == r, 1, 0) for c in colors]) for r in range(3)]

# Each rug must have at least 1 color (since all 3 rugs are woven)
for r in range(3):
    solver.add(count_in_rug[r] >= 1)

# Solid rug count
solid_rug_count = Sum([If(count_in_rug[r] == 1, 1, 0) for r in range(3)])

# Evaluate each option
found_options = []

# Option A: There is exactly one solid color rug.
solver.push()
solver.add(solid_rug_count == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: One of the rugs is solid forest.
solver.push()
solver.add(f != 3)
solver.add(Sum([If(c == f, 1, 0) for c in colors]) == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Turquoise is not used in any of the rugs.
solver.push()
solver.add(t == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Forest and olive are used together in a rug.
solver.push()
solver.add(f != 3)
solver.add(o != 3)
solver.add(f == o)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Peach and white are used together in a rug.
solver.push()
solver.add(p != 3)
solver.add(w != 3)
solver.add(p == w)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# For "could be true EXCEPT", the answer is the option that CANNOT be true
# So if 4 are SAT and 1 is UNSAT, that 1 is the answer
print(f"Options that could be true: {found_options}")

all_options = ["A", "B", "C", "D", "E"]
impossible = [opt for opt in all_options if opt not in found_options]

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible}")
elif len(impossible) == 0:
    print("STATUS: unsat")
    print("Refine: All options are possible (none impossible)")