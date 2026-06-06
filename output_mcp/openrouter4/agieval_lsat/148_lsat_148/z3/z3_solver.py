from z3 import *

solver = Solver()

# Positions: 1, 2, 3, 4
# Historians
p_F = Int('p_F')  # Farley
p_G = Int('p_G')  # Garcia
p_H = Int('p_H')  # Holden
p_J = Int('p_J')  # Jiang

# Topics
p_O = Int('p_O')  # Oil paintings
p_W = Int('p_W')  # Watercolors
p_L = Int('p_L')  # Lithographs
p_S = Int('p_S')  # Sculptures

# Domain: each position between 1 and 4
for var in [p_F, p_G, p_H, p_J, p_O, p_W, p_L, p_S]:
    solver.add(var >= 1, var <= 4)

# All historian positions are distinct
solver.add(Distinct(p_F, p_G, p_H, p_J))

# All topic positions are distinct
solver.add(Distinct(p_O, p_W, p_L, p_S))

# Constraint 1: Oil paintings and watercolors must both be earlier than lithographs
solver.add(p_O < p_L)
solver.add(p_W < p_L)

# Constraint 2: Farley's lecture must be earlier than the oil paintings lecture
solver.add(p_F < p_O)

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's
solver.add(p_H < p_G)
solver.add(p_H < p_J)

# Given: Garcia gives the sculptures lecture -> p_G = p_S
solver.add(p_G == p_S)

# Now test each option
options = {
    "A": p_L == 3,  # lithographs lecture is third
    "B": p_O == 3,  # oil paintings lecture is third
    "C": p_S == 1,  # sculptures lecture is first
    "D": p_S == 2,  # sculptures lecture is second
    "E": p_W == 2   # watercolors lecture is second
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter} ({constr}): {result}")
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"  Model: p_F={m[p_F]}, p_G={m[p_G]}, p_H={m[p_H]}, p_J={m[p_J]}")
        print(f"         p_O={m[p_O]}, p_W={m[p_W]}, p_L={m[p_L]}, p_S={m[p_S]}")
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