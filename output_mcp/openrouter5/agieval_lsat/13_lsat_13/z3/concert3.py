from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Create integer variables for the position of each composition
pos = {c: Int(f'pos_{c}') for c in compositions}

# The question asks: "P CANNOT be performed" at which position?
# We need to find which position is IMPOSSIBLE for P.
# Let's check each option: if adding "P is at position X" makes the problem UNSAT,
# then P cannot be at that position.

# Base constraints
def add_base_constraints(s):
    for c in compositions:
        s.add(pos[c] >= 1, pos[c] <= 8)
    s.add(Distinct([pos[c] for c in compositions]))
    # T immediately before F or immediately after R
    s.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))
    # At least two compositions between F and R
    s.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))
    # O is first or fifth
    s.add(Or(pos['O'] == 1, pos['O'] == 5))
    # Eighth is L or H
    s.add(Or(pos['L'] == 8, pos['H'] == 8))
    # P before S
    s.add(pos['P'] < pos['S'])
    # At least one composition between O and S
    s.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))

options = {
    'A': pos['P'] == 2,
    'B': pos['P'] == 3,
    'C': pos['P'] == 4,
    'D': pos['P'] == 6,
    'E': pos['P'] == 7
}

found_impossible = []
for letter, constr in options.items():
    s = Solver()
    add_base_constraints(s)
    s.add(constr)
    if s.check() == unsat:
        found_impossible.append(letter)

print(f"Positions where P CANNOT be: {found_impossible}")

if len(found_impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{found_impossible[0]}")
elif len(found_impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {found_impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")