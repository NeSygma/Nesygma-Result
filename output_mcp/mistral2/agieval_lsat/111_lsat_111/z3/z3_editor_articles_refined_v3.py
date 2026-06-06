from z3 import *

solver = Solver()

# Articles: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Assign each position (1-7) an article
position_articles = [Int(f'pos_article_{i}') for i in range(1, 8)]

# Each position must be assigned an article
for i in range(7):
    solver.add(position_articles[i] >= 0, position_articles[i] <= 6)

# All articles are used exactly once
solver.add(Distinct(position_articles))

# Helper function to get the article at a position
def article_at(pos):
    return position_articles[pos-1]

# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

def get_topic(article_str):
    if article_str in finance:
        return 0
    elif article_str in nutrition:
        return 1
    else:
        return 2

# Consecutive articles cannot cover the same topic
for i in range(1, 7):
    topic_i = get_topic(article_at(i))
    topic_i_plus_1 = get_topic(article_at(i+1))
    solver.add(topic_i != topic_i_plus_1)

# S can be earlier than Q only if Q is third
# If S is before Q, then Q must be third
solver.add(Implies(
    Int('S_pos') < Int('Q_pos'),
    Int('Q_pos') == 3
))

# S must be earlier than Y
solver.add(Int('S_pos') < Int('Y_pos'))

# J must be earlier than G, and G must be earlier than R
solver.add(Int('J_pos') < Int('G_pos'))
solver.add(Int('G_pos') < Int('R_pos'))

# G is fourth
solver.add(Int('G_pos') == 4)

# Link article positions to position_articles
article_to_int = {'G': 0, 'H': 1, 'J': 2, 'Q': 3, 'R': 4, 'S': 5, 'Y': 6}
for article in articles:
    solver.add(Or(
        *[And(
            article_at(pos) == article_to_int[article],
            Int(f'{article}_pos') == pos
        ) for pos in range(1, 8)]
    ))

# Now, evaluate the multiple choice options
found_options = []

# Option A: H is fifth
solver.push()
solver.add(Int('H_pos') == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J is first
solver.push()
solver.add(Int('J_pos') == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is second
solver.push()
solver.add(Int('Q_pos') == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is fifth
solver.push()
solver.add(Int('S_pos') == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is sixth
solver.push()
solver.add(Int('Y_pos') == 6)
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