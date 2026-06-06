from z3 import *

solver = Solver()

# Declare the positions (1 to 7)
positions = [Int(f'pos_{i}') for i in range(1, 8)]

# Each position must be assigned a unique article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
for article in articles:
    solver.add(Distinct([position for position in positions]))
    # Wait, no: the above is incorrect. We need to assign each article to a unique position.
    # Let's re-declare: each position holds one article, and all articles are used exactly once.

# Correct approach: Use a list of Int variables representing the article at each position.
# We'll map articles to unique integers for easier constraint handling.
article_to_int = {
    'G': 0,
    'H': 1,
    'J': 2,
    'Q': 3,
    'R': 4,
    'S': 5,
    'Y': 6
}
int_to_article = {v: k for k, v in article_to_int.items()}

# Assign each position a unique article (as an integer)
position_articles = [Int(f'pos_article_{i}') for i in range(1, 8)]
for i in range(7):
    solver.add(position_articles[i] >= 0, position_articles[i] <= 6)

# All articles are used exactly once
solver.add(Distinct(position_articles))

# Helper function to get the article at a position
def article_at(pos):
    # pos is 1-based
    return position_articles[pos-1]

# Helper function to check if an article is at a position
def is_article_at(pos, article):
    return article_at(pos) == article_to_int[article]

# Base constraints

# 1. Consecutive articles cannot cover the same topic as each other.
# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
finance_articles = [article_to_int['G'], article_to_int['H'], article_to_int['J']]
nutrition_articles = [article_to_int['Q'], article_to_int['R'], article_to_int['S']]
wildlife_articles = [article_to_int['Y']]

def get_topic(article_int):
    if article_int in finance_articles:
        return 0  # finance
    elif article_int in nutrition_articles:
        return 1  # nutrition
    else:
        return 2  # wildlife

for i in range(1, 7):
    topic_i = get_topic(article_at(i))
    topic_i_plus_1 = get_topic(article_at(i+1))
    solver.add(topic_i != topic_i_plus_1)

# 2. S can be earlier than Q only if Q is third.
solver.add(Implies(
    And(is_article_at(1, 'S'), is_article_at(2, 'Q')),
    False  # This is a placeholder; we need to formalize the constraint properly.
))
# Correct formalization:
# If S is before Q, then Q must be third.
# This is equivalent to: If Q is not third, then S cannot be before Q.
# Or: If S is before Q, then Q == 3.
# We can encode this as: Or(S >= Q, Q == 3)
# But since positions are 1-based, "S before Q" means position(S) < position(Q).
# So: If position(S) < position(Q), then position(Q) == 3.

# Let's define position variables for each article for easier constraints.
article_positions = {article: Int(f'pos_{article}') for article in articles}
for article in articles:
    solver.add(article_positions[article] >= 1, article_positions[article] <= 7)
    # Each position is assigned to exactly one article
    solver.add(Distinct(list(article_positions.values())))

# Link position_articles and article_positions
for i in range(1, 8):
    for article in articles:
        solver.add(Implies(position_articles[i-1] == article_to_int[article], article_positions[article] == i))
        solver.add(Implies(article_positions[article] == i, position_articles[i-1] == article_to_int[article]))

# Now, the constraint "S can be earlier than Q only if Q is third" becomes:
# If article_positions['S'] < article_positions['Q'], then article_positions['Q'] == 3.
solver.add(Implies(
    article_positions['S'] < article_positions['Q'],
    article_positions['Q'] == 3
))

# 3. S must be earlier than Y.
solver.add(article_positions['S'] < article_positions['Y'])

# 4. J must be earlier than G, and G must be earlier than R.
solver.add(article_positions['J'] < article_positions['G'])
solver.add(article_positions['G'] < article_positions['R'])

# Additional constraint: G is fourth.
solver.add(article_positions['G'] == 4)

# Now, evaluate the multiple choice options
found_options = []

# Option A: H is fifth
solver.push()
solver.add(article_positions['H'] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J is first
solver.push()
solver.add(article_positions['J'] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is second
solver.push()
solver.add(article_positions['Q'] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is fifth
solver.push()
solver.add(article_positions['S'] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is sixth
solver.push()
solver.add(article_positions['Y'] == 6)
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