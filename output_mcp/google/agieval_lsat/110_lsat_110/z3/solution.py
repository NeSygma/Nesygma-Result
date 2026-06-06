from z3 import *

# Articles
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
# Topics
topic = {'G': 'F', 'H': 'F', 'J': 'F', 'Q': 'N', 'R': 'N', 'S': 'N', 'Y': 'W'}

# pos[a] is the position of article a (1-7)
pos = {a: Int(f'pos_{a}') for a in articles}
# article_at[p] is the article at position p (1-7)
article_at = {p: Const(f'article_at_{p}', StringSort()) for p in range(1, 8)}

solver = Solver()

# Domain constraints
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

for p in range(1, 8):
    solver.add(Or([article_at[p] == a for a in articles]))
    # Link pos and article_at
    for a in articles:
        solver.add(Implies(article_at[p] == a, pos[a] == p))

# Condition 1: Consecutive articles cannot cover the same topic
for p in range(1, 7):
    def get_topic(a):
        return topic[a]
    
    # topic_at[p]
    topic_p_f = Or([And(article_at[p] == a, get_topic(a) == 'F') for a in articles])
    topic_p_n = Or([And(article_at[p] == a, get_topic(a) == 'N') for a in articles])
    topic_p_w = Or([And(article_at[p] == a, get_topic(a) == 'W') for a in articles])
    
    topic_next_f = Or([And(article_at[p+1] == a, get_topic(a) == 'F') for a in articles])
    topic_next_n = Or([And(article_at[p+1] == a, get_topic(a) == 'N') for a in articles])
    topic_next_w = Or([And(article_at[p+1] == a, get_topic(a) == 'W') for a in articles])
    
    solver.add(Not(And(topic_p_f, topic_next_f)))
    solver.add(Not(And(topic_p_n, topic_next_n)))
    solver.add(Not(And(topic_p_w, topic_next_w)))

# Condition 2: S can be earlier than Q only if Q is third.
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Condition 3: S must be earlier than Y.
solver.add(pos['S'] < pos['Y'])

# Condition 4: J < G < R.
solver.add(pos['J'] < pos['G'], pos['G'] < pos['R'])

# Question: If Y is fourth
solver.add(pos['Y'] == 4)

# Check if there is at least one valid configuration
if solver.check() == sat:
    print("STATUS: sat")
    # Check options
    options = {
        "A": pos['J'] == 2,
        "B": pos['J'] == 3,
        "C": pos['Q'] == 1,
        "D": pos['Q'] == 3,
        "E": pos['R'] == 7
    }
    
    must_be_true = []
    for letter, constr in options.items():
        solver.push()
        solver.add(Not(constr))
        if solver.check() == unsat:
            must_be_true.append(letter)
        solver.pop()
    
    print(f"Must be true: {must_be_true}")
else:
    print("STATUS: unsat")