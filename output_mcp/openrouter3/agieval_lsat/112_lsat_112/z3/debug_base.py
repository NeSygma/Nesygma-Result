from z3 import *

# Create solver
solver = Solver()

# Articles and their topics
article_ids = {
    'G': 0, 'H': 1, 'J': 2,
    'Q': 3, 'R': 4, 'S': 5,
    'Y': 6
}
finance_ids = [0, 1, 2]
nutrition_ids = [3, 4, 5]
wildlife_ids = [6]

# Position variables (1-7)
pos = {article: Int(f'pos_{article}') for article in article_ids}

# Each article gets a unique position from 1 to 7
for article in article_ids:
    solver.add(pos[article] >= 1)
    solver.add(pos[article] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[article] for article in article_ids]))

# Create an array: article_at_position[i] = article ID at position i
article_at = [Int(f'article_at_{i}') for i in range(1, 8)]

# Each position must have exactly one article ID (0-6)
for i in range(1, 8):
    solver.add(Or([article_at[i-1] == id for id in range(7)]))

# Each article ID must be at exactly one position
for id in range(7):
    solver.add(Or([pos[article] == i for article, aid in article_ids.items() if aid == id]))

# Link pos and article_at: if article_at[i] == id, then the article with that ID must be at position i
for article, id in article_ids.items():
    for i in range(1, 8):
        solver.add(Implies(article_at[i-1] == id, pos[article] == i))

# Constraint 1: Consecutive articles cannot cover the same topic
def get_topic_id(id):
    if id in finance_ids:
        return 0  # finance
    elif id in nutrition_ids:
        return 1  # nutrition
    else:  # wildlife
        return 2  # wildlife

# For each consecutive pair, ensure different topics
for i in range(1, 7):
    # article_at[i] and article_at[i+1] must have different topics
    # We'll use a constraint that checks all possible same-topic pairs
    same_topic_pairs = []
    for id1 in range(7):
        for id2 in range(7):
            if id1 != id2 and get_topic_id(id1) == get_topic_id(id2):
                same_topic_pairs.append(And(article_at[i-1] == id1, article_at[i] == id2))
    # If they are a same-topic pair, that's not allowed
    solver.add(Not(Or(same_topic_pairs)))

# Constraint 2: S can be earlier than Q only if Q is third
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Check if base constraints are satisfiable
result = solver.check()
print(f"Base constraints result: {result}")

if result == sat:
    m = solver.model()
    print("Base model:")
    for article in article_ids:
        print(f"  {article}: position {m[pos[article]]}")
    print("\nArticle at each position:")
    for i in range(1, 8):
        print(f"  Position {i}: article ID {m[article_at[i-1]]}")
else:
    print("Base constraints are unsatisfiable!")