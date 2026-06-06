from z3 import *

# Define the antiques
antiques = ['H', 'L', 'M', 'S', 'T', 'V']
# pos[a] is the day (1-6) the antique 'a' is auctioned
pos = {a: Int(f'pos_{a}') for a in antiques}

solver = Solver()

# Domain constraints
for a in antiques:
    solver.add(pos[a] >= 1, pos[a] <= 6)

# All antiques are auctioned on different days
solver.add(Distinct([pos[a] for a in antiques]))

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(pos['S'] != 1)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp, 
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(pos['H'] < pos['L'], pos['M'] < pos['L']))

# Condition 3: The sundial is auctioned on an earlier date than the mirror 
# and also on an earlier date than the vase.
solver.add(pos['S'] < pos['M'])
solver.add(pos['S'] < pos['V'])

# Condition 4: The table is auctioned on an earlier date than the harmonica 
# or on an earlier date than the vase, but not both.
# XOR in Z3: Xor(a, b)
solver.add(Xor(pos['T'] < pos['H'], pos['T'] < pos['V']))

# Test each option
options = [
    ("A", And(pos['T'] == 2, pos['L'] == 3)),
    ("B", And(pos['S'] == 2, pos['V'] == 3)),
    ("C", And(pos['M'] == 3, pos['S'] == 4)),
    ("D", And(pos['V'] == 4, pos['S'] == 5)),
    ("E", And(pos['S'] == 4, pos['T'] == 5))
]

found_options = []
for letter, constr in options:
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