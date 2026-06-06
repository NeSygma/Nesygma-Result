from z3 import *

solver = Solver()

# Positions: 0 to 6 (7 positions)
positions = list(range(7))

# Articles
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Assign each article to a unique position
article_pos = {art: Int(f'art_pos_{art}') for art in articles}

# Each position is assigned to exactly one article
solver.add(Distinct(list(article_pos.values())))
for art in articles:
    solver.add(article_pos[art] >= 0, article_pos[art] < 7)

# Topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# Helper function to get topic of an article
def get_topic(art):
    if art in finance:
        return 'finance'
    elif art in nutrition:
        return 'nutrition'
    else:
        return 'wildlife'

# Consecutive articles cannot cover the same topic
for i in range(6):
    for art1 in articles:
        for art2 in articles:
            solver.add(Implies(
                And(article_pos[art1] == i, article_pos[art2] == i+1),
                get_topic(art1) != get_topic(art2)
            ))

# S can be earlier than Q only if Q is third
solver.add(Implies(
    article_pos['S'] < article_pos['Q'],
    article_pos['Q'] == 2
))

# S must be earlier than Y
solver.add(article_pos['S'] < article_pos['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(article_pos['J'] < article_pos['G'])
solver.add(article_pos['G'] < article_pos['R'])

# Now, evaluate each option for S's position
found_options = []

# Option A: S is first (position 0)
solver.push()
solver.add(article_pos['S'] == 0)
res_A = solver.check()
solver.pop()

# Option B: S is third (position 2)
solver.push()
solver.add(article_pos['S'] == 2)
res_B = solver.check()
solver.pop()

# Option C: S is fourth (position 3)
solver.push()
solver.add(article_pos['S'] == 3)
res_C = solver.check()
solver.pop()

# Option D: S is fifth (position 4)
solver.push()
solver.add(article_pos['S'] == 4)
res_D = solver.check()
solver.pop()

# Option E: S is sixth (position 5)
solver.push()
solver.add(article_pos['S'] == 5)
res_E = solver.check()
solver.pop()

# Determine which position is the EXCEPT position
# The EXCEPT position is the one where solver.check() returns unsat
if res_A == unsat:
    print("STATUS: sat")
    print("answer:A")
elif res_B == unsat:
    print("STATUS: sat")
    print("answer:B")
elif res_C == unsat:
    print("STATUS: sat")
    print("answer:C")
elif res_D == unsat:
    print("STATUS: sat")
    print("answer:D")
elif res_E == unsat:
    print("STATUS: sat")
    print("answer:E")
else:
    print("STATUS: unsat")
    print("Refine: All positions are possible (no EXCEPT position found)")