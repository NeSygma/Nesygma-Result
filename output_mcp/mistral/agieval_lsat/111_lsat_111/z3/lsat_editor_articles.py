from z3 import *

# BENCHMARK_MODE: ON (model-finding with guaranteed solvable problems)
BENCHMARK_MODE = True

# Create a solver instance
solver = Solver()

# Positions: 1 to 7 (1-indexed for clarity)
positions = [Int(f'pos_{i}') for i in range(1, 8)]

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

# Helper: All articles are assigned to distinct positions
solver.add(Distinct(positions))

# Helper: Map each position to an article
# We'll use the fact that positions are integers 1..7 and articles are symbolic
# To enforce that each position has exactly one article, we can use the distinctness above
# and later ensure that the values are in the set of articles.

# Constrain each position to be one of the articles
for pos in positions:
    solver.add(Or([pos == ord(a) for a in articles]))

# Helper: Convert integer back to article symbol for readability
# We'll use a model evaluation trick later

# Base constraints from the problem

# 1. G is fourth
solver.add(positions[3] == ord('G'))  # positions[3] is 4th position (0-indexed as 3)

# 2. J must be earlier than G, and G must be earlier than R
# J < G < R in position order
# Since positions are 1..7, we can use < directly
solver.add(And(
    positions[0] == ord('J') >> positions[0] < positions[3],  # J < G
    positions[3] < positions[4]  # G < R (assuming R is at position 5, but we need to find R's position)
))

# Wait, the above is incorrect. We need to find the positions of J, G, R.
# Let me rephrase: There exist positions for J, G, R such that J < G < R.
# Since G is fixed at position 4, J must be in a position < 4, and R must be in a position > 4.

# Let's extract the positions of J, G, R, S, Q, Y, H
# G is at position 4 (0-indexed position 3)

# 3. S must be earlier than Y
# 4. Consecutive articles cannot cover the same topic
# 5. S can be earlier than Q only if Q is third

# Let's define the positions of each article as variables for clarity
# We'll use a mapping from article to its position
article_to_pos = {a: Int(f'pos_{a}') for a in articles}

# Constrain each article to a unique position
solver.add(Distinct(list(article_to_pos.values())))

# Constrain each position to be in 1..7
for a in articles:
    solver.add(article_to_pos[a] >= 1, article_to_pos[a] <= 7)

# G is fourth
solver.add(article_to_pos['G'] == 4)

# J < G < R
solver.add(article_to_pos['J'] < article_to_pos['G'])
solver.add(article_to_pos['G'] < article_to_pos['R'])

# S must be earlier than Y
solver.add(article_to_pos['S'] < article_to_pos['Y'])

# Consecutive articles cannot cover the same topic
# We need to ensure that for all positions i from 1 to 6, the topics of the articles at i and i+1 are different
# To do this, we need to know the article at each position, which we can derive from the article_to_pos mapping
# Let's define a function to get the article at a given position
# We can use the following trick: for each position p, there is exactly one article a such that article_to_pos[a] == p

# Let's define a list of articles in order
order = [Int(f'order_{i}') for i in range(1, 8)]

# Each order[i] is the article at position i+1
for i in range(7):
    pos_val = i + 1
    # order[i] is the article at position pos_val
    # There should be exactly one article a such that article_to_pos[a] == pos_val
    solver.add(Or([And(order[i] == ord(a), article_to_pos[a] == pos_val) for a in articles]))
    # Ensure only one article is assigned to this position
    solver.add(And([
        Implies(article_to_pos[a] == pos_val, order[i] == ord(a))
        for a in articles
    ]))

# Now, enforce that consecutive articles have different topics
for i in range(6):
    a1 = order[i]
    a2 = order[i+1]
    topic1 = get_topic(chr(a1))
    topic2 = get_topic(chr(a2))
    solver.add(topic1 != topic2)

# S can be earlier than Q only if Q is third
# This means: If S < Q, then Q must be at position 3
# In logical terms: S < Q => Q == 3
# Which is equivalent to: Not(S < Q) or Q == 3
# Or: Q != 3 or S >= Q
solver.add(Or(
    article_to_pos['Q'] == 3,
    article_to_pos['S'] >= article_to_pos['Q']
))

# Now, we have the base constraints. Let's check the multiple-choice options.

# We need to check each option independently
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