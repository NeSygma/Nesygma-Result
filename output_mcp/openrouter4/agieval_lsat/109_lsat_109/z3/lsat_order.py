from z3 import *

solver = Solver()

# Positions 0-6 (first = 0, seventh = 6)
pos_G, pos_H, pos_J = Ints('pos_G pos_H pos_J')
pos_Q, pos_R, pos_S = Ints('pos_Q pos_R pos_S')
pos_Y = Int('pos_Y')

all_positions = [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]

# Domain: each article has a unique position from 0 to 6
for p in all_positions:
    solver.add(p >= 0, p <= 6)
solver.add(Distinct(all_positions))

# Constraint 1: Consecutive articles cannot cover the same topic.
# Finance: G, H, J
finance_articles = [pos_G, pos_H, pos_J]
# For any two finance articles, their positions cannot differ by exactly 1
for i in range(len(finance_articles)):
    for j in range(i+1, len(finance_articles)):
        # |p_i - p_j| != 1
        solver.add(Not(Or(finance_articles[i] - finance_articles[j] == 1,
                          finance_articles[j] - finance_articles[i] == 1)))

# Nutrition: Q, R, S
nutrition_articles = [pos_Q, pos_R, pos_S]
for i in range(len(nutrition_articles)):
    for j in range(i+1, len(nutrition_articles)):
        solver.add(Not(Or(nutrition_articles[i] - nutrition_articles[j] == 1,
                          nutrition_articles[j] - nutrition_articles[i] == 1)))

# Wildlife: Y (only one, so no consecutive same-topic constraint needed)

# Constraint 2: S can be earlier than Q only if Q is third.
# If S < Q then Q must be third (position 2 in 0-indexed)
solver.add(Implies(pos_S < pos_Q, pos_Q == 2))

# Constraint 3: S must be earlier than Y
solver.add(pos_S < pos_Y)

# Constraint 4: J must be earlier than G, and G must be earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Now evaluate each option
# Option A: H, S, J, Q, Y, G, R
opt_a = And(
    pos_H == 0, pos_S == 1, pos_J == 2, pos_Q == 3,
    pos_Y == 4, pos_G == 5, pos_R == 6
)

# Option B: J, Q, G, H, S, Y, R
opt_b = And(
    pos_J == 0, pos_Q == 1, pos_G == 2, pos_H == 3,
    pos_S == 4, pos_Y == 5, pos_R == 6
)

# Option C: Q, J, S, H, Y, G, R
opt_c = And(
    pos_Q == 0, pos_J == 1, pos_S == 2, pos_H == 3,
    pos_Y == 4, pos_G == 5, pos_R == 6
)

# Option D: Q, J, Y, S, G, R, H
opt_d = And(
    pos_Q == 0, pos_J == 1, pos_Y == 2, pos_S == 3,
    pos_G == 4, pos_R == 5, pos_H == 6
)

# Option E: S, G, Q, J, Y, R, H
opt_e = And(
    pos_S == 0, pos_G == 1, pos_Q == 2, pos_J == 3,
    pos_Y == 4, pos_R == 5, pos_H == 6
)

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