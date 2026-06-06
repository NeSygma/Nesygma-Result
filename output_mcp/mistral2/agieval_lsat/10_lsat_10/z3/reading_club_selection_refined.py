from z3 import *

solver = Solver()

# Declare symbolic variables for the selection of works
# We have 9 works: 3 French novels (F1, F2, F3), 3 Russian novels (R1, R2, R3),
# 2 French plays (FP1, FP2), and 1 Russian play (RP1).

# Selection variables: 1 if selected, 0 otherwise
F_novels = [Int(f"F_novel_{i}") for i in range(3)]
R_novels = [Int(f"R_novel_{i}") for i in range(3)]
F_plays = [Int(f"F_play_{i}") for i in range(2)]
RP = Int("RP_play")

# Initialize selection variables to 0 or 1
for v in F_novels + R_novels + F_plays:
    solver.add(Or(v == 0, v == 1))
solver.add(Or(RP == 0, RP == 1))

# Total number of works selected: at least 5 and at most 6
total_selected = Sum(F_novels) + Sum(R_novels) + Sum(F_plays) + RP
solver.add(total_selected >= 5, total_selected <= 6)

# No more than four French works are selected
# French works: F_novels + F_plays
french_works = Sum(F_novels) + Sum(F_plays)
solver.add(french_works <= 4)

# At least three but no more than four novels are selected
novels_selected = Sum(F_novels) + Sum(R_novels)
solver.add(novels_selected >= 3, novels_selected <= 4)

# At least as many French novels as Russian novels
solver.add(Sum(F_novels) >= Sum(R_novels))

# If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(F_plays[0] == 1, F_plays[1] == 1), RP == 0))

# Base constraints for the selection

# Now, evaluate each option to see which one must be selected in all valid scenarios
# We check the negation of each option: if the negation is unsat, the option is necessarily true

# Option A: one French novel and one French play
# Negation: No French novel OR no French play
opt_a_neg = Or(Sum(F_novels) == 0, Sum(F_plays) == 0)

# Option B: one French novel and one Russian play
# Negation: No French novel OR no Russian play
opt_b_neg = Or(Sum(F_novels) == 0, RP == 0)

# Option C: one Russian novel and one French play
# Negation: No Russian novel OR no French play
opt_c_neg = Or(Sum(R_novels) == 0, Sum(F_plays) == 0)

# Option D: two French novels
# Negation: Less than two French novels
opt_d_neg = Sum(F_novels) < 2

# Option E: two Russian novels
# Negation: Less than two Russian novels
opt_e_neg = Sum(R_novels) < 2

# Test the negation of each option
necessarily_true = []
for letter, neg_constr in [("A", opt_a_neg), ("B", opt_b_neg), ("C", opt_c_neg), ("D", opt_d_neg), ("E", opt_e_neg)]:
    s_neg = Solver()
    s_neg.add(solver.assertions())
    s_neg.add(neg_constr)
    if s_neg.check() == unsat:
        necessarily_true.append(letter)

if len(necessarily_true) == 1:
    print("STATUS: sat")
    print(f"answer:{necessarily_true[0]}")
elif len(necessarily_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessarily true options found {necessarily_true}")
else:
    print("STATUS: unsat")
    print("Refine: No necessarily true options found")