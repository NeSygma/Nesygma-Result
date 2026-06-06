from z3 import *

solver = Solver()

# Declare variables for the number of each type of work selected
french_novels = Int('french_novels')
russian_novels = Int('russian_novels')
french_plays = Int('french_plays')
russian_play = Int('russian_play')

# Base constraints
solver.add(french_novels >= 0, french_novels <= 3)
solver.add(russian_novels >= 0, russian_novels <= 3)
solver.add(french_plays >= 0, french_plays <= 2)
solver.add(russian_play >= 0, russian_play <= 1)

# Total works selected: at least 5, at most 6
solver.add(french_novels + russian_novels + french_plays + russian_play >= 5)
solver.add(french_novels + russian_novels + french_plays + russian_play <= 6)

# No more than 4 French works
solver.add(french_novels + french_plays <= 4)

# At least 3 but no more than 4 novels
solver.add(french_novels + russian_novels >= 3)
solver.add(french_novels + russian_novels <= 4)

# At least as many French novels as Russian novels
solver.add(french_novels >= russian_novels)

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(french_plays == 2, russian_play == 0))

# Evaluate each option
found_options = []

# Option A: No Russian novels and exactly one play are selected
solver.push()
solver.add(russian_novels == 0)
solver.add(french_plays + russian_play == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Exactly one Russian novel and both French plays are selected
solver.push()
solver.add(russian_novels == 1)
solver.add(french_plays == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Exactly two French novels and the Russian play are selected
solver.push()
solver.add(french_novels == 2)
solver.add(russian_play == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Exactly two French novels and exactly two plays are selected
solver.push()
solver.add(french_novels == 2)
solver.add(french_plays + russian_play == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Exactly two Russian novels and exactly one play are selected
solver.push()
solver.add(russian_novels == 2)
solver.add(french_plays + russian_play == 1)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the answer
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")