from z3 import *

# Members
members = ['G', 'K', 'P', 'S', 'T', 'V']
# pos[m] is the position (1-6) of member m
pos = {m: Int(f'pos_{m}') for m in members}

solver = Solver()

# Each member performs exactly one solo at a unique position 1-6
solver.add(Distinct([pos[m] for m in members]))
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)

# Constraints
# 1. The guitarist does not perform the fourth solo.
solver.add(pos['G'] != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(pos['P'] < pos['K'])

# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(pos['V'] < pos['K'])
solver.add(pos['K'] < pos['G'])

# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# (S > P) XOR (S > T)
solver.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))

# Define the answer choices
choices = {
    'A': ['V', 'P', 'S', 'G', 'T', 'K'],
    'B': ['P', 'V', 'K', 'T', 'S', 'G'],
    'C': ['V', 'T', 'S', 'P', 'K', 'G'],
    'D': ['K', 'T', 'V', 'S', 'G', 'P'],
    'E': ['G', 'V', 'K', 'P', 'S', 'T']
}

def check_choice(order):
    # order is a list of members in order of position 1 to 6
    s = Solver()
    # Add base constraints
    s.add(Distinct([pos[m] for m in members]))
    for m in members:
        s.add(pos[m] >= 1, pos[m] <= 6)
    s.add(pos['G'] != 4)
    s.add(pos['P'] < pos['K'])
    s.add(pos['V'] < pos['K'])
    s.add(pos['K'] < pos['G'])
    s.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))
    
    # Add choice constraints
    for i, m in enumerate(order):
        s.add(pos[m] == i + 1)
    
    return s.check() == sat

found_options = []
for letter, order in choices.items():
    if check_choice(order):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")