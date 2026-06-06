from z3 import *

solver = Solver()

# Six members, each has a solo position from 1 to 6 (1 = earliest, 6 = latest)
guitarist = Int('guitarist')
keyboard = Int('keyboard')
percussionist = Int('percussionist')
saxophonist = Int('saxophonist')
trumpeter = Int('trumpeter')
violinist = Int('violinist')

members = [guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist]

# Each performs exactly one solo (positions 1-6, all distinct)
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: The guitarist does not perform the fourth solo
solver.add(guitarist != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does
solver.add(percussionist < keyboard)

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
# and at some time before the guitarist does
solver.add(violinist < keyboard)
solver.add(keyboard < guitarist)

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist
# does or the trumpeter does, but not both.
# XOR: (percussionist < saxophonist) XOR (trumpeter < saxophonist)
solver.add(If(percussionist < saxophonist, 1, 0) + If(trumpeter < saxophonist, 1, 0) == 1)

# Now test each option: which member CANNOT be the third solo?
# We check each option for being SAT (possible). The one that's UNSAT is the answer.

options = [
    ("A", guitarist == 3),
    ("B", keyboard == 3),
    ("C", saxophonist == 3),
    ("D", trumpeter == 3),
    ("E", violinist == 3)
]

# Collect options that are possible (SAT)
possible_options = []
impossible_options = []

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        possible_options.append(letter)
    else:
        impossible_options.append(letter)
    solver.pop()

# The question asks "which one CANNOT perform the third solo?"
# So we're looking for the option that is impossible.
# If exactly one option is impossible, that's our answer.
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options impossible {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options impossible (all are possible)")