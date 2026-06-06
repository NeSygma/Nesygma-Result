from z3 import *

# Colors: 0:Forest, 1:Olive, 2:Peach, 3:Turquoise, 4:White, 5:Yellow
colors = range(6)
F, O, P, T, W, Y = 0, 1, 2, 3, 4, 5

solver = Solver()

# Variables
used = [Bool(f'used_{c}') for c in colors]
rug = [Int(f'rug_{c}') for c in colors]

# Exactly 5 colors used
solver.add(Sum([If(used[c], 1, 0) for c in colors]) == 5)

# Rug assignment
for c in colors:
    solver.add(Implies(used[c], And(rug[c] >= 0, rug[c] < 3)))

# Each of the 3 rugs must be used (have at least one color)
for r in range(3):
    solver.add(Or([And(used[c], rug[c] == r) for c in colors]))

# Rule 1: In any rug in which white is used, two other colors are also used.
# (Total 3 colors in that rug)
solver.add(Implies(used[W], Sum([If(And(used[c], rug[c] == rug[W]), 1, 0) for c in colors]) == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
solver.add(Implies(used[O], And(used[P], rug[O] == rug[P])))

# Rule 3: Forest and turquoise are not used together in a rug.
solver.add(Not(And(used[F], used[T], rug[F] == rug[T])))

# Rule 4: Peach and turquoise are not used together in a rug.
solver.add(Not(And(used[P], used[T], rug[P] == rug[T])))

# Rule 5: Peach and yellow are not used together in a rug.
solver.add(Not(And(used[P], used[Y], rug[P] == rug[Y])))

# Condition: Forest and peach are used together in a rug.
solver.add(used[F], used[P], rug[F] == rug[P])

# Options
def is_solid(r):
    return Sum([If(And(used[c], rug[c] == r), 1, 0) for c in colors]) == 1

opt_a = Sum([If(is_solid(r), 1, 0) for r in range(3)]) == 1
opt_b = Not(used[W])
opt_c = Not(used[Y])
opt_d = And(used[T], used[W], rug[T] == rug[W])
opt_e = And(used[T], used[Y], rug[T] == rug[Y])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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