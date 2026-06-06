from z3 import *

# BENCHMARK_MODE: ON (model-finding with guaranteed solvable problems)
BENCHMARK_MODE = True

# Create a solver instance
solver = Solver()

# Articles
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Topics
finance = {'G', 'H', 'J'}
nutrition = {'Q', 'R', 'S'}
wildlife = {'Y'}

def get_topic(article):
    if article in finance:
        return 'finance'
    elif article in nutrition:
        return 'nutrition'
    else:
        return 'wildlife'

# Map each article to its position (1 to 7)
article_to_pos = {a: Int(f'pos_{a}') for a in articles}

# Each position is unique and in 1..7
solver.add(Distinct(list(article_to_pos.values())))
for a in articles:
    solver.add(article_to_pos[a] >= 1, article_to_pos[a] <= 7)

# G is fourth
solver.add(article_to_pos['G'] == 4)

# J < G < R
solver.add(article_to_pos['J'] < article_to_pos['G'])
solver.add(article_to_pos['G'] < article_to_pos['R'])

# S < Y
solver.add(article_to_pos['S'] < article_to_pos['Y'])

# Consecutive articles cannot cover the same topic
# For every pair of articles, if their positions are consecutive, their topics must differ
for a1 in articles:
    for a2 in articles:
        if a1 != a2:
            # If pos(a1) + 1 == pos(a2), then topic(a1) != topic(a2)
            solver.add(Implies(
                article_to_pos[a1] + 1 == article_to_pos[a2],
                get_topic(a1) != get_topic(a2)
            ))

# S can be earlier than Q only if Q is third
# This means: If S < Q, then Q must be at position 3
# In logical terms: S < Q => Q == 3
# Which is equivalent to: Not(S < Q) or Q == 3
# Or: Q != 3 or S >= Q
solver.add(Or(
    article_to_pos['Q'] == 3,
    article_to_pos['S'] >= article_to_pos['Q']
))

# Now, check the multiple-choice options
found_options = []

# Option A: H is fifth
solver.push()
solver.add(article_to_pos['H'] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J is first
solver.push()
solver.add(article_to_pos['J'] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is second
solver.push()
solver.add(article_to_pos['Q'] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is fifth
solver.push()
solver.add(article_to_pos['S'] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is sixth
solver.push()
solver.add(article_to_pos['Y'] == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")