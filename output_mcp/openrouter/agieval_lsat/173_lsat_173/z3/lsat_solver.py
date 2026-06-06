from z3 import *

# Photographers: 0=Fuentes (F), 1=Gagnon (G), 2=Hue (H)
# Variables for each slot
L1, L2 = Ints('L1 L2')
M1, M2 = Ints('M1 M2')
S1, S2 = Ints('S1 S2')
vars = [L1, L2, M1, M2, S1, S2]

solver = Solver()
# Domain constraints
for v in vars:
    solver.add(And(v >= 0, v <= 2))

# Photographer count constraints: each appears 1 to 3 times total
for p in range(3):
    cnt = Sum([If(v == p, 1, 0) for v in vars])
    solver.add(cnt >= 1, cnt <= 3)

# Intersection: at least one photographer appears in both Lifestyle and Metro
intersect = Or(
    And(Or(L1 == 0, L2 == 0), Or(M1 == 0, M2 == 0)),
    And(Or(L1 == 1, L2 == 1), Or(M1 == 1, M2 == 1)),
    And(Or(L1 == 2, L2 == 2), Or(M1 == 2, M2 == 2))
)
solver.add(intersect)

# Hue in Lifestyle equals Fuentes in Sports
hue_L = Sum([If(L1 == 2, 1, 0), If(L2 == 2, 1, 0)])
fuentes_S = Sum([If(S1 == 0, 1, 0), If(S2 == 0, 1, 0)])
solver.add(hue_L == fuentes_S)

# No Gagnon in Sports
solver.add(S1 != 1, S2 != 1)

# At least one section has both photographs by Gagnon
both_G_section = Or(
    And(L1 == 1, L2 == 1),
    And(M1 == 1, M2 == 1),
    And(S1 == 1, S2 == 1)
)
solver.add(both_G_section)

# Define option constraints
opt_a = And(L1 == 2, L2 == 2)  # both Lifestyle Hue
opt_b = And(Or(L1 == 0, L2 == 0), Or(L1 == 2, L2 == 2), L1 != L2)  # one F one H in Lifestyle
# more directly: set of two values {0,2}
opt_c = And(M1 == 0, M2 == 0)  # both Metro Fuentes
opt_d = And(Or(M1 == 1, M2 == 1), Or(M1 == 2, M2 == 2), M1 != M2)  # one G one H in Metro
opt_e = And(S1 == 2, S2 == 2)  # both Sports Hue

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