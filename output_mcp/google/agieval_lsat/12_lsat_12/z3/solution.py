from z3 import *

# Compositions
comps = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
# pos[comp] is the position (1-8)
pos = {c: Int(c) for c in comps}

solver = Solver()

# Each position 1-8 is used exactly once
solver.add(Distinct([pos[c] for c in comps]))
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# 1. T is performed either immediately before F or immediately after R.
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# 2. At least two compositions are performed either after F and before R, or after R and before F.
# |pos(F) - pos(R)| - 1 >= 2  => |pos(F) - pos(R)| >= 3
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# 3. O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# 4. The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# 5. P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# 6. At least one composition is performed either after O and before S, or after S and before O.
# |pos(O) - pos(S)| - 1 >= 1 => |pos(O) - pos(S)| >= 2
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Define options
options = {
    "A": ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    "B": ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    "C": ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    "D": ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    "E": ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
}

found_options = []
for letter, order in options.items():
    solver.push()
    # Add constraints for this specific order
    for i, comp in enumerate(order):
        solver.add(pos[comp] == i + 1)
    
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