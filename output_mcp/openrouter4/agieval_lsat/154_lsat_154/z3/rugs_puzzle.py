from z3 import *

solver = Solver()

# Colors: F=forest, O=olive, P=peach, T=turquoise, W=white, Y=yellow
colors = ['F', 'O', 'P', 'T', 'W', 'Y']
n = len(colors)  # 6

# Each color assigned to rug 0,1,2,3 where 0 = not used, 1/2/3 = rug number
rug = {c: Int(f'rug_{c}') for c in colors}

for c in colors:
    solver.add(rug[c] >= 0)
    solver.add(rug[c] <= 3)

# Exactly 5 of 6 colors are used (exactly one color has value 0)
solver.add(Sum([If(rug[c] == 0, 1, 0) for c in colors]) == 1)

# Rule 1: In any rug in which white is used, two other colors are also used.
# So if white is in rug r (r != 0), then the count of colors in rug r is exactly 3.
for r in [1, 2, 3]:
    # Count of colors in rug r
    count_r = Sum([If(rug[c] == r, 1, 0) for c in colors])
    solver.add(Implies(rug['W'] == r, count_r == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
# If olive is used (rug['O'] != 0), then peach is used and in the same rug.
solver.add(Implies(rug['O'] != 0, And(rug['P'] != 0, rug['O'] == rug['P'])))

# Rule 3: Forest and turquoise are not used together in a rug.
solver.add(Not(And(rug['F'] != 0, rug['T'] != 0, rug['F'] == rug['T'])))

# Rule 4: Peach and turquoise are not used together in a rug.
solver.add(Not(And(rug['P'] != 0, rug['T'] != 0, rug['P'] == rug['T'])))

# Rule 5: Peach and yellow are not used together in a rug.
solver.add(Not(And(rug['P'] != 0, rug['Y'] != 0, rug['P'] == rug['Y'])))

# Given condition: One of the rugs is solid yellow.
# So yellow is used (rug['Y'] != 0), and the rug containing yellow has exactly 1 color.
# First, yellow must be used:
solver.add(rug['Y'] != 0)
# The rug containing yellow has exactly 1 color:
for r in [1, 2, 3]:
    count_r = Sum([If(rug[c] == r, 1, 0) for c in colors])
    solver.add(Implies(rug['Y'] == r, count_r == 1))

# Now evaluate each option

# Option A: There is exactly one solid color rug.
# A solid rug has exactly 1 color. We need exactly one rug with count == 1.
opt_a = Sum([If(Sum([If(rug[c] == r, 1, 0) for c in colors]) == 1, 1, 0) for r in [1, 2, 3]]) == 1

# Option B: One of the rugs is solid forest.
# Forest is used and its rug has exactly 1 color.
opt_b = And(rug['F'] != 0, Sum([If(rug[c] == rug['F'], 1, 0) for c in colors]) == 1)

# Option C: Turquoise is not used in any of the rugs.
opt_c = rug['T'] == 0

# Option D: Forest and olive are used together in a rug.
opt_d = And(rug['F'] != 0, rug['O'] != 0, rug['F'] == rug['O'])

# Option E: Peach and white are used together in a rug.
opt_e = And(rug['P'] != 0, rug['W'] != 0, rug['P'] == rug['W'])

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        found_options.append(letter)
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")