from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

solver = Solver()

# Each position is between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct
solver.add(Distinct([pos[c] for c in compositions]))

# Condition 1: T is performed either immediately before F or immediately after R.
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# |pos[F] - pos[R]| >= 3
solver.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))

# Condition 3: O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 5: P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# |pos[O] - pos[S]| >= 2
solver.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))

# Given: P is performed third and S is performed sixth.
solver.add(pos['P'] == 3)
solver.add(pos['S'] == 6)

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")
if result == sat:
    m = solver.model()
    for c in compositions:
        print(f"  {c}: {m[pos[c]]}")
else:
    print("Base constraints are unsatisfiable!")
    # Let's debug by checking individual constraints
    # Try removing condition 2 to see if it's the issue
    solver2 = Solver()
    for c in compositions:
        solver2.add(pos[c] >= 1, pos[c] <= 8)
    solver2.add(Distinct([pos[c] for c in compositions]))
    solver2.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))
    # Skip condition 2 for now
    solver2.add(Or(pos['O'] == 1, pos['O'] == 5))
    solver2.add(Or(pos['L'] == 8, pos['H'] == 8))
    solver2.add(pos['P'] < pos['S'])
    solver2.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))
    solver2.add(pos['P'] == 3)
    solver2.add(pos['S'] == 6)
    print(f"Without condition 2: {solver2.check()}")
    if solver2.check() == sat:
        m2 = solver2.model()
        for c in compositions:
            print(f"  {c}: {m2[pos[c]]}")