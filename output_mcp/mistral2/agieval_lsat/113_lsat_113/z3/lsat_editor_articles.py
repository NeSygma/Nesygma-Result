from z3 import *

solver = Solver()

# Declare the positions (1st to 7th)
positions = [Int(f'pos_{i}') for i in range(1, 8)]

# Each position must be assigned a unique article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
article_vars = {a: Int(f'article_{a}') for a in articles}

# Assign each article to a unique position
solver.add(Distinct(positions))
for a in articles:
    solver.add(article_vars[a] >= 1, article_vars[a] <= 7)

# Each position must have exactly one article
for p in positions:
    solver.add(Or([article_vars[a] == p for a in articles]))
    solver.add(Distinct([article_vars[a] for a in articles]))

# Topic constraints
# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
topic = {
    'G': 'finance', 'H': 'finance', 'J': 'finance',
    'Q': 'nutrition', 'R': 'nutrition', 'S': 'nutrition',
    'Y': 'wildlife'
}

# Helper function to get the topic of an article
article_to_topic = Function('article_to_topic', StringSort(), IntSort())
solver.add(article_to_topic(String('G')) == 0)  # finance
solver.add(article_to_topic(String('H')) == 0)  # finance
solver.add(article_to_topic(String('J')) == 0)  # finance
solver.add(article_to_topic(String('Q')) == 1)  # nutrition
solver.add(article_to_topic(String('R')) == 1)  # nutrition
solver.add(article_to_topic(String('S')) == 1)  # nutrition
solver.add(article_to_topic(String('Y')) == 2)  # wildlife

# Consecutive articles cannot cover the same topic
for i in range(6):
    a1 = article_vars[articles[i]]
    a2 = article_vars[articles[i+1]]
    solver.add(Or(
        article_to_topic(Concat(StringVal(""), IntToStr(a1))) != article_to_topic(Concat(StringVal(""), IntToStr(a2))),
        article_to_topic(Concat(StringVal(""), IntToStr(a2))) != article_to_topic(Concat(StringVal(""), IntToStr(a1)))
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