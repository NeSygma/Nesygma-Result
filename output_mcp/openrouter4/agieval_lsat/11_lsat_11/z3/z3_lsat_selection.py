from z3 import *

solver = Solver()

# Decision variables: counts of each type of work selected
f_novels = Int('f_novels')   # French novels (0-3)
r_novels = Int('r_novels')   # Russian novels (0-3)
f_plays  = Int('f_plays')    # French plays (0-2)
r_play   = Int('r_play')     # Russian play (0-1)

# Domain constraints
solver.add(f_novels >= 0, f_novels <= 3)
solver.add(r_novels >= 0, r_novels <= 3)
solver.add(f_plays >= 0, f_plays <= 2)
solver.add(r_play >= 0, r_play <= 1)

# Total works selected: at least 5, at most 6
total = f_novels + r_novels + f_plays + r_play
solver.add(total >= 5, total <= 6)

# Constraint 1: No more than 4 French works selected
solver.add(f_novels + f_plays <= 4)

# Constraint 2: At least 3 but no more than 4 novels selected
solver.add(f_novels + r_novels >= 3)
solver.add(f_novels + r_novels <= 4)

# Constraint 3: At least as many French novels as Russian novels
solver.add(f_novels >= r_novels)

# Constraint 4: If both French plays are selected, then the Russian play is not selected
solver.add(Implies(f_plays == 2, r_play == 0))

# Now test each option
# (A) No Russian novels and exactly one play
opt_a = And(r_novels == 0, f_plays + r_play == 1)

# (B) Exactly one Russian novel and both French plays
opt_b = And(r_novels == 1, f_plays == 2)

# (C) Exactly two French novels and the Russian play
opt_c = And(f_novels == 2, r_play == 1)

# (D) Exactly two French novels and exactly two plays
opt_d = And(f_novels == 2, f_plays + r_play == 2)

# (E) Exactly two Russian novels and exactly one play
opt_e = And(r_novels == 2, f_plays + r_play == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    res = solver.check()
    print(f"Option {letter}: {res}")
    if res == sat:
        m = solver.model()
        print(f"  f_novels={m[f_novels]}, r_novels={m[r_novels]}, f_plays={m[f_plays]}, r_play={m[r_play]}")
        found_options.append(letter)
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