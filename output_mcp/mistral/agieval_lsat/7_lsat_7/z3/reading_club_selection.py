from z3 import *

# Declare boolean variables for each work
# French novels (3)
french_novel = [Bool(f"french_novel_{i}") for i in range(3)]
# Russian novels (3)
russian_novel = [Bool(f"russian_novel_{i}") for i in range(3)]
# French plays (2)
french_play = [Bool(f"french_play_{i}") for i in range(2)]
# Russian play (1)
russian_play = Bool("russian_play")

# Selection is the list of all works
selection = french_novel + russian_novel + french_play + [russian_play]

# Base constraints from the problem
solver = Solver()

# 1. Selection size: at least 5 and at most 6
solver.add(Sum(selection) >= 5)
solver.add(Sum(selection) <= 6)

# 2. No more than 4 French works (novels + plays)
solver.add(Sum(french_novel) + Sum(french_play) <= 4)

# 3. At least 3 but no more than 4 novels
solver.add(Sum(french_novel) + Sum(russian_novel) >= 3)
solver.add(Sum(french_novel) + Sum(russian_novel) <= 4)

# 4. At least as many French novels as Russian novels
solver.add(Sum(french_novel) >= Sum(russian_novel))

# 5. If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(french_play[0], french_play[1]), Not(russian_play)))

# Define constraints for each option
# Option A: one French novel, two Russian novels, one French play, one Russian play
opt_a_constr = And(
    Sum(french_novel) == 1,
    Sum(russian_novel) == 2,
    Sum(french_play) == 1,
    russian_play == True
)

# Option B: two French novels, one Russian novel, two French plays, one Russian play
opt_b_constr = And(
    Sum(french_novel) == 2,
    Sum(russian_novel) == 1,
    Sum(french_play) == 2,
    russian_play == True
)

# Option C: two French novels, two Russian novels, two French plays
opt_c_constr = And(
    Sum(french_novel) == 2,
    Sum(russian_novel) == 2,
    Sum(french_play) == 2,
    russian_play == False
)

# Option D: three French novels, one Russian novel, two French plays
opt_d_constr = And(
    Sum(french_novel) == 3,
    Sum(russian_novel) == 1,
    Sum(french_play) == 2,
    russian_play == False
)

# Option E: three French novels, two Russian novels, one Russian play
opt_e_constr = And(
    Sum(french_novel) == 3,
    Sum(russian_novel) == 2,
    Sum(french_play) == 0,
    russian_play == True
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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