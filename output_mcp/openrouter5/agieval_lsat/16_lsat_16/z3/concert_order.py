from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
comp_names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Create Int variables for each composition's position (1..8)
pos = {c: Int(f'pos_{c}') for c in comp_names}

solver = Solver()

# Each position is between 1 and 8
for c in comp_names:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct (each composition performed exactly once)
solver.add(Distinct([pos[c] for c in comp_names]))

# Condition 1: T is performed either immediately before F or immediately after R.
# T immediately before F: pos[T] + 1 == pos[F]
# T immediately after R: pos[R] + 1 == pos[T]
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# So |pos[F] - pos[R]| >= 3 (since at least 2 compositions between them)
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))

# Condition 3: O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 5: P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# |pos[O] - pos[S]| >= 2
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Additional condition from the question: S is performed fourth.
solver.add(pos['S'] == 4)

# Now evaluate each option.
# Each option gives a list of compositions for positions 1, 2, 3.
options = {
    "A": ['F', 'H', 'P'],
    "B": ['H', 'P', 'L'],
    "C": ['O', 'P', 'R'],
    "D": ['O', 'P', 'T'],
    "E": ['P', 'R', 'T']
}

found_options = []
for letter, opt_list in options.items():
    solver.push()
    # Constrain positions 1, 2, 3 to the given compositions
    solver.add(pos[opt_list[0]] == 1)
    solver.add(pos[opt_list[1]] == 2)
    solver.add(pos[opt_list[2]] == 3)
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