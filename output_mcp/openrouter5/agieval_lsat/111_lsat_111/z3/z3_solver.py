from z3 import *

solver = Solver()

# 7 positions (1-indexed for readability)
positions = list(range(1, 8))

# Variables: each article's position
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article gets a distinct position from 1 to 7
articles = [G, H, J, Q, R, S, Y]
solver.add(Distinct(articles))
for a in articles:
    solver.add(a >= 1, a <= 7)

# Topics: Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# Consecutive articles cannot cover the same topic.
# We encode this by saying for each pair of positions i and i+1,
# the articles at those positions cannot be from the same topic group.
# We'll use an auxiliary function: for each position, which article is there?
# Better: use constraints on the position variables.

# For each pair of consecutive positions (i, i+1), we forbid same-topic articles.
# We can do this by iterating over all pairs of articles that share a topic
# and ensuring they are not consecutive.

# Finance articles: G, H, J
finance = [G, H, J]
# Nutrition articles: Q, R, S
nutrition = [Q, R, S]
# Wildlife: Y (only one, so no consecutive issue with itself)

# For each pair of finance articles, they cannot be consecutive
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(Abs(finance[i] - finance[j]) != 1)

# For each pair of nutrition articles, they cannot be consecutive
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(Abs(nutrition[i] - nutrition[j]) != 1)

# Also, Y (wildlife) has no same-topic neighbor, so no constraint needed.

# S can be earlier than Q only if Q is third.
# "S can be earlier than Q only if Q is third" means:
# If S < Q, then Q == 3.
# Equivalently: Not(S < Q) OR Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Given condition: G is fourth
solver.add(G == 4)

# Now evaluate each option
# Option A: H is fifth
opt_a = (H == 5)
# Option B: J is first
opt_b = (J == 1)
# Option C: Q is second
opt_c = (Q == 2)
# Option D: S is fifth
opt_d = (S == 5)
# Option E: Y is sixth
opt_e = (Y == 6)

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