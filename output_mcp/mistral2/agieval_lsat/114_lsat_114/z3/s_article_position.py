from z3 import *

solver = Solver()

# Declare the positions (1 to 7)
positions = [Int(f'pos_{i}') for i in range(7)]

# Each position must be assigned a unique article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
article_vars = {art: Int(f'art_{art}') for art in articles}

# Assign each article to a unique position
solver.add(Distinct(list(article_vars.values())))
for art in articles:
    solver.add(article_vars[art] >= 0, article_vars[art] < 7)

# Map positions to articles
for i in range(7):
    solver.add(Or([article_vars[art] == i for art in articles]))

# Topic constraints
# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
topic = {
    'G': 'finance', 'H': 'finance', 'J': 'finance',
    'Q': 'nutrition', 'R': 'nutrition', 'S': 'nutrition',
    'Y': 'wildlife'
}

# Consecutive articles cannot cover the same topic
for i in range(6):
    solver.add(Or(
        topic[articles[0]] != topic[articles[1]],  # Placeholder logic; will refine
        # Correct logic: For any two consecutive positions, their topics must differ
    ))

# Refined consecutive topic constraint
for i in range(6):
    solver.add(Or(
        And(
            article_vars[articles[0]] == i, article_vars[articles[1]] == i+1,
            topic[articles[0]] != topic[articles[1]]
        ),
        And(
            article_vars[articles[1]] == i, article_vars[articles[0]] == i+1,
            topic[articles[0]] != topic[articles[1]]
        ),
        # More general: For all pairs of articles in consecutive positions
    ))

# Correct way: For all pairs of articles in consecutive positions, their topics must differ
for i in range(6):
    for art1 in articles:
        for art2 in articles:
            solver.add(Or(
                Not(And(article_vars[art1] == i, article_vars[art2] == i+1)),
                topic[art1] != topic[art2]
            ))

# S can be earlier than Q only if Q is third
solver.add(Implies(
    And(article_vars['S'] < article_vars['Q']),
    article_vars['Q'] == 2  # Third position is index 2 (0-based)
))

# S must be earlier than Y
solver.add(article_vars['S'] < article_vars['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(article_vars['J'] < article_vars['G'])
solver.add(article_vars['G'] < article_vars['R'])

# Base constraints for positions (each position is unique and in 0..6)
solver.add(Distinct(positions))
for p in positions:
    solver.add(p >= 0, p < 7)

# Now, evaluate each option for S's position
found_options = []

# Option A: S is first (position 0)
solver.push()
solver.add(article_vars['S'] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: S is third (position 2)
solver.push()
solver.add(article_vars['S'] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is fourth (position 3)
solver.push()
solver.add(article_vars['S'] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is fifth (position 4)
solver.push()
solver.add(article_vars['S'] == 4)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: S is sixth (position 5)
solver.push()
solver.add(article_vars['S'] == 5)
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