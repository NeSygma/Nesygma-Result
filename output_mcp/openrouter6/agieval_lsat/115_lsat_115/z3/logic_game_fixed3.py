from z3 import *

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
# Map article to integer code
article_to_int = {a: i for i, a in enumerate(articles)}
int_to_article = {i: a for a, i in article_to_int.items()}

# Topics: finance=0, nutrition=1, wildlife=2
topic_of = {}
for a in articles:
    if a in ['G', 'H', 'J']:
        topic_of[article_to_int[a]] = 0
    elif a in ['Q', 'R', 'S']:
        topic_of[article_to_int[a]] = 1
    else:  # Y
        topic_of[article_to_int[a]] = 2

# Create order array: order[i] = article integer at position i (0-indexed positions 0..6)
order = [Int(f'order_{i}') for i in range(7)]

solver = Solver()

# Each position gets a unique article code
for i in range(7):
    solver.add(Or([order[i] == article_to_int[a] for a in articles]))

# All positions distinct
solver.add(Distinct(order))

# Helper: get topic of article at position i
def get_topic(pos_expr):
    # pos_expr is an integer expression representing article code
    # Return topic integer expression
    # Use If chain over all possible article codes
    t = IntVal(-1)  # placeholder
    for a_int, topic in topic_of.items():
        t = If(pos_expr == a_int, topic, t)
    return t

# Constraint 1: Consecutive articles cannot cover the same topic
for i in range(6):
    topic_i = get_topic(order[i])
    topic_i1 = get_topic(order[i+1])
    solver.add(topic_i != topic_i1)

# Positions of specific articles
pos_S = Int('pos_S')
pos_Q = Int('pos_Q')
pos_Y = Int('pos_Y')
pos_J = Int('pos_J')
pos_G = Int('pos_G')
pos_R = Int('pos_R')
pos_H = Int('pos_H')

# Map each article to its position (1-indexed)
for a in articles:
    a_int = article_to_int[a]
    # Find which position has this article
    pos_expr = Int(f'pos_{a}')
    solver.add(Or([pos_expr == i+1 for i in range(7) if order[i] == a_int]))
    # Also ensure consistency: if order[i] == a_int then pos_expr == i+1
    # We'll add constraints linking order and pos_expr
    for i in range(7):
        solver.add(Implies(order[i] == a_int, pos_expr == i+1))

# Constraint 2: S can be earlier than Q only if Q is third
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos_S < pos_Y)

# Constraint 4: J < G < R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Function to count solutions
def count_solutions(solver, decision_vars):
    s = Solver()
    s.add(solver.assertions())
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = tuple((v, m.eval(v, model_completion=True)) for v in decision_vars)
        solutions.append(sol)
        blocking = Or([v != m.eval(v, model_completion=True) for v in decision_vars])
        s.add(blocking)
    return len(solutions)

# Decision variables: the order array and position variables
decision_vars = order + [pos_S, pos_Q, pos_Y, pos_J, pos_G, pos_R, pos_H]

# Answer choices
options = [
    ("A", pos_H == 4),  # H is fourth
    ("B", pos_H == 6),  # H is sixth
    ("C", pos_R == 4),  # R is fourth
    ("D", pos_R == 7),  # R is seventh
    ("E", pos_Y == 5)   # Y is fifth
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    num_solutions = count_solutions(solver, decision_vars)
    if num_solutions == 1:
        found_options.append(letter)
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