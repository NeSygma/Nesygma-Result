from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# All articles
articles = finance + nutrition + wildlife  # ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Create an array for the sequence: seq[i] = article at position i+1 (0-indexed)
seq = [Int(f'seq_{i}') for i in range(7)]

solver = Solver()

# Each position must be one of the articles (1-7, but we'll map articles to numbers)
# Let's assign numbers to articles: G=1, H=2, J=3, Q=4, R=5, S=6, Y=7
article_to_num = {art: i+1 for i, art in enumerate(articles)}
num_to_article = {i+1: art for i, art in enumerate(articles)}

# Constraint: Each position must be a valid article number
for i in range(7):
    solver.add(Or([seq[i] == article_to_num[art] for art in articles]))

# All positions must be distinct (each article appears exactly once)
solver.add(Distinct(seq))

# Helper function to get topic of an article number
def topic_of(num):
    art = num_to_article[num]
    if art in finance:
        return 'finance'
    elif art in nutrition:
        return 'nutrition'
    else:
        return 'wildlife'

# Constraint: Consecutive articles cannot have the same topic
for i in range(6):
    # For each pair of consecutive positions, their topics must differ
    # We need to express this without Python if/else in constraints
    # Use Or over all possible article combinations
    for a1 in articles:
        for a2 in articles:
            if topic_of(article_to_num[a1]) == topic_of(article_to_num[a2]):
                # Same topic, cannot be consecutive
                solver.add(Not(And(seq[i] == article_to_num[a1], seq[i+1] == article_to_num[a2])))

# Now we need to map positions back to articles for the specific constraints
# Let's create helper functions to get position of each article
def pos_of(art):
    num = article_to_num[art]
    # Return the position (1-indexed) where article 'art' appears
    # We'll use an Or-loop pattern
    pos = Int(f'pos_{art}')
    solver.add(Or([And(seq[i] == num, pos == i+1) for i in range(7)]))
    return pos

# Get positions for relevant articles
pos_S = pos_of('S')
pos_Q = pos_of('Q')
pos_Y = pos_of('Y')
pos_J = pos_of('J')
pos_G = pos_of('G')
pos_R = pos_of('R')

# Constraint: S can be earlier than Q only if Q is third
# If S < Q, then Q must be at position 3
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# Constraint: S must be earlier than Y
solver.add(pos_S < pos_Y)

# Constraint: J must be earlier than G, and G must be earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Now test each answer choice to see which positions are IMPOSSIBLE for S
impossible_options = []

# Test A: S could be first
solver.push()
solver.add(pos_S == 1)
result_A = solver.check()
solver.pop()
if result_A != sat:
    impossible_options.append('A')

# Test B: S could be third
solver.push()
solver.add(pos_S == 3)
result_B = solver.check()
solver.pop()
if result_B != sat:
    impossible_options.append('B')

# Test C: S could be fourth
solver.push()
solver.add(pos_S == 4)
result_C = solver.check()
solver.pop()
if result_C != sat:
    impossible_options.append('C')

# Test D: S could be fifth
solver.push()
solver.add(pos_S == 5)
result_D = solver.check()
solver.pop()
if result_D != sat:
    impossible_options.append('D')

# Test E: S could be sixth
solver.push()
solver.add(pos_S == 6)
result_E = solver.check()
solver.pop()
if result_E != sat:
    impossible_options.append('E')

# Print results
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found (all positions possible)")