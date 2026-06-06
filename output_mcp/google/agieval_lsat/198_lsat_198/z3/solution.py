from z3 import *

# Antiques
antiques = ['H', 'L', 'M', 'S', 'T', 'V']
# Days 1-6
days = range(1, 7)

# pos[A] is the day antique A is auctioned
pos = {a: Int(f'pos_{a}') for a in antiques}

solver = Solver()

# Each antique is auctioned on a unique day
solver.add(Distinct([pos[a] for a in antiques]))
for a in antiques:
    solver.add(pos[a] >= 1, pos[a] <= 6)

# C1: The sundial is not auctioned on June 1st.
solver.add(pos['S'] != 1)

# C2: If the harmonica is auctioned on an earlier date than the lamp, 
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(pos['H'] < pos['L'], pos['M'] < pos['L']))

# C3: The sundial is auctioned on an earlier date than the mirror 
# and also on an earlier date than the vase.
solver.add(pos['S'] < pos['M'])
solver.add(pos['S'] < pos['V'])

# C4: The table is auctioned on an earlier date than the harmonica 
# or on an earlier date than the vase, but not both.
solver.add(Xor(pos['T'] < pos['H'], pos['T'] < pos['V']))

# Q-Condition: If the table is auctioned on a date that is later than 
# both the date on which the mirror is auctioned and the date on which the vase is auctioned
solver.add(pos['T'] > pos['M'])
solver.add(pos['T'] > pos['V'])

# Options
options = {
    "A": pos['H'] < pos['T'],
    "B": pos['T'] < pos['L'],
    "C": pos['T'] < pos['S'],
    "D": pos['M'] < pos['V'],
    "E": pos['S'] < pos['L']
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