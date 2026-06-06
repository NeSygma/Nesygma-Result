from z3 import *

# Compositions
comp_names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in comp_names}

solver = Solver()

# Domain: 1 to 8
for c in comp_names:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All distinct
solver.add(Distinct([pos[c] for c in comp_names]))

# 1. T is immediately before F OR immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['T'] - 1 == pos['R']))

# 2. At least two compositions between F and R
# |pos[F] - pos[R]| - 1 >= 2  => |pos[F] - pos[R]| >= 3
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# 3. O is 1st or 5th
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# 4. 8th is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# 5. P is before S
solver.add(pos['P'] < pos['S'])

# 6. At least one composition between O and S
# |pos[O] - pos[S]| - 1 >= 1 => |pos[O] - pos[S]| >= 2
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Test each option
options = [("A", 2), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]
found_options = []

for letter, p_pos in options:
    solver.push()
    solver.add(pos['P'] == p_pos)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Options where P can be placed: {found_options}")
if len(found_options) == 4:
    # If 4 are possible, one is impossible.
    all_options = ["A", "B", "C", "D", "E"]
    impossible = [opt for opt in all_options if opt not in found_options]
    print(f"STATUS: sat")
    print(f"answer:{impossible[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Found {len(found_options)} options, expected 4.")