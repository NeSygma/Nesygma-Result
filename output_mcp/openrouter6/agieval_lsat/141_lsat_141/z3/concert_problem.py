from z3 import *

solver = Solver()

# Declare variables for positions (1 to 6)
guitarist = Int('guitarist')
keyboard = Int('keyboard')
percussionist = Int('percussionist')
saxophonist = Int('saxophonist')
trumpeter = Int('trumpeter')
violinist = Int('violinist')

# All positions are between 1 and 6 inclusive
solver.add(guitarist >= 1, guitarist <= 6)
solver.add(keyboard >= 1, keyboard <= 6)
solver.add(percussionist >= 1, percussionist <= 6)
solver.add(saxophonist >= 1, saxophonist <= 6)
solver.add(trumpeter >= 1, trumpeter <= 6)
solver.add(violinist >= 1, violinist <= 6)

# All positions are distinct
solver.add(Distinct([guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist]))

# Base constraints
# 1. Guitarist does not perform the fourth solo
solver.add(guitarist != 4)

# 2. Percussionist before keyboard
solver.add(percussionist < keyboard)

# 3. Keyboard after violinist and before guitarist
solver.add(violinist < keyboard)
solver.add(keyboard < guitarist)

# 4. Saxophonist after either percussionist or trumpeter, but not both
sax_gt_perc = saxophonist > percussionist
sax_gt_trump = saxophonist > trumpeter
solver.add(Or(And(sax_gt_perc, Not(sax_gt_trump)), And(Not(sax_gt_perc), sax_gt_trump)))

# Define options as constraints
opt_a = (keyboard == 1)
opt_b = (guitarist == 2)
opt_c = (guitarist < saxophonist)
opt_d = (guitarist < percussionist)
opt_e = (keyboard < saxophonist)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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