from z3 import *

# Create solver
solver = Solver()

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']
all_articles = finance + nutrition + wildlife  # ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Position variables (1-7)
pos = {article: Int(f'pos_{article}') for article in all_articles}

# Each article gets a unique position from 1 to 7
for article in all_articles:
    solver.add(pos[article] >= 1)
    solver.add(pos[article] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[article] for article in all_articles]))

# Create a mapping from position to article (inverse of pos)
# We'll use an array: article_at_position[i] = article at position i
# Since we have 7 positions, we can use a list of variables
article_at = [Int(f'article_at_{i}') for i in range(1, 8)]  # positions 1-7

# Each position must have exactly one article
# For each position, it must be one of the articles
for i in range(1, 8):
    solver.add(Or([article_at[i-1] == article for article in all_articles]))

# Each article must be at exactly one position
for article in all_articles:
    solver.add(Or([pos[article] == i for i in range(1, 8)]))

# Link pos and article_at: if article_at[i] == article, then pos[article] == i
for article in all_articles:
    for i in range(1, 8):
        solver.add(Implies(article_at[i-1] == article, pos[article] == i))

# Constraint 1: Consecutive articles cannot cover the same topic
# For each position i from 1 to 6, the articles at i and i+1 must have different topics
def get_topic(article):
    if article in finance:
        return 0  # finance
    elif article in nutrition:
        return 1  # nutrition
    else:  # Y
        return 2  # wildlife

# For each consecutive pair, ensure different topics
for i in range(1, 7):
    # article_at[i] and article_at[i+1] must have different topics
    # We'll use a constraint that checks all possible same-topic pairs
    same_topic_pairs = []
    for a1 in all_articles:
        for a2 in all_articles:
            if a1 != a2 and get_topic(a1) == get_topic(a2):
                same_topic_pairs.append(And(article_at[i-1] == a1, article_at[i] == a2))
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