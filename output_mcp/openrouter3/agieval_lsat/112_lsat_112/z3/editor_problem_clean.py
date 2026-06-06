from z3 import *

# Create solver
solver = Solver()

# Articles and their topics
# We'll assign integer IDs to articles
# 0: G, 1: H, 2: J (finance)
# 3: Q, 4: R, 5: S (nutrition)
# 6: Y (wildlife)
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
# We'll use a list of variables for positions 1-7
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
# For each position i from 1 to 6, the articles at i and i+1 must have different topics
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
# This means: If pos[S] < pos[Q], then pos[Q] == 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now test each option using the required skeleton
found_options = []

# Option A: G is second
opt_a_constr = (pos['G'] == 2)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: H is second
opt_b_constr = (pos['H'] == 2)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: S is second
opt_c_constr = (pos['S'] == 2)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: R is third
opt_d_constr = (pos['R'] == 3)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Y is third
opt_e_constr = (pos['Y'] == 3)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results according to the required logic
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")