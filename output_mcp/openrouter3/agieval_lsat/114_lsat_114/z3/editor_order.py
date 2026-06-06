from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# All articles
articles = finance + nutrition + wildlife  # ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Create position variables for each article
pos = {art: Int(f'pos_{art}') for art in articles}

solver = Solver()

# Constraint 1: All positions are distinct and between 1 and 7
for art in articles:
    solver.add(pos[art] >= 1)
    solver.add(pos[art] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[art] for art in articles]))

# Constraint 2: Consecutive articles cannot cover the same topic
# We need to ensure that for any two articles with same topic, their positions are not consecutive
# For each topic, ensure no two articles have consecutive positions
def no_consecutive_same_topic(topic_articles):
    for i in range(len(topic_articles)):
        for j in range(i+1, len(topic_articles)):
            art1 = topic_articles[i]
            art2 = topic_articles[j]
            # They cannot be consecutive: |pos1 - pos2| != 1
            solver.add(Or(pos[art1] - pos[art2] != 1, pos[art2] - pos[art1] != 1))

no_consecutive_same_topic(finance)
no_consecutive_same_topic(nutrition)
# wildlife has only one article, so no constraint needed

# Constraint 3: S can be earlier than Q only if Q is third
# This means: If S < Q, then Q = 3
# Equivalent: (S < Q) => (Q == 3)
# In Z3: Implies(pos['S'] < pos['Q'], pos['Q'] == 3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 4: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 5: J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now test each answer choice
found_options = []

# Test A: S could be first
solver.push()
solver.add(pos['S'] == 1)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Test B: S could be third
solver.push()
solver.add(pos['S'] == 3)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Test C: S could be fourth
solver.push()
solver.add(pos['S'] == 4)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Test D: S could be fifth
solver.push()
solver.add(pos['S'] == 5)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Test E: S could be sixth
solver.push()
solver.add(pos['S'] == 6)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")