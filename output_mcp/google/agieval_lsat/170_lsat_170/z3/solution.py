from z3 import *

# Sections: 0: Lifestyle, 1: Metro, 2: Sports
# Photos: 2 per section
# Photographers: 0: Fuentes, 1: Gagnon, 2: Hue

solver = Solver()

# p[section][photo_index]
p = [[Int(f'p_{s}_{i}') for i in range(2)] for s in range(3)]

# Domain constraints
for s in range(3):
    for i in range(2):
        solver.add(p[s][i] >= 0, p[s][i] <= 2)

# 1. Each photographer has at least 1 and at most 3 photos total
for photog in range(3):
    count = Sum([If(p[s][i] == photog, 1, 0) for s in range(3) for i in range(2)])
    solver.add(count >= 1, count <= 3)

# 2. At least one photo in L must be by a photographer who has at least one photo in M
# Let has_in_M(photog) be true if photog has a photo in M
def has_in_M(photog):
    return Or(p[1][0] == photog, p[1][1] == photog)

# At least one photo in L (p[0][0] or p[0][1]) is by a photog who has_in_M(photog)
solver.add(Or(
    And(p[0][0] == 0, has_in_M(0)),
    And(p[0][0] == 1, has_in_M(1)),
    And(p[0][0] == 2, has_in_M(2)),
    And(p[0][1] == 0, has_in_M(0)),
    And(p[0][1] == 1, has_in_M(1)),
    And(p[0][1] == 2, has_in_M(2))
))

# 3. Count(H in L) == Count(F in S)
solver.add(Sum([If(p[0][i] == 2, 1, 0) for i in range(2)]) == Sum([If(p[2][i] == 0, 1, 0) for i in range(2)]))

# 4. None of Gagnon's photos can be in the Sports section
solver.add(p[2][0] != 1, p[2][1] != 1)

# Question condition: One photo in L is by Gagnon and one is by Hue
solver.add(Sum([If(p[0][i] == 1, 1, 0) for i in range(2)]) == 1)
solver.add(Sum([If(p[0][i] == 2, 1, 0) for i in range(2)]) == 1)

# Define options
opt_a = (Sum([If(p[1][i] == 0, 1, 0) for i in range(2)]) == 1)
opt_b = (Sum([If(p[1][i] == 1, 1, 0) for i in range(2)]) == 1)
opt_c = (Sum([If(p[1][i] == 1, 1, 0) for i in range(2)]) == 2)
opt_d = (Sum([If(p[2][i] == 2, 1, 0) for i in range(2)]) == 1)
opt_e = (Sum([If(p[2][i] == 2, 1, 0) for i in range(2)]) == 2)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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