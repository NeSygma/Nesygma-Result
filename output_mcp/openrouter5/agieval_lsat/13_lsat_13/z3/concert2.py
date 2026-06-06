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
solver.add(Or(
    pos['T'] + 1 == pos['F'],
    pos['R'] + 1 == pos['T']
))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# So |pos[F] - pos[R]| >= 3 (at least 2 compositions between them)
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

# Let's first find all valid models to understand the constraints better
# We'll enumerate solutions to see which positions P can take

solutions = []
decision_vars = [pos[c] for c in compositions]

while solver.check() == sat:
    m = solver.model()
    sol = {c: m.eval(pos[c], model_completion=True).as_long() for c in compositions}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([pos[c] != m.eval(pos[c], model_completion=True) for c in compositions]))

print(f"Total valid orderings found: {len(solutions)}")

# Check which positions P can take
p_positions = set()
for sol in solutions:
    p_positions.add(sol['P'])

print(f"P can be at positions: {sorted(p_positions)}")

# All positions 1-8
all_positions = set(range(1, 9))
cannot_be = sorted(all_positions - p_positions)
print(f"P CANNOT be at positions: {cannot_be}")

# Now evaluate each option
options = {
    'A': pos['P'] == 2,
    'B': pos['P'] == 3,
    'C': pos['P'] == 4,
    'D': pos['P'] == 6,
    'E': pos['P'] == 7
}

# Re-create solver for clean check
solver2 = Solver()
for c in compositions:
    solver2.add(pos[c] >= 1, pos[c] <= 8)
solver2.add(Distinct([pos[c] for c in compositions]))
solver2.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))
solver2.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))
solver2.add(Or(pos['O'] == 1, pos['O'] == 5))
solver2.add(Or(pos['L'] == 8, pos['H'] == 8))
solver2.add(pos['P'] < pos['S'])
solver2.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))

found_options = []
for letter, constr in options.items():
    solver2.push()
    solver2.add(constr)
    if solver2.check() == sat:
        found_options.append(letter)
    solver2.pop()

print(f"Options that are SAT (P CAN be there): {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")