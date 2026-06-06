from z3 import *

# Create position variables for each article (1-7)
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')
articles = [G, H, J, Q, R, S, Y]
article_names = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

solver = Solver()

# Each article is in position 1-7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All articles in distinct positions
solver.add(Distinct(articles))

# Topics: Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# Consecutive articles cannot cover the same topic
# For any two articles in consecutive positions, they must be from different topics

# Helper: check if two articles are in consecutive positions
def are_consecutive(a1, a2):
    return Or(a1 - a2 == 1, a2 - a1 == 1)

# Finance articles: G, H, J
finance = [G, H, J]
# Nutrition articles: Q, R, S
nutrition = [Q, R, S]
# Wildlife: Y

# No two finance articles can be consecutive
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(Not(are_consecutive(finance[i], finance[j])))

# No two nutrition articles can be consecutive
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(Not(are_consecutive(nutrition[i], nutrition[j])))

# Y is the only wildlife article, so no consecutive wildlife conflict needed

# S can be earlier than Q only if Q is third
# "S can be earlier than Q only if Q is third" means: if S < Q then Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now check each option
options = {
    "A": [H, S, J, Q, Y, G, R],  # H, S, J, Q, Y, G, R
    "B": [J, Q, G, H, S, Y, R],  # J, Q, G, H, S, Y, R
    "C": [Q, J, S, H, Y, G, R],  # Q, J, S, H, Y, G, R
    "D": [Q, J, Y, S, G, R, H],  # Q, J, Y, S, G, R, H
    "E": [S, G, Q, J, Y, R, H],  # S, G, Q, J, Y, R, H
}

found_options = []
for letter, order in options.items():
    solver.push()
    # Add constraints that fix the positions
    for i, var in enumerate(order):
        solver.add(var == i + 1)
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