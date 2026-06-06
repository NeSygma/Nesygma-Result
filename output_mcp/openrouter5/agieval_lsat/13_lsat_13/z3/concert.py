from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Create integer variables for the position of each composition
pos = {c: Int(f'pos_{c}') for c in compositions}

solver = Solver()

# Each position is between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct (each composition performed exactly once)
solver.add(Distinct([pos[c] for c in compositions]))

# Condition 1: T is performed either immediately before F or immediately after R.
# T immediately before F: pos[T] + 1 == pos[F]
# T immediately after R: pos[R] + 1 == pos[T]
solver.add(Or(
    pos['T'] + 1 == pos['F'],
    pos['R'] + 1 == pos['T']
))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# Let gap = |pos[F] - pos[R]| - 1. We need gap >= 2.
# So |pos[F] - pos[R]| >= 3
solver.add(Or(
    pos['F'] + 3 <= pos['R'],
    pos['R'] + 3 <= pos['F']
))

# Condition 3: O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 5: P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# |pos[O] - pos[S]| >= 2
solver.add(Or(
    pos['O'] + 2 <= pos['S'],
    pos['S'] + 2 <= pos['O']
))

# Now evaluate each option: "P CANNOT be performed at position X"
# We test: can P be at position X? If sat, then P CAN be at X. If unsat, then P CANNOT be at X.
# We want the position where P CANNOT be performed.

options = {
    'A': pos['P'] == 2,
    'B': pos['P'] == 3,
    'C': pos['P'] == 4,
    'D': pos['P'] == 6,
    'E': pos['P'] == 7
}

found_options = []
for letter, constr in options.items():
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