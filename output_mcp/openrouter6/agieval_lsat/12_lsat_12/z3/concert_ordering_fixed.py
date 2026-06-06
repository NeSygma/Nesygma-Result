from z3 import *

# Base constraints
comps = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in comps}

solver = Solver()

# Domain and distinctness
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct([pos[c] for c in comps]))

# Condition 1: T immediately before F OR immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Condition 2: At least two compositions between F and R
solver.add(Or(
    And(pos['F'] < pos['R'], pos['R'] - pos['F'] >= 3),
    And(pos['R'] < pos['F'], pos['F'] - pos['R'] >= 3)
))

# Condition 3: O first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 4: Eighth is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 5: P before S
solver.add(pos['P'] < pos['S'])

# Condition 6: At least one composition between O and S
solver.add(Or(
    And(pos['O'] < pos['S'], pos['S'] - pos['O'] >= 2),
    And(pos['S'] < pos['O'], pos['O'] - pos['S'] >= 2)
))

# Define answer choices as sequences from first to eighth
choices = {
    "A": ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    "B": ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    "C": ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    "D": ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    "E": ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
}

found_options = []
for letter, seq in choices.items():
    solver.push()
    # Add constraints for this sequence
    for idx, comp in enumerate(seq, start=1):
        solver.add(pos[comp] == idx)
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