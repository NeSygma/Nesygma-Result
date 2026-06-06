from z3 import *

solver = Solver()

# Base constraints:
# - Total works selected: at least 5, at most 6
# - Group composition:
#   - 3 French novels
#   - 3 Russian novels
#   - 2 French plays
#   - 1 Russian play

# Let's define symbolic variables for the selection:
# f_novels: number of French novels selected (0 to 3)
# r_novels: number of Russian novels selected (0 to 3)
# f_plays: number of French plays selected (0 to 2)
# r_play: number of Russian plays selected (0 or 1)

f_novels = Int('f_novels')
r_novels = Int('r_novels')
f_plays = Int('f_plays')
r_play = Int('r_play')

# Total works selected
total_works = f_novels + r_novels + f_plays + r_play

# Constraints:
# 1. Total works: at least 5, at most 6
solver.add(total_works >= 5, total_works <= 6)

# 2. No more than four French works are selected
# French works = French novels + French plays
solver.add(f_novels + f_plays <= 4)

# 3. At least three but no more than four novels are selected
solver.add(r_novels + f_novels >= 3, r_novels + f_novels <= 4)

# 4. At least as many French novels as Russian novels
solver.add(f_novels >= r_novels)

# 5. If both French plays are selected, then the Russian play is not selected
solver.add(Implies(f_plays == 2, r_play == 0))

# Domain constraints for each variable
solver.add(f_novels >= 0, f_novels <= 3)
solver.add(r_novels >= 0, r_novels <= 3)
solver.add(f_plays >= 0, f_plays <= 2)
solver.add(r_play >= 0, r_play <= 1)

# Now, evaluate each option
found_options = []

# Option A: one French novel, two Russian novels, one French play, one Russian play
solver.push()
solver.add(f_novels == 1, r_novels == 2, f_plays == 1, r_play == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: two French novels, one Russian novel, two French plays, one Russian play
solver.push()
solver.add(f_novels == 2, r_novels == 1, f_plays == 2, r_play == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: two French novels, two Russian novels, two French plays
solver.push()
solver.add(f_novels == 2, r_novels == 2, f_plays == 2, r_play == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: three French novels, one Russian novel, two French plays
solver.push()
solver.add(f_novels == 3, r_novels == 1, f_plays == 2, r_play == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: three French novels, two Russian novels, one Russian play
solver.push()
solver.add(f_novels == 3, r_novels == 2, f_plays == 0, r_play == 1)
if solver.check() == sat:
    found_options.append("E")
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