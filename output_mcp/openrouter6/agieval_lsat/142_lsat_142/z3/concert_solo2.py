from z3 import *

solver = Solver()

# Declare variables for each member's solo position (1 to 6)
guitarist = Int('guitarist')
keyboard = Int('keyboard')
percussionist = Int('percussionist')
saxophonist = Int('saxophonist')
trumpeter = Int('trumpeter')
violinist = Int('violinist')

# All positions are distinct and between 1 and 6
members = [guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist]
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Base constraints from problem
# 1. Guitarist does not perform the fourth solo
solver.add(guitarist != 4)

# 2. Percussionist before keyboard
solver.add(percussionist < keyboard)

# 3. Keyboard after violinist and before guitarist
solver.add(violinist < keyboard)
solver.add(keyboard < guitarist)

# 4. Saxophonist after either percussionist or trumpeter, but not both
# XOR: (percussionist < saxophonist) != (trumpeter < saxophonist)
solver.add((percussionist < saxophonist) != (trumpeter < saxophonist))

# Now test each option: which member cannot be third?
found_unsat_options = []
for letter, constr in [
    ("A", guitarist == 3),
    ("B", keyboard == 3),
    ("C", saxophonist == 3),
    ("D", trumpeter == 3),
    ("E", violinist == 3)
]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_unsat_options.append(letter)
    solver.pop()

if len(found_unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat_options[0]}")
elif len(found_unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")