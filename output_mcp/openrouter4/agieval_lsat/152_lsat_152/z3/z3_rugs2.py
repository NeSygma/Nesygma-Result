from z3 import *

# Colors: forest(0), olive(1), peach(2), turquoise(3), white(4), yellow(5)
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5
N = 6
color_names = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

solver = Solver()

# rug[c] = 0,1,2 (rug assignment) or 3 (unused)
rug = [Int(f'rug_{c}') for c in range(N)]
for c in range(N):
    solver.add(rug[c] >= 0, rug[c] <= 3)

# Exactly 5 of 6 colors are used
solver.add(Sum([If(rug[c] != 3, 1, 0) for c in range(N)]) == 5)

# Each rug has at least 1 color
for r in range(3):
    solver.add(Sum([If(rug[c] == r, 1, 0) for c in range(N)]) >= 1)

# Exactly 2 rugs are solid (have exactly 1 color)
solid_rug_count = Sum([If(Sum([If(rug[c] == r, 1, 0) for c in range(N)]) == 1, 1, 0) for r in range(3)])
solver.add(solid_rug_count == 2)

# Rule 1: If white is used, its rug has exactly 3 colors (white + 2 others)
solver.add(Implies(rug[W] != 3,
    Sum([If(rug[c] == rug[W], 1, 0) for c in range(N)]) == 3))

# Rule 2: If olive is used, peach is also used in the same rug
solver.add(Implies(rug[O] != 3,
    And(rug[P] != 3, rug[O] == rug[P])))

# Rule 3: Forest and turquoise not together in a rug
solver.add(Implies(And(rug[F] != 3, rug[T] != 3),
    rug[F] != rug[T]))

# Rule 4: Peach and turquoise not together in a rug
solver.add(Implies(And(rug[P] != 3, rug[T] != 3),
    rug[P] != rug[T]))

# Rule 5: Peach and yellow not together in a rug
solver.add(Implies(And(rug[P] != 3, rug[Y] != 3),
    rug[P] != rug[Y]))

# Test each option: which option is IMPOSSIBLE (UNSAT)?
# The question asks which pair CANNOT be the two solid rugs.
# We want the option that is UNSAT when we force those two colors to be solid rugs.

options = [
    ("A", F, P),
    ("B", F, Y),
    ("C", P, T),
    ("D", P, Y),
    ("E", T, Y),
]

impossible_options = []

for letter, c1, c2 in options:
    solver.push()
    # c1 is in a solid rug (only color in its rug)
    solver.add(Sum([If(rug[i] == rug[c1], 1, 0) for i in range(N)]) == 1)
    # c2 is in a different solid rug
    solver.add(Sum([If(rug[i] == rug[c2], 1, 0) for i in range(N)]) == 1)
    solver.add(rug[c1] != rug[c2])
    # Both must be used
    solver.add(rug[c1] != 3)
    solver.add(rug[c2] != 3)
    
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

# The question asks which pair CANNOT be, so we find the one that's impossible.
# If there is exactly one impossible option, that's our answer.
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found (all are possible)")