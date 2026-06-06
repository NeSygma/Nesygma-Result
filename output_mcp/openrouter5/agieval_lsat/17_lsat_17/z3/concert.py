from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
# We'll use Int variables for each composition's position
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
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# This means the number of compositions strictly between F and R is >= 2.
# So |pos[F] - pos[R]| >= 3
solver.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))

# Condition 3: O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 5: P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# This means |pos[O] - pos[S]| >= 2 (at least one composition strictly between them)
solver.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))

# Given: P is performed third and S is performed sixth.
solver.add(pos['P'] == 3)
solver.add(pos['S'] == 6)

# Now evaluate each answer choice for "the composition performed fifth must be"
# Each option gives a pair: the fifth position must be one of the two.

# Option A: F or H
opt_a = Or(pos['F'] == 5, pos['H'] == 5)
# Option B: F or O
opt_b = Or(pos['F'] == 5, pos['O'] == 5)
# Option C: F or T
opt_c = Or(pos['F'] == 5, pos['T'] == 5)
# Option D: H or L
opt_d = Or(pos['H'] == 5, pos['L'] == 5)
# Option E: O or R
opt_e = Or(pos['O'] == 5, pos['R'] == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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