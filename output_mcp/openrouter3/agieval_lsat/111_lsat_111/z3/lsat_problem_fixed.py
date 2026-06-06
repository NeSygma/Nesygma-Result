from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# Create position variables for each article
positions = {article: Int(f'pos_{article}') for article in finance + nutrition + wildlife}

solver = Solver()

# Domain constraints: positions are between 1 and 7
for article in positions:
    solver.add(positions[article] >= 1)
    solver.add(positions[article] <= 7)

# All articles must be in distinct positions
solver.add(Distinct(list(positions.values())))

# Helper function to get topic of an article
def get_topic(article):
    if article in finance:
        return 0  # finance
    elif article in nutrition:
        return 1  # nutrition
    else:  # Y
        return 2  # wildlife

# Constraint 1: Consecutive articles cannot cover the same topic
# For each position i from 1 to 6, ensure that the articles at positions i and i+1 have different topics
# We need to find which article is at each position
# Create an array of articles indexed by position
articles_by_pos = [Int(f'art_at_pos_{i}') for i in range(1, 8)]

# Each position must have exactly one article
# We'll use a different approach: for each pair of articles with same topic, ensure they're not adjacent
for topic in [finance, nutrition]:
    for i in range(len(topic)):
        for j in range(i+1, len(topic)):
            # If two articles have same topic, their positions cannot be consecutive
            solver.add(Or(
                positions[topic[i]] != positions[topic[j]] - 1,
                positions[topic[i]] != positions[topic[j]] + 1
            ))

# Constraint 2: S can be earlier than Q only if Q is third
# This means: If S < Q, then Q = 3
# Equivalent to: (S < Q) => (Q = 3)
# In Z3: Or(S >= Q, positions['Q'] == 3)
solver.add(Or(positions['S'] >= positions['Q'], positions['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(positions['S'] < positions['Y'])

# Constraint 4: J < G < R
solver.add(positions['J'] < positions['G'])
solver.add(positions['G'] < positions['R'])

# Additional constraint from question: G is fourth
solver.add(positions['G'] == 4)

# Now test each option
found_options = []

# Option A: H is fifth
solver.push()
solver.add(positions['H'] == 5)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: J is first
solver.push()
solver.add(positions['J'] == 1)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Q is second
solver.push()
solver.add(positions['Q'] == 2)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: S is fifth
solver.push()
solver.add(positions['S'] == 5)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Y is sixth
solver.push()
solver.add(positions['Y'] == 6)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")