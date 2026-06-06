from z3 import *

# Antiques: Harmonica (H), Lamp (L), Mirror (M), Sundial (S), Table (T), Vase (V)
antiques = ['H', 'L', 'M', 'S', 'T', 'V']
pos = {a: Int(a) for a in antiques}

solver = Solver()

# Each antique is auctioned on a unique day from 1 to 6
for a in antiques:
    solver.add(pos[a] >= 1, pos[a] <= 6)
solver.add(Distinct([pos[a] for a in antiques]))

# Constraints:
# 1. The sundial is not auctioned on June 1st.
solver.add(pos['S'] != 1)

# 2. If the harmonica is auctioned on an earlier date than the lamp, 
#    then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(pos['H'] < pos['L'], pos['M'] < pos['L']))

# 3. The sundial is auctioned on an earlier date than the mirror 
#    and also on an earlier date than the vase.
solver.add(pos['S'] < pos['M'])
solver.add(pos['S'] < pos['V'])

# 4. The table is auctioned on an earlier date than the harmonica 
#    or on an earlier date than the vase, but not both.
#    (T < H) XOR (T < V)
solver.add(Xor(pos['T'] < pos['H'], pos['T'] < pos['V']))

# Options:
options = [
    ("A", pos['S'] == 5),
    ("B", pos['S'] == 4),
    ("C", And(pos['L'] == 5, pos['M'] == 6)),
    ("D", And(pos['T'] == 3, pos['L'] == 4)),
    ("E", And(pos['H'] == 2, pos['V'] == 3))
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