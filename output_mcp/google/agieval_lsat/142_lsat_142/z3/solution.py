from z3 import *

# Members
members = ['G', 'K', 'P', 'S', 'T', 'V']
# Positions 1-6
pos = {m: Int(f'pos_{m}') for m in members}

solver = Solver()

# Each member has a unique position from 1 to 6
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Constraints
# 1. The guitarist does not perform the fourth solo.
solver.add(pos['G'] != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(pos['P'] < pos['K'])

# 3. The keyboard player performs a solo at some time after the violinist does
solver.add(pos['V'] < pos['K'])

# 4. and at some time before the guitarist does.
solver.add(pos['K'] < pos['G'])

# 5. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# (S > P XOR S > T)
solver.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))

# Test each option for position 3
options = [('A', 'G'), ('B', 'K'), ('C', 'S'), ('D', 'T'), ('E', 'V')]
found_options = []

for letter, member in options:
    solver.push()
    solver.add(pos[member] == 3)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Options that CAN perform the third solo: {found_options}")

# The question asks which one CANNOT perform the third.
# So we look for the one that is NOT in found_options.
all_options = ['A', 'B', 'C', 'D', 'E']
cannot_perform = [opt for opt in all_options if opt not in found_options]

if len(cannot_perform) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_perform[0]}")
elif len(cannot_perform) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {cannot_perform}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")