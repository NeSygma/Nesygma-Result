from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
# rug[i] = which rug (0,1,2) color i is assigned to, or -1 if not used
colors = [Int(f'color_{i}') for i in range(6)]
color_names = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']

# Each color is assigned to rug 0, 1, 2, or -1 (not used)
for c in colors:
    solver.add(Or(c == -1, c == 0, c == 1, c == 2))

# Exactly 5 colors are used (exactly 1 is not used)
solver.add(Sum([If(c != -1, 1, 0) for c in colors]) == 5)

# Count colors per rug
rug_size = [Sum([If(colors[i] == r, 1, 0) for i in range(6)]) for r in range(3)]

# Exactly two rugs are solid (size 1), one rug is multicolored (size 3)
solver.add(Sum([If(rug_size[r] == 1, 1, 0) for r in range(3)]) == 2)
solver.add(Sum([If(rug_size[r] == 3, 1, 0) for r in range(3)]) == 1)

# Rule 1: If white (4) is used in a rug, two other colors are also used (rug has 3 colors)
for r in range(3):
    solver.add(Implies(colors[4] == r, rug_size[r] == 3))

# Rule 2: If olive (1) is used in a rug, peach (2) is also used in that rug
for r in range(3):
    solver.add(Implies(colors[1] == r, colors[2] == r))

# Rule 3: Forest (0) and turquoise (3) not together
for r in range(3):
    solver.add(Not(And(colors[0] == r, colors[3] == r)))

# Rule 4: Peach (2) and turquoise (3) not together
for r in range(3):
    solver.add(Not(And(colors[2] == r, colors[3] == r)))

# Rule 5: Peach (2) and yellow (5) not together
for r in range(3):
    solver.add(Not(And(colors[2] == r, colors[5] == r)))

# Helper: color c is in a solid rug (rug of size 1)
def solid_color_constraint(c_idx):
    """color c_idx is assigned to a rug of size 1"""
    size_is_one = Or([And(colors[c_idx] == r, rug_size[r] == 1) for r in range(3)])
    return And(colors[c_idx] != -1, size_is_one)

def two_colors_are_solid(c1, c2):
    """c1 and c2 are each in a different solid rug"""
    return And(
        solid_color_constraint(c1),
        solid_color_constraint(c2),
        colors[c1] != colors[c2]
    )

options = {
    "A": two_colors_are_solid(0, 2),  # forest and peach
    "B": two_colors_are_solid(0, 5),  # forest and yellow
    "C": two_colors_are_solid(2, 3),  # peach and turquoise
    "D": two_colors_are_solid(2, 5),  # peach and yellow
    "E": two_colors_are_solid(3, 5),  # turquoise and yellow
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        print(f"Option {letter}: POSSIBLE (sat)")
        m = solver.model()
        for i in range(6):
            val = m.eval(colors[i], model_completion=True)
            if val.as_long() != -1:
                print(f"  {color_names[i]} -> rug {val}")
            else:
                print(f"  {color_names[i]} -> not used")
        for r in range(3):
            print(f"  Rug {r} size: {m.eval(rug_size[r], model_completion=True)}")
    else:
        print(f"Option {letter}: IMPOSSIBLE ({result})")
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