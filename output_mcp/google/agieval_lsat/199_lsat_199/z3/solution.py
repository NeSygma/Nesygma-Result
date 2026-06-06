from z3 import *

# Days: 1, 2, 3, 4, 5, 6
# Antiques: H, L, M, S, T, V
antiques = ['H', 'L', 'M', 'S', 'T', 'V']
# pos[a] is the day (1-6) for antique a
pos = {a: Int(a) for a in antiques}

solver = Solver()

# Each antique is auctioned exactly once per day
for a in antiques:
    solver.add(pos[a] >= 1, pos[a] <= 6)
solver.add(Distinct([pos[a] for a in antiques]))

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

# The question asks: Which one of the following CANNOT be the antique 
# auctioned on the day immediately preceding the day on which the vase is auctioned?
# This means: For which antique 'A' is it impossible that pos[A] == pos[V] - 1?

# Let's check each option:
# (A) harmonica (B) lamp (C) mirror (D) sundial (E) table
# If an option is "CANNOT", it means the solver should return UNSAT when we add pos[A] == pos[V] - 1.

options = [("A", 'H'), ("B", 'L'), ("C", 'M'), ("D", 'S'), ("E", 'T')]
cannot_be = []

for letter, opt in options:
    solver.push()
    solver.add(pos[opt] == pos['V'] - 1)
    if solver.check() == unsat:
        cannot_be.append(letter)
    solver.pop()

print(f"Cannot be: {cannot_be}")
if len(cannot_be) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be[0]}")
else:
    print("STATUS: unsat")