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
# Which means exactly one of them is true.
solver.add(If(percussionist < saxophonist, 1, 0) + If(trumpeter < saxophonist, 1, 0) == 1)

# Now test each option: which member CAN be the third solo?
# The one that CANNOT is the answer.

options = [
    ("A", guitarist == 3),
    ("B", keyboard == 3),
    ("C", saxophonist == 3),
    ("D", trumpeter == 3),
    ("E", violinist == 3)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Also print the model for verification
        m = solver.model()
        print(f"Option {letter} is possible:")
        for var, name in [(guitarist, "guitarist"), (keyboard, "keyboard"), (percussionist, "percussionist"), 
                          (saxophonist, "saxophonist"), (trumpeter, "trumpeter"), (violinist, "violinist")]:
            print(f"  {name} = {m[var]}")
    else:
        print(f"Option {letter} is NOT possible")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")