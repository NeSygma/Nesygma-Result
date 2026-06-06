from z3 import *

solver = Solver()

# Declare the positions (1st to 7th)
positions = [Int(f'pos_{i}') for i in range(1, 8)]

# Each position must be assigned a unique article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
article_vars = {a: Int(f'article_{a}') for a in articles}

# Assign each article to a unique position
solver.add(Distinct(list(article_vars.values())))
for a in articles:
    solver.add(article_vars[a] >= 1, article_vars[a] <= 7)

# Topic constraints
# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
topic = {
    'G': 0, 'H': 0, 'J': 0,
    'Q': 1, 'R': 1, 'S': 1,
    'Y': 2
}

# Consecutive articles cannot cover the same topic
for i in range(6):
    for j in range(i+1, 7):
        solver.add(Or(
            article_vars[articles[i]] != article_vars[articles[j]] - 1,
            topic[articles[i]] != topic[articles[j]]
        ))

# S can be earlier than Q only if Q is third
solver.add(Implies(article_vars['S'] < article_vars['Q'], article_vars['Q'] == 3))

# S must be earlier than Y
solver.add(article_vars['S'] < article_vars['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(article_vars['J'] < article_vars['G'])
solver.add(article_vars['G'] < article_vars['R'])

# Base constraint: J is third
solver.add(article_vars['J'] == 3)

# Evaluate each option
found_options = []

# Option A: G is fourth
solver.push()
solver.add(article_vars['G'] == 4)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is sixth
solver.push()
solver.add(article_vars['H'] == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is first
solver.push()
solver.add(article_vars['Q'] == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is second
solver.push()
solver.add(article_vars['S'] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is fifth
solver.push()
solver.add(article_vars['Y'] == 5)
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