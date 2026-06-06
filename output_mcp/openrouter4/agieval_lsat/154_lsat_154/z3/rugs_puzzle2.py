from z3 import *

solver = Solver()

# Colors: F=forest, O=olive, P=peach, T=turquoise, W=white, Y=yellow
colors = ['F', 'O', 'P', 'T', 'W', 'Y']

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
    count_r = Sum([If(rug[c] == r, 1, 0) for c in colors])
    solver.add(Implies(rug['W'] == r, count_r == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
solver.add(Implies(rug['O'] != 0, And(rug['P'] != 0, rug['O'] == rug['P'])))

# Rule 3: Forest and turquoise are not used together in a rug.
solver.add(Not(And(rug['F'] != 0, rug['T'] != 0, rug['F'] == rug['T'])))

# Rule 4: Peach and turquoise are not used together in a rug.
solver.add(Not(And(rug['P'] != 0, rug['T'] != 0, rug['P'] == rug['T'])))

# Rule 5: Peach and yellow are not used together in a rug.
solver.add(Not(And(rug['P'] != 0, rug['Y'] != 0, rug['P'] == rug['Y'])))

# Given condition: One of the rugs is solid yellow.
solver.add(rug['Y'] != 0)
for r in [1, 2, 3]:
    count_r = Sum([If(rug[c] == r, 1, 0) for c in colors])
    solver.add(Implies(rug['Y'] == r, count_r == 1))

# Now evaluate each option.
# The question asks: which CANNOT be true (EXCEPT)?
# So we test each option. The one that is UNSAT is the answer (cannot be true).
# The ones that are SAT could be true.

# Option A: There is exactly one solid color rug.
opt_a = Sum([If(Sum([If(rug[c] == r, 1, 0) for c in colors]) == 1, 1, 0) for r in [1, 2, 3]]) == 1

# Option B: One of the rugs is solid forest.
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

# First, check if the base problem (without any option) is satisfiable
print("Base problem check:")
base_res = solver.check()
print(f"Base: {base_res}")
if base_res == sat:
    m = solver.model()
    for c in colors:
        print(f"  {c}: {m[rug[c]]}")

print()

# Now test each option
sat_options = []
unsat_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        sat_options.append(letter)
    else:
        unsat_options.append(letter)
    solver.pop()

print()
print(f"Could be true (SAT): {sat_options}")
print(f"Cannot be true (UNSAT): {unsat_options}")

# The EXCEPT answer is the one that is UNSAT (cannot be true)
# If exactly one UNSAT, that's the answer
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) == 0:
    print("STATUS: unsat")
    print("Refine: No options are impossible (all could be true)")
else:
    print("STATUS: unsat")
    print(f"Refine: Multiple options are impossible {unsat_options}")