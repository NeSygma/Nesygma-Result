from z3 import *

solver = Solver()

# Declare the positions (1st to 7th)
# Each position is assigned an article
positions = [Int(f'pos_{i}') for i in range(1, 8)]

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
topic = {
    'G': 'finance', 'H': 'finance', 'J': 'finance',
    'Q': 'nutrition', 'R': 'nutrition', 'S': 'nutrition',
    'Y': 'wildlife'
}

# Assign each position to an article
article_at_pos = [Int(f'article_at_pos_{i}') for i in range(1, 8)]
for i in range(1, 8):
    solver.add(article_at_pos[i-1] >= 0, article_at_pos[i-1] < 7)

# Each article is assigned to exactly one position
solver.add(Distinct(article_at_pos))

# Map article indices to their names for clarity
article_names = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Topic constraints
# Consecutive articles cannot cover the same topic
for i in range(6):
    pos1 = i
    pos2 = i + 1
    a1 = article_at_pos[pos1]
    a2 = article_at_pos[pos2]
    solver.add(Or(topic[article_names[a1]] != topic[article_names[a2]]))

# S can be earlier than Q only if Q is third
solver.add(Implies(
    IntVal(article_names.index('S')) < IntVal(article_names.index('Q')),
    article_at_pos[2] == IntVal(article_names.index('Q'))  # Q is third (0-indexed position 2)
))

# S must be earlier than Y
solver.add(IntVal(article_names.index('S')) < IntVal(article_names.index('Y')))

# J must be earlier than G, and G must be earlier than R
solver.add(IntVal(article_names.index('J')) < IntVal(article_names.index('G')))
solver.add(IntVal(article_names.index('G')) < IntVal(article_names.index('R')))

# Base constraint: J is third (position 3, 0-indexed position 2)
solver.add(article_at_pos[2] == IntVal(article_names.index('J')))

# Evaluate each option
found_options = []

# Option A: G is fourth (position 4, 0-indexed position 3)
solver.push()
solver.add(article_at_pos[3] == IntVal(article_names.index('G')))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is sixth (position 6, 0-indexed position 5)
solver.push()
solver.add(article_at_pos[5] == IntVal(article_names.index('H')))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is first (position 1, 0-indexed position 0)
solver.push()
solver.add(article_at_pos[0] == IntVal(article_names.index('Q')))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is second (position 2, 0-indexed position 1)
solver.push()
solver.add(article_at_pos[1] == IntVal(article_names.index('S')))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is fifth (position 5, 0-indexed position 4)
solver.push()
solver.add(article_at_pos[4] == IntVal(article_names.index('Y')))
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