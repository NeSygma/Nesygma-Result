from z3 import *

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
topics = {
    'G': 'finance', 'H': 'finance', 'J': 'finance',
    'Q': 'nutrition', 'R': 'nutrition', 'S': 'nutrition',
    'Y': 'wildlife'
}

# Create an array where order[i] = article at position i (1-indexed)
order = [Int(f'order_{i}') for i in range(1, 8)]  # order[0] is position 1, order[6] is position 7

solver = Solver()

# Each position gets a unique article (represented as integer codes)
# Let's map articles to integers: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
article_to_int = {a: i for i, a in enumerate(articles)}
int_to_article = {i: a for a, i in article_to_int.items()}

# Each position must have a valid article code
for i in range(7):
    solver.add(Or([order[i] == article_to_int[a] for a in articles]))

# All positions must have distinct articles
solver.add(Distinct(order))

# Constraint 1: Consecutive articles cannot cover the same topic
# For each position i from 0 to 5 (positions 1-6), check topics of order[i] and order[i+1]
for i in range(6):
    # Get topic of article at position i
    topic_i = If(order[i] == article_to_int['G'], 'finance',
                 If(order[i] == article_to_int['H'], 'finance',
                    If(order[i] == article_to_int['J'], 'finance',
                       If(order[i] == article_to_int['Q'], 'nutrition',
                          If(order[i] == article_to_int['R'], 'nutrition',
                             If(order[i] == article_to_int['S'], 'nutrition', 'wildlife'))))))
    
    # Get topic of article at position i+1
    topic_i1 = If(order[i+1] == article_to_int['G'], 'finance',
                  If(order[i+1] == article_to_int['H'], 'finance',
                     If(order[i+1] == article_to_int['J'], 'finance',
                        If(order[i+1] == article_to_int['Q'], 'nutrition',
                           If(order[i+1] == article_to_int['R'], 'nutrition',
                              If(order[i+1] == article_to_int['S'], 'nutrition', 'wildlife'))))))
    
    # Topics must be different
    solver.add(topic_i != topic_i1)

# Constraint 2: S can be earlier than Q only if Q is third
# Find positions of S and Q
pos_S = Int('pos_S')
pos_Q = Int('pos_Q')
solver.add(Or([pos_S == i+1 for i in range(7) if articles[i] == 'S']))
solver.add(Or([pos_Q == i+1 for i in range(7) if articles[i] == 'Q']))

# If S < Q, then Q must be in position 3
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# Constraint 3: S must be earlier than Y
pos_Y = Int('pos_Y')
solver.add(Or([pos_Y == i+1 for i in range(7) if articles[i] == 'Y']))
solver.add(pos_S < pos_Y)

# Constraint 4: J < G < R
pos_J = Int('pos_J')
pos_G = Int('pos_G')
pos_R = Int('pos_R')
solver.add(Or([pos_J == i+1 for i in range(7) if articles[i] == 'J']))
solver.add(Or([pos_G == i+1 for i in range(7) if articles[i] == 'G']))
solver.add(Or([pos_R == i+1 for i in range(7) if articles[i] == 'R']))
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

# Decision variables: the order array
decision_vars = order + [pos_S, pos_Q, pos_Y, pos_J, pos_G, pos_R]

# Answer choices
options = [
    ("A", pos_H == 4),  # H is fourth
    ("B", pos_H == 6),  # H is sixth
    ("C", pos_R == 4),  # R is fourth
    ("D", pos_R == 7),  # R is seventh
    ("E", pos_Y == 5)   # Y is fifth
]

# Need to define pos_H
pos_H = Int('pos_H')
solver.add(Or([pos_H == i+1 for i in range(7) if articles[i] == 'H']))

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