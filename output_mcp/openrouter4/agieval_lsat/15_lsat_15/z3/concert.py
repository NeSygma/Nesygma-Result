from z3 import *

solver = Solver()

# Compositions: F, H, L, O, P, R, S, T
# Their positions: 1 to 8
pos = {}
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
for name in names:
    pos[name] = Int(f'pos_{name}')
    solver.add(pos[name] >= 1, pos[name] <= 8)

# All positions are distinct
solver.add(Distinct([pos[name] for name in names]))

# Constraint 1: T is performed either immediately before F or immediately after R.
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F.
# This means |pos_F - pos_R| >= 3 (at least 2 positions strictly between them)
solver.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))

# Constraint 3: O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Constraint 4: The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Constraint 5: P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O.
# This means |pos_O - pos_S| >= 2 (at least 1 composition strictly between them)
solver.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))

# Additional condition: O is performed immediately after T
solver.add(pos['T'] + 1 == pos['O'])

# Now let's find all possible positions for F
# Use enumeration
possible_f_positions = set()

while solver.check() == sat:
    m = solver.model()
    f_pos = m.eval(pos['F']).as_long()
    possible_f_positions.add(f_pos)
    # Block this solution
    solver.add(Or([pos[name] != m.eval(pos[name]).as_long() for name in names]))

print(f"Possible positions for F: {sorted(possible_f_positions)}")

# Now evaluate each option
# Option A: first(1) or second(2)
# Option B: second(2) or third(3)
# Option C: fourth(4) or sixth(6)
# Option D: fourth(4) or seventh(7)
# Option E: sixth(6) or seventh(7)

options = {
    'A': {1, 2},
    'B': {2, 3},
    'C': {4, 6},
    'D': {4, 7},
    'E': {6, 7}
}

# Find which option correctly captures the possible positions
# The correct option is the one where all possible F positions are within the option's set,
# AND the option doesn't include positions that are impossible... actually,
# "F must be performed either first or second" means F can only be first or second.
# So the set of possible positions should be a subset of the option's set.

# Actually, let's just check each option: can F be outside those two positions?
found_options = []
for letter, pos_set in options.items():
    solver.push()
    # Add constraint that F is NOT in any of the two positions
    solver.add(And([pos['F'] != p for p in pos_set]))
    if solver.check() == unsat:
        # F cannot be outside these positions, so F must be in one of them
        found_options.append(letter)
    solver.pop()

print(f"Options where F must be in the given positions: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    # Check more carefully - which option's set exactly matches the possible positions
    print(f"Multiple options found: {found_options}")
    print("Checking exact match...")
    for letter, pos_set in options.items():
        if possible_f_positions == pos_set:
            print(f"Exact match: {letter}")
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")