from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
# rug[c] = which rug color c belongs to (-1 = unused, 0, 1, 2)
rug = [Int(f'rug_{c}') for c in range(6)]

# Each color assigned to rug -1, 0, 1, or 2
for c in range(6):
    solver.add(Or(rug[c] == -1, rug[c] == 0, rug[c] == 1, rug[c] == 2))

# Exactly 5 colors used (1 unused)
solver.add(Sum([If(rug[c] == -1, 1, 0) for c in range(6)]) == 1)

# Size of each rug
size = [Int(f'size_{r}') for r in range(3)]
for r in range(3):
    solver.add(size[r] == Sum([If(rug[c] == r, 1, 0) for c in range(6)]))

# Exactly 2 solid rugs (size 1) and 1 multicolored rug (size 3)
# 5 colors - 2 solid = 3 in multicolored
solver.add(Sum([If(size[r] == 1, 1, 0) for r in range(3)]) == 2)
solver.add(Sum([If(size[r] == 3, 1, 0) for r in range(3)]) == 1)

# Constraint 1: White - if used, in a rug with >= 3 colors (the multicolored rug)
for r in range(3):
    solver.add(Implies(rug[4] == r, size[r] >= 3))

# Constraint 2: Olive-Peach same rug if olive used
solver.add(Implies(rug[1] != -1, And(rug[2] != -1, rug[1] == rug[2])))

# Constraint 3: Forest-Turquoise not together
solver.add(Implies(And(rug[0] != -1, rug[3] != -1), rug[0] != rug[3]))

# Constraint 4: Peach-Turquoise not together
solver.add(Implies(And(rug[2] != -1, rug[3] != -1), rug[2] != rug[3]))

# Constraint 5: Peach-Yellow not together
solver.add(Implies(And(rug[2] != -1, rug[5] != -1), rug[2] != rug[5]))

# Test each option: can these two colors be the solid rug colors?
options = [
    ("A", 0, 2),  # forest and peach
    ("B", 0, 5),  # forest and yellow
    ("C", 2, 3),  # peach and turquoise
    ("D", 2, 5),  # peach and yellow
    ("E", 3, 5),  # turquoise and yellow
]

found_options = []
for letter, c1, c2 in options:
    solver.push()
    # Both colors must be used
    solver.add(rug[c1] != -1)
    solver.add(rug[c2] != -1)
    # They must be in different rugs
    solver.add(rug[c1] != rug[c2])
    # Each must be in a solid rug (size == 1)
    for r in range(3):
        solver.add(Implies(rug[c1] == r, size[r] == 1))
        solver.add(Implies(rug[c2] == r, size[r] == 1))
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        rug_vals = [m.evaluate(rug[c]) for c in range(6)]
        size_vals = [m.evaluate(size[r]) for r in range(3)]
        print(f"Option {letter} SAT: rug_assignments={rug_vals}, sizes={size_vals}")
    else:
        print(f"Option {letter} UNSAT (IMPOSSIBLE)")
    solver.pop()

print(f"\nSatisfiable (possible) options: {found_options}")

# The answer is the option that CANNOT be (unsatisfiable)
impossible = [l for l, _, _ in options if l not in found_options]
print(f"Impossible options: {impossible}")

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")